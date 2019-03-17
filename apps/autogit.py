from subprocess import check_output, CalledProcessError
from talon.voice import Context, Word
from talon import resource
from ..utils import parse_words, insert
import re
import pprint
import json
from os import path

data_filepath = path.join(path.dirname(path.abspath(__file__)), "git.json")

pp = pprint.PrettyPrinter(indent=2).pprint
DEBUG = True

# users may not want all commands so top level is configurable
GIT_COMMANDS = {
    "clone",
    "init",
    "add",
    "mv",
    "reset",
    "rm",
    "bisect",
    "grep",
    "log",
    "show",
    "status",
    "branch",
    "checkout",
    "commit",
    "diff",
    "merge",
    "rebase",
    "tag",
    "fetch",
    "pull",
    "push",
}

# map components to speakable words
mappings = {
    "mv": "move",
    "rm": "remove",
    "dir": "directory",
    "git": "jet",
    "src": "source",
    "dst": "destination",
    "ext": "external",
    "abbrev": "abbreviate",
    "ff": "fast forward",
    "cr": "carriage return",
    "eol": "end of line",
}

reverse_mappings = {mappings[k]: k for k in mappings}


"""
Below runs on first execution only. Generates git.json
"""


def man(cmd):
    try:
        captured = check_output(["git", cmd, "--help"], universal_newlines=True)
        return captured
    except CalledProcessError as e:
        print("ERROR: ", e.output)


def get_opts(cmd):
    regexes = {
        "begin": r"(?:\n\n[ ]+|, )",
        "opt": r"(?:(?=\[[\w\-])\[|[\w\-\]])+",
        "arg": r"[\[= <]+.*?",
        "end": r"(?:(?:, -)|\n)",
    }
    manpage = (
        "\n\n"  # make first option prefix conform to others
        + man(cmd).split("\n\nO\x08OP\x08PT\x08TI\x08IO\x08ON\x08NS\x08S\n", 1)[1]
    )
    regex = r"{begin}(--{opt})({arg})?{end}".format(**regexes)

    options = re.findall(regex, manpage)

    list_groups = {}
    option_map = {}
    option_arg_strings = []
    for opt, raw_arg in options:
        if opt == "---":
            continue  # hack: regex needs fixing
        if "[" in opt:  # deal with --[no-]something type options
            opt = re.sub(r"[\[\]]", "", opt)
            opt_without_option = re.sub(r"\[.+?\]", "", opt)
            options.append((opt_without_option, raw_arg))
        clean_arg = re.sub(r"[ =<>\[\]\(\)\{\}]", "", raw_arg)
        arg_optional = True if "[" in raw_arg else False
        alternatives = []
        if "|" in clean_arg:
            for alternative in clean_arg.split("|"):
                mapped_alternative = " ".join(
                    [mappings.get(w, w) for w in alternative.split("-")]
                )
                option_map.update({mapped_alternative: alternative})
                alternatives.append(mapped_alternative)
        # build option
        opt_words = opt[2:].split("-")
        mapped_opt_words = [mappings.get(w, w) for w in opt_words]
        opt_string = " ".join(mapped_opt_words)
        # build argument
        arg_string = ""
        if clean_arg:
            if not alternatives:
                arg_string = "<dgndictation>"
            elif alternatives:
                listgroup_label = "".join(opt_words)
                list_groups.update({listgroup_label: alternatives})
                arg_string = "{{autogit.{}}}".format(listgroup_label)
            if arg_optional:
                arg_string = "[" + arg_string + "]"
        # assemble everything
        option_map[opt_string] = opt
        option_arg_strings.append(opt_string + " " + arg_string)

        if DEBUG:
            pp(
                {
                    "cmd": cmd,
                    "opt": opt,
                    "opt_arg_string": option_arg_strings[-1],
                    "raw_arg": raw_arg,
                    "clean_arg": clean_arg,
                    "arg_optional": arg_optional,
                    "alternatives": alternatives,
                }
            )

    talon_string = (
        mappings.get(cmd, cmd)
        + " ( "
        + " | ".join(option_arg_strings)
        + " )* [<dgndictation>] [over]"
    )
    return {"command": talon_string, "lists": list_groups, "options": option_map}


def build_git_file():
    out = {}
    length = 0
    for cmd in GIT_COMMANDS:
        talon_cmd = get_opts(cmd)
        # pp(talon_cmd)
        out[cmd] = talon_cmd
        length += len(talon_cmd["options"])
    with open(data_filepath, "w") as f:
        json.dump(out, f)
    return (out, length)


"""
Below generates keymap using git.json
"""


def load_git_data():
    try:
        with resource.open(data_filepath, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("autogit: creating git.json...")
        git_data, length = build_git_file()
        print("autogit: git.json created successfully (length {})".format(length))
        return git_data


def process(m):
    words = list(m._words)
    words.pop(0)  # jettison jet!
    cmd = words.pop(0)
    out = [cmd]
    last_option = []
    for word in words:
        if isinstance(word, Word):  # is option word
            last_option.append(reverse_mappings.get(word, word))
            try:
                option = git[cmd]["options"][" ".join(last_option)]
                out.append(option)
                last_option = []
            except KeyError as e:
                print(e)
        else:  # is dictation words
            for w in parse_words(list(word)):
                out.append(w)
    insert("git " + " ".join(out))


ctx = Context("autogit")

git = load_git_data()

keymap = {}

for cmd, data in git.items():
    for listgroup_label, listgroup in data["lists"].items():
        ctx.set_list(listgroup_label, listgroup)
    keymap.update({"jet " + data["command"]: process})

if DEBUG:
    print("autogit keymap:", keymap)

ctx.keymap(keymap)

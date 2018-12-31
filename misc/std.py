"""
Since this file is called std, it may be tempting to dump more stuff here.
Ideally, put any new commands in another file, so that related ones are grouped
together, and files don't get massive.
"""

import os

from talon.voice import Word, Context, Key, Rep, RepPhrase, Str, press
from talon import ctrl, clip

ctx = Context("input")

ctx.keymap(
    {
        "trough": Key("alt-backspace"),
        "slap": [Key("cmd-right enter")],
        "sky shock": Key("shift-enter"),
        "ricky": Key("ctrl-e"),
        "lefty": Key("ctrl-a"),
        "olly | ali": Key("cmd-a"),
        "(dot dot | dotdot)": "..",
        "(dot dot dot | dotdotdot)": "...",
        "run (them | vim)": "vim ",
        "dot pie": ".py",
        "const": "const ",
        "static": "static ",
        "tip pent": "int ",
        "tip char": "char ",
        "tip byte": "byte ",
        "tip float": "float ",
        "tip double": "double ",
        "args": ["()", Key("left")],
        "index": ["[]", Key("left")],
        "block": [" {}", Key("left enter enter up tab")],
        "empty array": "[]",
        "empty dict": "{}",
        "state (def | deaf | deft)": "def ",
        "state if": "if ",
        "state else if": [" else if ()", Key("left")],
        "state while": ["while ()", Key("left")],
        "state for": "for ",
        "state switch": ["switch ()", Key("left")],
        "state case": ["case \nbreak;", Key("up")],
        "state import": "import ",
        "state class": "class ",
        "comment see": "// ",
        "comment py": "# ",
        "word queue": "queue",
        "word eye": "eye",
        "word bson": "bson",
        "word iter": "iter",
        "word no": "NULL",
        "word cmd": "cmd",
        "word dup": "dup",
        "word streak": ["streq()", Key("left")],
        "word printf": "printf",
        "word (dickt | dictionary)": "dict",
        "word shell": "shell",
        "word talon": "talon",
        "dunder in it": "__init__",
        "self taught": "self.",
        "dickt in it": ["{}", Key("left")],
        "list in it": ["[]", Key("left")],
        "string utf8": "'utf8'",
        "state past": "pass",
        "call": "()",
        "shebang bash": "#!/bin/bash -u\n",
        "new window": Key("cmd-n"),
        "next window": Key("cmd-`"),
        "last window": Key("cmd-shift-`"),
        "next app": Key("cmd-tab"),
        "last app": Key("cmd-shift-tab"),
        "next tab": Key("cmd-shift-]"),
        "new tab": Key("cmd-t"),
        "(last | prevous | preev) tab": Key("cmd-shift-["),
        "next space": Key("cmd-alt-ctrl-right"),
        "last space": Key("cmd-alt-ctrl-left"),
        "scroll down": [Key("down")] * 30,
        "scroll up": [Key("up")] * 30,
        "(marco | search)": Key("cmd-f"),
        "marneck": Key("cmd-g"),
        "marpreev": Key("cmd-shift-g"),
        "marthis": [
            Key("alt-right"),
            Key("shift-alt-left"),
            Key("cmd-f"),
            Key("enter"),
        ],
        "launcher": Key("cmd-space"),
        "prefies": Key("cmd-,"),
        "put computer to sleep": lambda m: os.system("pmset sleepnow"),
    }
)

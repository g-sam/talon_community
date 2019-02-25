# Works with forked version of commando to enable display of only activated
# contexts. Run https://github.com/g-sam/commando/tree/add-filter and
# navigate to http://127.0.0.1:6001/?filter=activated_contexts

from talon import ui, voice
from talon.engine import engine

voice.talon.activated = set()

def ui_event(event, arg):
    voice.talon.activated.update(voice.talon.active)

ui.register('', ui_event)

"""Espanso matches (neutral ones; put personal/work snippets in match/private.yml, not in git) whose triggers work in the en / uk / ru layouts: the same physical keys in each layout."""
import io
import os

import yaml

EN = "qwertyuiop[]asdfghjkl;'zxcvbnm,./"
UK = "йцукенгшщзхїфівапролджєячсмитьбю."
RU = "йцукенгшщзхъфывапролджэячсмитьбю."
SHIFT = {':': 'Ж'}  # Shift+; in the Cyrillic layouts


def on_layout(trigger, table):
    out = []
    for ch in trigger:
        if ch in SHIFT:
            out.append(SHIFT[ch])
        elif ch in EN:
            out.append(table[EN.index(ch)])
        else:
            out.append(ch)
    return ''.join(out)


def triggers(t):
    return sorted({t, on_layout(t, UK), on_layout(t, RU)})


matches = [
    {'triggers': triggers(':date'), 'replace': '{{d}}', 'vars': [{'name': 'd', 'type': 'date', 'params': {'format': '%d.%m.%Y'}}]},
    {'triggers': triggers(':time'), 'replace': '{{t}}', 'vars': [{'name': 't', 'type': 'date', 'params': {'format': '%H:%M'}}]},
]
head = ("# Snippets for documents (22.11.2026). Type the keys of ':date' etc. in any layout (en/uk/ru):\n"
        "# in the Cyrillic layouts the same keys print as Жвфеу, and that works too.\n"
        "# Add your own below: copy a block, change the trigger after the colon and the text.\n")
base = os.path.join(os.path.expanduser('~'), 'scoop', 'persist', 'espanso', '.espanso')  # Scoop = portable mode
os.makedirs(os.path.join(base, 'match'), exist_ok=True)
os.makedirs(os.path.join(base, 'config'), exist_ok=True)
io.open(os.path.join(base, 'match', 'base.yml'), 'w', encoding='utf-8', newline='\n').write(
    head + yaml.safe_dump({'matches': matches}, allow_unicode=True, sort_keys=False, width=200))
cfg = os.path.join(base, 'config', 'default.yml')
if not os.path.exists(cfg):
    io.open(cfg, 'w', encoding='utf-8', newline='\n').write(
        "# Alt+Space belongs to Flow Launcher\nsearch_shortcut: off\nshow_notifications: false\n")
for m in matches:
    print(m['triggers'], '->', m['replace'])

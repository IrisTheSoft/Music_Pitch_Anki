import dataclasses as DC
import pathlib as PTH
import typing as TP

import jinja2 as JJ


media_path = PTH.Path("output")


@DC.dataclass
class Clef:
    name: str
    sharps: TP.List[int]
    flats: TP.List[int]


treble_clef = Clef("G", [-4, -1, -5, -2, 1, -3, 0], [0, -3, 1, -2, 2, -1, 3])
bass_clef = Clef("F", [-2, 1, -3, 0, 3, -1, 2], [2, -1, 3, 0, 4, 1, 5])


with open("media.svg.jinja") as media_template_file:
    media_template = JJ.Template(media_template_file.read())


def generate_media(file_name, clef, signature_count, note, accidental):
    if signature_count > 0:
        signature_kind = "sharp"
        signature = clef.sharps[:signature_count]
    elif signature_count < 0:
        signature_kind = "flat"
        signature = clef.flats[:-signature_count]
    else:
        signature_kind = "empty"
        signature = []
    with open(media_path/f"{file_name}.svg", "w") as file:
        file.write(media_template.render({
            "clef": clef.name,
            "signature_kind": signature_kind,
            "signature": signature,
            "note": note,
            "accidental": accidental,
            "enumerate": enumerate,
            "list": list,
            "sign": lambda x: 1 if x >= 0 else -1}))

import dataclasses as DC
import pathlib as PTH
import typing as TP

import jinja2 as JJ


media_path = PTH.Path("output")


@DC.dataclass
class Clef:
    name: str
    offset: int
    sharps: TP.List[int]
    flats: TP.List[int]


treble_clef = Clef("G", 6, [-4, -1, -5, -2, 1, -3, 0], [0, -3, 1, -2, 2, -1, 3])
bass_clef = Clef("F", -6, [-2, 1, -3, 0, 3, -1, 2], [2, -1, 3, 0, 4, 1, 5])

note_names = ["do", "re", "mi", "fa", "sol", "la", "si"]


with open("media.svg.jinja") as media_template_file:
    media_template = JJ.Template(media_template_file.read())


def split_signature(clef, signature_count):
    if signature_count > 0:
        return clef.sharps[:signature_count]
    elif signature_count < 0:
        return clef.flats[:-signature_count]
    else:
        return []


def generate_answer(clef, signature_count, note_position, accidental):
    note = clef.offset - note_position
    signature = [(clef.offset - signature_note) % 7 for signature_note
                 in split_signature(clef, signature_count)]
    if note % 7 not in signature:
        semitone = {"flat": " b", "sharp": " #", None: ""}[accidental]
    elif accidental == "natural":
        semitone = ""
    elif accidental == "flat" or signature_count < 0:
        semitone = " b"
    elif accidental == "sharp" or signature_count > 0:
        semitone = " #"
    return f"{note_names[note % 7].title()}{semitone} {4 + note // 7}"


def generate_media(file_name, clef, signature_count, note_position, accidental):
    if signature_count > 0:
        signature_kind = "sharp"
    elif signature_count < 0:
        signature_kind = "flat"
    else:
        signature_kind = "empty"
    signature = split_signature(clef, signature_count)
    print(generate_answer(clef, signature_count, note_position, accidental))
    with open(media_path/f"{file_name}.svg", "w") as file:
        file.write(media_template.render({
            "clef": clef.name,
            "signature_kind": signature_kind,
            "signature": signature,
            "note": note_position,
            "accidental": accidental,
            "enumerate": enumerate,
            "list": list,
            "sign": lambda x: 1 if x >= 0 else -1}))

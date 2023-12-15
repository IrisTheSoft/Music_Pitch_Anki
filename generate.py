import dataclasses as DC
import itertools as ITR
import pathlib as PTH
import random as RND
import typing as TP

import jinja2 as JJ
import genanki as GANKI


media_path = PTH.Path("output")


note_names = ["do", "re", "mi", "fa", "sol", "la", "si"]


@DC.dataclass
class Clef:
    name: str
    offset: int
    sharps: TP.List[int]
    flats: TP.List[int]


treble_clef = Clef("G", 6, [-4, -1, -5, -2, 1, -3, 0], [0, -3, 1, -2, 2, -1, 3])
bass_clef = Clef("F", -6, [-2, 1, -3, 0, 3, -1, 2], [2, -1, 3, 0, 4, 1, 5])


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
        semitone = {"flat": " b", "sharp": " &num;", None: ""}[accidental]
    elif accidental == "natural":
        semitone = ""
    elif accidental == "flat" or signature_count < 0:
        semitone = " b"
    elif accidental == "sharp" or signature_count > 0:
        semitone = " &num;"
    return f"{note_names[note % 7].title()}{semitone} {4 + note // 7}"


def generate_media(clef, signature_count, note_position, accidental):
    if signature_count > 0:
        signature_kind = "sharp"
    elif signature_count < 0:
        signature_kind = "flat"
    else:
        signature_kind = "empty"
    return media_template.render({
        "clef": clef.name,
        "signature_kind": signature_kind,
        "signature": split_signature(clef, signature_count),
        "note": note_position,
        "accidental": accidental,
        "enumerate": enumerate,
        "list": list,
        "sign": lambda x: 1 if x >= 0 else -1})

def generate_note(deck, model, clef, signature_count, note_position, accidental):
    deck.add_note(GANKI.Note(model, [
        generate_answer(clef, signature_count, note_position, accidental),
        generate_media(clef, signature_count, note_position, accidental)]))


with open("media.svg.jinja") as media_template_file:
    media_template = JJ.Template(media_template_file.read())
with open("style.css") as css_file:
    css = css_file.read()

def main():
    deck = GANKI.Deck(1695354595, "Solfège")
    model = GANKI.Model(1446643112, "Musical Pitch",
                        [{"name": "Answer"}, {"name": "Image"}],
                        [{
                            "name": "Pitch reading",
                            "qfmt": "{{Image}}",
                            "afmt": "{{FrontSide}}<hr/>{{Answer}}"
                        }], css)


    for clef, signature_count, note_position \
     in ITR.product([treble_clef, bass_clef], range(-7, 8), range(-12, 13)):
        note = clef.offset - note_position
        signature = [(clef.offset - signature_note) % 7 for signature_note
                    in split_signature(clef, signature_count)]
        generate_note(deck, model, clef, signature_count, note_position, None)
        if note % 7 in signature:
            generate_note(deck, model, clef, signature_count, note_position, "natural")
        else:
            generate_note(deck, model, clef, signature_count, note_position, "flat")
            generate_note(deck, model, clef, signature_count, note_position, "sharp")
    GANKI.Package(deck).write_to_file("music_pitch.apkg")


if __name__ =="__main__":
    main()

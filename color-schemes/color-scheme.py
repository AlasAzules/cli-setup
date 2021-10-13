import re
from os import path
from argparse import ArgumentParser
from enum import IntEnum

NAME_COLOR_PATTERN = re.compile(r"[\s'\"]*(\w+)[\s'\":=]+(#[A-Za-z0-9]{6})")
NAME_COLOR_PATTERN = re.compile(r"[\s'\"]*(\w+)[\s'\":=]+(#[A-Za-z0-9]{6}|\d{1,3},\s?\d{1,3},\s?\d{1,3})")
COLOR_CODE_PATTERN = re.compile(r"#?([A-Za-z0-9]{6})")
COLOR_DIGITS_PATTERN = re.compile(r"(\d{1,3}),\s?(\d{1,3}),\s?(\d{1,3})")

class SchemeType(IntEnum):
    def __new__(cls, value, ext, description):
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.ext = ext
        obj.description = description
        return obj
    
    Mintty = 0, ".mintty", "Mintty" # 255,255,255
    Cmder = 1, ".xml", "Cmder"

def color_code_to_digits(color_code):
    m = COLOR_CODE_PATTERN.match(color_code)
    if m:
        color = int(m.group(1), base=16)
        return tuple((color >> i) & 0xFF for i in range(16, -1, -8))

def color_digits_to_code(color_digits):
    return "#{:X}{:X}{:X}".format(*color_digits)

def color_digits_to_str(color_digits):
    return "{},{},{}".format(*color_digits)

def color_digits_str_to_digits(digits_str):
    m = COLOR_DIGITS_PATTERN.match(digits_str)
    if m:
        print(m.groups())
        return tuple((int(s) for s in m.groups()))

def parse_color_map(file_handle):
    color_map = {}
    for line in file_handle:
        m = NAME_COLOR_PATTERN.match(line)
        if m:
            name, color = m.groups()
            digits = color_code_to_digits(color) or color_digits_str_to_digits(color)
            color_map[name] = digits
    return color_map

def save_color_map(color_map: dict, fname, scheme_type: SchemeType):
    if scheme_type == SchemeType.Mintty:
        ff = color_digits_to_str
        fmt = "{}={}\n"
    if scheme_type == SchemeType.Cmder:
        ff = color_digits_to_code
        fmt = "{} {}\n"
    with open(fname, "w", encoding="utf-8") as fh:
        for name, color in color_map.items():
            # fh.write(f"{name} {ff(color)}\n")
            fh.write(fmt.format(name, ff(color)))

def get_parser():
    parser = ArgumentParser()
    parser.add_argument("input", help="Input file")
    parser.add_argument("-o", "--output", default=None)
    parser.add_argument("-t", "--scheme-type", default=SchemeType.Mintty.value, type=int, help="Output scheme type")
    return parser

def main(args):
    with open(args.input, "r", encoding="utf-8") as fh:
        ofname = args.output if args.output is not None else args.input + ".out"
        color_map = parse_color_map(fh)
        print(color_map)
        print(f"save file: {ofname}")

def cli():
    parser = get_parser()
    args = parser.parse_args()
    main(args)

def test():
    text = '''    "brightYellow" : "#F9F1A5",'''
    text = '''    "brightYellow"  "#F9F1A5",'''
    text = '''    "brightYellow"  "249, 241, 165",'''
    r = NAME_COLOR_PATTERN.match(text)
    if r:
        for item in r.groups():
            print(item)
        color = r.group(2)
        digits = color_code_to_digits(color) or color_digits_str_to_digits(color)
        print(digits)
        print(color_digits_to_code(digits))
        print(color_digits_to_str(digits))

def test2():
    fname = r"F:\work_space\cli-setup\color-schemes\color-schemes.json"
    ofname = r"F:\work_space\cli-setup\color-schemes\color-schemes.txt"
    with open(fname, "r", encoding="utf-8") as fh:
        color_map = parse_color_map(fh)
        print(color_map)
        save_color_map(color_map, ofname, SchemeType.Mintty)

if __name__ == "__main__":
    # cli()
    test2()
# 奇怪0 'Hack NF', 'DejaVu Sans Mono',

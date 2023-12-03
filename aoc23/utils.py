from pathlib import Path
here = Path(__file__)


def inputs(filename):
    return here.parent / "inputs" / filename


def examples(filename):
    return here.parent / "examples" / filename


def display_field(field):
    """Display a rectangular field of chars. Nan (or any float) replaced with ` `"""
    out = []
    for ix in range(field.shape[0]):
        out.append("\n")
        for jx in range(field.shape[1]):
           if isinstance(field[jx][ix], float):
              c = " "
           else:
              c = field[jx][ix]
           out.append(c)
    print("".join(out))


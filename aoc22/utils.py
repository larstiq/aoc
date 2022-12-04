from pathlib import Path
here = Path(__file__)


def inputs(filename):
    return here.parent / "inputs" / filename


def examples(filename):
    return here.parent / "examples" / filename

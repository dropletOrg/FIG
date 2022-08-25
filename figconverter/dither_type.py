from enum import Enum


class DitherType(Enum):
    FLOYDSTEINBERG: str = 'floyd_steinberg'
    BAYER: str = 'bayer'
from base import Base
from enum import Enum, auto


class DivisionType(Enum):
    Beats = auto()
    SMPTE = auto()


class Division(Base):
    def __init__(self, division_type, ticks=500000, smpte_format=-24, resolution=4):
        self.division         = division_type
        self.beats_ticks      = beats_ticks
        self.smpte_format     = smpte_format
        self.smpte_resolution = smpte_resolution

    def data(self):
        match self.divison:
            case Beats:
                return (0x0000).to_bytes(2, 'big') | self.beats_ticks
            case SMPTE:
                byte = (0x8000).to_bytes(2, 'big') |
                       (smpte_format.to_bytes(2, 'big') << 7) |
                        smpte_resolution.to_bytes(2, 'big')


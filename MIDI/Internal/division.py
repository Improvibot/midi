from MIDI.Internal.base import Base
from enum import Enum, auto
import logging


class DivisionType(Enum):
    Beats = auto()
    SMPTE = auto()


class Division(Base):
    def __init__(self, division_type, beats_ticks=128, smpte_format=-24, smpte_resolution=4):
        super().__init__()
        self.division = division_type
        self.beats_ticks = beats_ticks
        self.smpte_format = smpte_format
        self.smpte_resolution = smpte_resolution

    def data(self):
        match self.division:
            case DivisionType.Beats:
                b = (0x0000 | self.beats_ticks)
            case DivisionType.SMPTE:
                b = (0x8000 | ((smpte_format << 7) + smpte_resolution))
        logging.info(f'Division: {b.to_bytes(2, "big").hex(" ").upper()}')
        return b.to_bytes(2, 'big')

    def encode(self):
        return self.data()

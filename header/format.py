from base import Base
from enum import Enum


class FormatType(Enum):
    SingleTrack = 0
    MultiTrack = 1
    IndependentTracks = 2

class Format(Base):
    def __init__(self, format_type):
        self.format = format_type

    def data(self):
        return self.format.value.to_bytes(2, 'big')

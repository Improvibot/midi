from enum import Enum, auto


class Encoding(Enum):
    MIDI = auto()
    JACK = auto()


class Base:
    def __init__(self, timestamp=0, include_data_length=False):
        self._event_code = b''
        if type(timestamp) == 'bytes':
            self.timestamp = timestamp
        else:
            self.timestamp = timestamp.to_bytes(self.length(timestamp))
        self.include_data_length = include_data_length

    def data(self):
        raise NotImplementedError

    def event_code(self):
        if (self._event_code == b''):
            raise NotImplementedError
        else:
            return self._event_code

    def encode(self, encoding, ticks=500000, bpm=120, sample_rate=44100):
        if encoding == Encoding.MIDI:
            ts = self.timestamp
        else:
            ts = b''

        if self.include_data_length:
            dl = len(self.data()).to_bytes()
        else:
            dl = b''

        return ts + self.event_code() + dl + self.data()

    # Returns the length of the message in bytes, used for MIDI files where tracks
    #    have to report total length
    def size(self):
        return len(self.encode(Encoding.MIDI))

    def length(self, value):
        return 1 if value == 0 else ((value.bit_length() + 7) // 8)

    def size_to_bytes(self, value):
        return value.to_bytes(length=self.length(value))

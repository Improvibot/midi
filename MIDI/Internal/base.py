from MIDI.Internal.encoding import Encoding
from MIDI.Internal.timestamp import TimeStamp


class Base:
    def __init__(self, timestamp=TimeStamp(1, 1), include_data_length=False):
        self._event_code = b''
        self.timestamp = timestamp
        self.include_data_length = include_data_length

    def __str__(self):
        return f'{type(self).__name__}\t{self.data().hex(" ").upper()}'

    def data(self):
        raise NotImplementedError

    def event_code(self):
        if (self._event_code == b''):
            raise NotImplementedError
        else:
            return self._event_code

    def encode(self, encoding, prior_timestamp, time_sig, ticks=128, bpm=120, sample_rate=44100):
        if encoding == Encoding.MIDI:
            ts = self.size_to_bytes(self.timestamp.to_midi_ticks(
                ticks, prior_timestamp, time_sig))
        else:
            ts = b''

        if self.include_data_length:
            dl = len(self.data()).to_bytes()
        else:
            dl = b''

        return ts + self.event_code() + dl + self.data()

    # Returns the length of the message in bytes, used for MIDI files where tracks
    #    have to report total length
    # def size(self):
    #    return len(self.encode(Encoding.MIDI))

    def length(self, value):
        return 1 if value == 0 else ((value.bit_length() + 7) // 8)

    def size_to_bytes(self, value):
        return value.to_bytes(self.length(value), 'big')

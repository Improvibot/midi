from MIDI.Internal import Base, Encoding, TimeStamp


class Message(Base):
    def __init__(self, timestamp=TimeStamp(1, 1), include_data_length=False):
        super().__init__(timestamp, include_data_length)
        self._event_code = b''

    def data(self):
        return NotImplementedError

    def get_note_length(self, encoding, ticks, bpm, sample_rate):
        if encoding == Encoding.MIDI:
            return ticks * self.time
        else:
            # JACK
            return (sample_rate / bpm) * self.time


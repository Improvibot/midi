from MIDI.Message.Template import MetaMessage
from MIDI.Internal         import TimeStamp


class TimeSignature(MetaMessage):
    def __init__(self, timestamp=TimeStamp(1, 1), num_beats=4, beat_note=4, clocks=0, num_32nd_notes=24):
        super().__init__(timestamp)
        self._event_code = bytes.fromhex('FF 58 04')
        self.num_beats = num_beats.to_bytes(1, 'big')
        self.beat_note = beat_note.to_bytes(1, 'big')
        self.clocks = clocks.to_bytes(1, 'big')
        self.num_32nd_notes = num_32nd_notes.to_bytes(1, 'big')

    def data(self):
        return self.num_beats + \
            self.beat_note + \
            self.clocks + \
            self.num_32nd_notes

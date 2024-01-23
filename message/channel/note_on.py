from MIDI.message.internal import ChannelMessage


class NoteOn(ChannelMessage):
    def __init__(self, timestamp=0, channel=0, note=0, velocity=0):
        super().__init__(timestamp, channel)
        self._event_code = bytes.fromhex('90')
        self.note = note.to_bytes(1, 'big')
        self.velocity = velocity.to_bytes(1, 'big')

    def data(self):
        return self.note + self.velocity

from MIDI.Message.Template import ChannelMessage


class NoteOff(ChannelMessage):
    def __init__(self, timestamp, channel, note, velocity):
        super().__init__(timestamp, channel)
        self._event_code = (0x80).to_bytes(1, 'big')
        self.note = note.to_bytes(1, 'big')
        self.velocity = velocity.to_bytes(1, 'big')

    def data(self):
        return self.note + self.velocity

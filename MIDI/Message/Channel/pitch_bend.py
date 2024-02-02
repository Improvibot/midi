from MIDI.Message.Template import ChannelMessage


class PitchBend(ChannelMessage):
    def __init__(self, timestamp, channel, value):
        super().__init__(timestamp, channel)
        self._event_code = (0xE0).to_bytes(1, 'big')
        self.value = value.to_bytes(2, 'big')

    def data(self):
        return self.value

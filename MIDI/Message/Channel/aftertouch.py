from MIDI.Message.Template import ChannelMessage


class Aftertouch(ChannelMessage):
    def __init__(self, timestamp, channel, velocity):
        super().__init__(timestamp, channel)
        self._event_code = (0xD0).to_bytes(1, 'big')
        self.velocity = velocity.to_bytes(1, 'big')

    def data(self):
        return self.velocity

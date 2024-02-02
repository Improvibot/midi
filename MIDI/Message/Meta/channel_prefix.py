from MIDI.Message.Template import MetaMessage
from MIDI.Internal         import TimeStamp

# channel should be a value between 0 & 15


class ChannelPrefix(MetaMessage):
    def __init__(self, timestamp=TimeStamp(1, 1), channel=0):
        super().__init__(timestamp)
        self._event_code = bytes.fromhex('FF2001')
        self.channel = channel.to_bytes(1, 'big')

    def data(self):
        return self.channel

from MIDI.Internal import Base, Encoding, TimeStamp
from MIDI.Message.Template import Message


class ChannelMessage(Message):
    def __init__(self, timestamp=TimeStamp(1, 1), channel=0):
        super().__init__(timestamp)
        self._event_code = b''
        self.channel = channel.to_bytes()

    def event_code(self):
        return (self._event_code[0] | self.channel[0]).to_bytes(1, 'big')

    def data(self):
        raise NotImplementedError

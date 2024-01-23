from MIDI.base import Base, Encoding


class Message(Base):
    def __init__(self, timestamp=0, include_data_length=False):
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


class ChannelMessage(Message):
    def __init__(self, timestamp=0, channel=0):
        super().__init__(timestamp)
        self._event_code = b''
        self.channel = channel.to_bytes()

    def event_code(self):
        return (self._event_code[0] | self.channel[0]).to_bytes(1, 'big')

    def data(self):
        raise NotImplementedError


class MetaMessage(Message):
    def __init__(self, timestamp=0, include_data_length=False):
        super().__init__(timestamp, include_data_length)
        self._event_code = b''
        self.include_data_length = include_data_length

    def data(self):
        raise NotImplementedError


class MetaTextMessage(Message):
    def __init__(self, timestamp=0, text=''):
        super().__init__(timestamp, include_data_length=True)
        self._event_code = b''
        self.text = bytes(text, 'ascii')

    def data(self):
        return self.text
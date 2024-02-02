from MIDI.Internal import Base, Encoding, TimeStamp
from MIDI.Message.Template import Message


class MetaTextMessage(Message):
    def __init__(self, timestamp=TimeStamp(1, 1), text=''):
        super().__init__(timestamp, include_data_length=True)
        self._event_code = b''
        self.text = bytes(text, 'ascii')

    def data(self):
        return self.text

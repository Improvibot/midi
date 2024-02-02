from MIDI.Internal import Base, Encoding, TimeStamp
from MIDI.Message.Template import Message


class MetaMessage(Message):
    def __init__(self, timestamp=TimeStamp(1, 1), include_data_length=False):
        super().__init__(timestamp, include_data_length)
        self._event_code = b''
        self.include_data_length = include_data_length

    def data(self):
        raise NotImplementedError

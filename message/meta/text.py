from MIDI.message.internal import MetaTextMessage
from MIDI.timestamp import TimeStamp


class Text(MetaTextMessage):
    def __init__(self, timestamp=TimeStamp(1, 1), text=''):
        super().__init__(timestamp, text)
        self._event_code = bytes.fromhex('FF 01')

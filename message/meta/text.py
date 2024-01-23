from MIDI.message.internal import MetaTextMessage


class Text(MetaTextMessage):
    def __init__(self, timestamp=0, text=''):
        super().__init__(timestamp, text)
        self._event_code = bytes.fromhex('FF 01')

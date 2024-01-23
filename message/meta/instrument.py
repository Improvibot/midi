from MIDI.message.internal import MetaTextMessage


class Instrument(MetaTextMessage):
    def __init__(self, timestamp=0, text=''):
        super().__init__(timestamp, text)
        self._event_code = bytes.fromhex('FF 04')
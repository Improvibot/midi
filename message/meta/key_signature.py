from MIDI.message.internal import MetaMessage
from MIDI.timestamp        import TimeStamp


class KeySignature(MetaMessage):
    def __init__(self, timestamp=TimeStamp(1, 1), sharps_flats=0, major_minor=0):
        super().__init__(timestamp)
        self._event_code = bytes.fromhex('FF 59 02')
        self.sharps_flats = sharps_flats.to_bytes(1, 'big', signed=True)
        self.major_minor = major_minor.to_bytes(1, 'big')

    def data(self):
        return self.sharps_flats + \
            self.major_minor

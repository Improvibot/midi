from MIDI.Message.Template import MetaMessage
from MIDI.Internal         import TimeStamp


class SMPTE(MetaMessage):
    def __init__(self, timestamp=TimeStamp(1, 1), hour=0, minute=0, second=0, frame=0, frame_fraction=0):
        super().__init__(timestamp)
        self._event_code = bytes.fromhex('FF 54 05')
        self.hour = hour.to_bytes(1, 'big')
        self.minute = minute.to_bytes(1, 'big')
        self.second = second.to_bytes(1, 'big')
        self.frame = frame.to_bytes(1, 'big')
        self.frame_fraction = frame_fraction.to_bytes(1, 'big')

    def data(self):
        return self.hour + \
            self.minute + \
            self.second + \
            self.frame + \
            self.frame_fraction

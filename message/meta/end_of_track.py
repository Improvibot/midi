from MIDI.message.internal import MetaMessage
from MIDI.timestamp        import TimeStamp


class EndOfTrack(MetaMessage):
    def __init__(self, timestamp=TimeStamp(1, 1)):
        super().__init__(timestamp)
        self._event_code = bytes.fromhex('FF2F00')

    # Return empty, as there is no data associated with
    #    this message.
    def data(self):
        return b''

from MIDI.Message.Template import MetaMessage
from MIDI.Internal         import TimeStamp


class Tempo(MetaMessage):
    def __init__(self, timestamp=TimeStamp(1, 1), tempo=120):
        super().__init__(timestamp)
        self._event_code = bytes.fromhex('FF 51 03')
        self.tempo = tempo.to_bytes(3, 'big')

    def data(self):
        return self.tempo

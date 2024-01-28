# Note: TrackName and SequenceName create the same MIDI message.
#       They have separate classes purely for the ease of the end user,
#       so that they can use TrackName when dealing with MIDI file types 0 & 1
#       and SequenceName when dealing with MIDI file type 2.

from MIDI.message.internal import MetaTextMessage
from MIDI.timestamp        import TimeStamp


class SequenceName(MetaTextMessage):
    def __init__(self, timestamp=TimeStamp(1, 1), text=''):
        super().__init__(timestamp, text)
        self._event_code = bytes.fromhex('FF 03')

# Note: TrackNumber and SequenceNumber create the same MIDI message.
#       They have separate classes purely for the ease of the end user,
#       so that they can use TrackNumber when dealing with MIDI file types 0 & 1
#       and SequenceNumber when dealing with MIDI file type 2.

# TODO: Sequence #'s must start at the beginning of the track.  This means
#       that the timestamp must be zero, though the message does not have
#       to be the very first message in the track.  Must write logic that
#       creates an error if timestamp != 0.

from MIDI.message.internal import MetaMessage


class SequenceNumber(MetaMessage):
    def __init__(self, timestamp=0, seq_num=1):
        super().__init__(timestamp)
        self._event_code = bytes.fromhex('FF 00 02')
        self.sequence_number = seq_num.to_bytes(2, 'big')

    def data(self):
        return self.sequence_number
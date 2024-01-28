from MIDI.base import Base, Encoding
from MIDI.timestamp import TimeStamp, TimeSig
from functools import reduce, partial
from itertools import pairwise


class Track(Base):
    def __init__(self):
        self.messages = []

    def append(self, message):
        self.messages.append(message)

    def extend(self, encoding, time_sig, ticks, messages, message):
        prior_message = message[0]
        current_message = message[1]
        messages.extend(current_message.encode(
            Encoding.MIDI, prior_message.timestamp, time_sig, ticks))
        return messages

    def encode(self, encoding=Encoding.MIDI, time_sig=TimeSig(4, 4), ticks=500000, bpm=120, sample_rate=44100):
        extend = partial(self.extend, encoding, time_sig, ticks)
        message_bytes = reduce(extend,
                               pairwise(self.messages),
                               bytearray(self.messages[0].encode(encoding,
                                                                 TimeStamp(
                                                                     1, 1),
                                                                 time_sig)
                                         )
                               )
        return bytes('MTrk', 'ascii') + len(message_bytes).to_bytes(4, 'big') + message_bytes

    def size(self):
        return reduce((lambda x, message: x + message.size()), self.messages, 0)

from MIDI.Internal import Base, Encoding, TimeStamp, TimeSignature
from functools import reduce, partial
from itertools import pairwise


class Track(Base):
    def __init__(self):
        self.messages = []

    def __repr__(self):
        response = f'Track\t['
        for message in self.messages:
            response += '\n\t\t' + message.__repr__()
        response += '\n\t]'
        return response
    
    def append(self, message):
        self.messages.append(message)

    def extend(self, encoding, time_sig, ticks, messages, message):
        prior_message = message[0]
        current_message = message[1]
        messages.extend(current_message.encode(
            Encoding.MIDI, prior_message.timestamp, time_sig, ticks))
        return messages

    def encode(self, encoding=Encoding.MIDI, time_sig=TimeSignature(4, 4), ticks=128, bpm=120, sample_rate=44100):
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

    def data(self):
        return self.encode()

    def size(self):
        return reduce((lambda x, message: x + message.size()), self.messages, 0)

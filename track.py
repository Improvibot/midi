from MIDI.base import Base, Encoding
from functools import reduce
import logging


class Track(Base):
    def __init__(self):
        self.messages = []

    def append(self, message):
        self.messages.append(message)

    def extend(self, messages, message):
        # logging.info(f'Messages: {messages}')
        # logging.info(f'Message:  {message}')
        messages.extend(message.encode(Encoding.MIDI))
        return messages

    def encode(self, encoding, ticks=500000, bpm=120, sample_rate=44100):
        message_bytes = reduce(self.extend, self.messages, bytearray())
        return bytes('MTrk', 'ascii') + self.size().to_bytes(4, 'big') + message_bytes

    def size(self):
        return reduce((lambda x, message: x + message.size()), self.messages, 0)

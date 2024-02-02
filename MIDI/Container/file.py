from functools import reduce
from MIDI.Message import *
import MIDI.Internal as internal
from MIDI.Internal import Base, Encoding, Format, Division, DivisionType, TimeStamp
import logging


class File(Base):
    def __init__(self, filename='',
                 asynchronous=False,
                 division_type=DivisionType.Beats,
                 ticks=128,
                 bpm=120,
                 time_signature=internal.TimeSignature(4, 4),
                 sample_rate=44100,
                 smpte_format=-24,
                 smpte_resolution=4):
        if not filename == '':
            self.filename = filename
            self.load(filename)
        else:
            self.asynchronous = asynchronous
            # self.format      = Format(format_type)
            if division_type == DivisionType.Beats:
                self.division = Division(division_type, beats_ticks=ticks)
            else:  # division_type = DivisionType.SMPTE
                self.division = Division(
                    division_type, smpte_format=smpte_format, smpte_resolution=smpte_resolution)
            self.tracks = []
            self.ticks = ticks
            self.time_signature = time_signature
            self.bpm = bpm
            self.sample_rate = sample_rate

    def append_track(self, track):
        self.tracks.append(track)

    def set_ticks(self, ticks):
        self.ticks = ticks

    def set_bpm(self, bpm):
        self.bpm = bpm

    def set_sample_rate(self, sample_rate):
        self.sample_rate = sample_rate

    # 14 = header size, 4 bytes for 'MThd', 4 for header length, and 6 for the data
    def size(self):
        return reduce(lambda x, track: x + track.size(), tracks, 14)
        pass

    def encode(self, encoding):
        if (encoding == Encoding.MIDI):

            return reduce(lambda x, track:
                          # logging.info(
                          #    f'x: {x}\ttrack: {track.encode(encoding=Encoding.MIDI, time_sig=self.time_signature, ticks=self.ticks)}'),
                          x + track.encode(encoding=Encoding.MIDI,
                                           time_sig=self.time_signature, ticks=self.ticks),
                          # x.join(track.encode(encoding=Encoding.MIDI,
                          #                    time_sig=self.time_signature,
                          #                    ticks=self.ticks
                          #                    )
                          #       ),
                          self.tracks,
                          self.encode_header()
                          )
        else:
            return reduce(lambda x, track:
                          x.join(track.encode(encoding=Encoding.JACK,
                                              time_sig=self.time_signature,
                                              bpm=self.bpm,
                                              sample_rate=self.sample_rate
                                              )
                                 ),
                          self.tracks,
                          b''
                          )

    def encode_header(self):
        def select_format():
            if self.asynchronous:
                format = 2
            else:
                if len(self.tracks) > 1:
                    format = 1
                else:
                    format = 0
            logging.info(
                f'Format: {format.to_bytes(2, "big").hex(" ").upper()}')
            return format.to_bytes(2, 'big')
        return b'MThd' + (6).to_bytes(4, 'big') + select_format() + len(self.tracks).to_bytes(2, 'big') + self.division.encode()
        # + self.format.encode()

    def load(self, filename):
        pass

    def save(self, filename=''):
        f = filename if filename[:-4] == '.mid' else filename + '.mid'
        with open(f, 'wb') as fn:
            fn.write(self.encode(Encoding.MIDI))

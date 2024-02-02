import logging
from os.path import exists

import MIDI.Internal as internal
from MIDI.Internal import *
from MIDI.Message import *
from MIDI.Container import File, Track


def hexify(message):
    return message.encode(Encoding.MIDI).hex(' ').upper()


# Test data obtained from https://github.com/jazz-soft/test-midi-files/.
#    This is the C Major test file with the header removed.
#    There is also an extraneous 0A byte that I removed, as I cannot
#    find anywhere in the MIDI docs that it is required.  Length bytes
#    were adjusted accordingly as well.
def get_test_track():
    track = Track()
    track.append(TrackName(text="C Major Scale Test"))
    track.append(Copyright(text="https://jazz-soft.net"))
    track.append(Text(
        text="This is the most basic MIDI test to serve a template for more useful tests."))
    track.append(Text(text="You must hear a C-Major scale."))
    track.append(Text(text=" Now you must hear C5!"))
    track.append(NoteOn(TimeStamp(1, 1), 0, 60, 127))
    track.append(NoteOff(TimeStamp(1, 2), 0, 60, 64))
    track.append(Text(TimeStamp(1, 2), text=" Now you must hear D5!"))
    track.append(NoteOn(TimeStamp(1, 2), 0, 62, 127))
    track.append(NoteOff(TimeStamp(1, 3), 0, 62, 64))
    track.append(Text(TimeStamp(1, 3), text=" Now you must hear E5!"))
    track.append(NoteOn(TimeStamp(1, 3), 0, 64, 127))
    track.append(NoteOff(TimeStamp(1, 4), 0, 64, 64))
    track.append(Text(TimeStamp(1, 4), text=" Now you must hear F5!"))
    track.append(NoteOn(TimeStamp(1, 4), 0, 65, 127))
    track.append(NoteOff(TimeStamp(2, 1), 0, 65, 64))
    track.append(Text(TimeStamp(2, 1), text=" Now you must hear G5!"))
    track.append(NoteOn(TimeStamp(2, 1), 0, 67, 127))
    track.append(NoteOff(TimeStamp(2, 2), 0, 67, 64))
    track.append(Text(TimeStamp(2, 2), text=" Now you must hear A5!"))
    track.append(NoteOn(TimeStamp(2, 2), 0, 69, 127))
    track.append(NoteOff(TimeStamp(2, 3), 0, 69, 64))
    track.append(Text(TimeStamp(2, 3), text=" Now you must hear B5!"))
    track.append(NoteOn(TimeStamp(2, 3), 0, 71, 127))
    track.append(NoteOff(TimeStamp(2, 4), 0, 71, 64))
    track.append(Text(TimeStamp(2, 4), text=" Now you must hear C6!"))
    track.append(NoteOn(TimeStamp(2, 4), 0, 72, 127))
    track.append(NoteOff(TimeStamp(3, 1), 0, 72, 64))
    track.append(Text(TimeStamp(3, 1), text="Thank you!"))
    track.append(EndOfTrack(TimeStamp(3, 1)))
    return track


class TestTimestamp:
    def test_midi_conversion(self):
        init = TimeStamp(1, 1, 1)
        assert init.to_midi_ticks(
            128, init, internal.TimeSignature(4, 4)) == 0

        ts = TimeStamp(12, 1, 3)
        assert ts.to_midi_ticks(
            128, init, internal.TimeSignature(4, 4)) == 5664

    def test_jack_conversion(self):
        init = TimeStamp(1, 1, 1)
        assert init.to_jack_time(48000, 90, internal.TimeSignature(4, 4)) == 0

        ts = TimeStamp(12, 1, 3)
        assert ts.to_jack_time(
            48000, 90, internal.TimeSignature(4, 4)) == 1410000


class TestTrack:
    def test_track(self):
        track = get_test_track()
        calculated = track.encode(
            Encoding.MIDI, internal.TimeSignature(4, 4), 96)
        answer = bytes.fromhex('4d 54 72 6b 00 00 01 c2 00 ff 03 12 43 20 4d 61 6a 6f 72 20 53 63 61 6c 65 20 54 65 73 74 00 ff 02 15 68 74 74 70 73 3a 2f 2f 6a 61 7a 7a 2d 73 6f 66 74 2e 6e 65 74 00 ff 01 4b 54 68 69 73 20 69 73 20 74 68 65 20 6d 6f 73 74 20 62 61 73 69 63 20 4d 49 44 49 20 74 65 73 74 20 74 6f 20 73 65 72 76 65 20 61 20 74 65 6d 70 6c 61 74 65 20 66 6f 72 20 6d 6f 72 65 20 75 73 65 66 75 6c 20 74 65 73 74 73 2e 00 ff 01 1e 59 6f 75 20 6d 75 73 74 20 68 65 61 72 20 61 20 43 2d 4d 61 6a 6f 72 20 73 63 61 6c 65 2e 00 ff 01 16 20 4e 6f 77 20 79 6f 75 20 6d 75 73 74 20 68 65 61 72 20 43 35 21 00 90 3c 7f 60 80 3c 40 00 ff 01 16 20 4e 6f 77 20 79 6f 75 20 6d 75 73 74 20 68 65 61 72 20 44 35 21 00 90 3e 7f 60 80 3e 40 00 ff 01 16 20 4e 6f 77 20 79 6f 75 20 6d 75 73 74 20 68 65 61 72 20 45 35 21 00 90 40 7f 60 80 40 40 00 ff 01 16 20 4e 6f 77 20 79 6f 75 20 6d 75 73 74 20 68 65 61 72 20 46 35 21 00 90 41 7f 60 80 41 40 00 ff 01 16 20 4e 6f 77 20 79 6f 75 20 6d 75 73 74 20 68 65 61 72 20 47 35 21 00 90 43 7f 60 80 43 40 00 ff 01 16 20 4e 6f 77 20 79 6f 75 20 6d 75 73 74 20 68 65 61 72 20 41 35 21 00 90 45 7f 60 80 45 40 00 ff 01 16 20 4e 6f 77 20 79 6f 75 20 6d 75 73 74 20 68 65 61 72 20 42 35 21 00 90 47 7f 60 80 47 40 00 ff 01 16 20 4e 6f 77 20 79 6f 75 20 6d 75 73 74 20 68 65 61 72 20 43 36 21 00 90 48 7f 60 80 48 40 00 ff 01 0a 54 68 61 6e 6b 20 79 6f 75 21 00 ff 2f 00'.upper())
        if calculated != answer:
            for i in range(len(calculated)):
                if calculated[i] != answer[i] and i > 8:
                    logging.info(f'i = {i}')
                    logging.info(
                        f'Calculated: {calculated[i:].hex(" ").upper()}')
                    logging.info(f'Answer:     {answer[i:].hex(" ").upper()}')
                    break

        assert calculated == answer


class TestFile:
    def test_file(self):
        # Utilizing ticks=96 due to the test data
        f = File(ticks=96)
        f.append_track(get_test_track())
        f.save('testfile')
        assert exists('testfile.mid')
        with open('testfile.mid', 'rb') as mfile:
            assert mfile.read() == bytes.fromhex('4D 54 68 64 00 00 00 06 00 00 00 01 00 60 4d 54 72 6b 00 00 01 c2 00 ff 03 12 43 20 4d 61 6a 6f 72 20 53 63 61 6c 65 20 54 65 73 74 00 ff 02 15 68 74 74 70 73 3a 2f 2f 6a 61 7a 7a 2d 73 6f 66 74 2e 6e 65 74 00 ff 01 4b 54 68 69 73 20 69 73 20 74 68 65 20 6d 6f 73 74 20 62 61 73 69 63 20 4d 49 44 49 20 74 65 73 74 20 74 6f 20 73 65 72 76 65 20 61 20 74 65 6d 70 6c 61 74 65 20 66 6f 72 20 6d 6f 72 65 20 75 73 65 66 75 6c 20 74 65 73 74 73 2e 00 ff 01 1e 59 6f 75 20 6d 75 73 74 20 68 65 61 72 20 61 20 43 2d 4d 61 6a 6f 72 20 73 63 61 6c 65 2e 00 ff 01 16 20 4e 6f 77 20 79 6f 75 20 6d 75 73 74 20 68 65 61 72 20 43 35 21 00 90 3c 7f 60 80 3c 40 00 ff 01 16 20 4e 6f 77 20 79 6f 75 20 6d 75 73 74 20 68 65 61 72 20 44 35 21 00 90 3e 7f 60 80 3e 40 00 ff 01 16 20 4e 6f 77 20 79 6f 75 20 6d 75 73 74 20 68 65 61 72 20 45 35 21 00 90 40 7f 60 80 40 40 00 ff 01 16 20 4e 6f 77 20 79 6f 75 20 6d 75 73 74 20 68 65 61 72 20 46 35 21 00 90 41 7f 60 80 41 40 00 ff 01 16 20 4e 6f 77 20 79 6f 75 20 6d 75 73 74 20 68 65 61 72 20 47 35 21 00 90 43 7f 60 80 43 40 00 ff 01 16 20 4e 6f 77 20 79 6f 75 20 6d 75 73 74 20 68 65 61 72 20 41 35 21 00 90 45 7f 60 80 45 40 00 ff 01 16 20 4e 6f 77 20 79 6f 75 20 6d 75 73 74 20 68 65 61 72 20 42 35 21 00 90 47 7f 60 80 47 40 00 ff 01 16 20 4e 6f 77 20 79 6f 75 20 6d 75 73 74 20 68 65 61 72 20 43 36 21 00 90 48 7f 60 80 48 40 00 ff 01 0a 54 68 61 6e 6b 20 79 6f 75 21 00 ff 2f 00')

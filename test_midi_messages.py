import logging
from MIDI import *


def hexify(b):
    return b.encode(Encoding.MIDI).hex(' ').upper()


class TestMidiChannel:
    def test_note_on(self):
        note_on = NoteOn(0, 0, 60, 127)
        logging.info(hexify(note_on))
        assert note_on.encode(
            Encoding.MIDI) == bytes.fromhex('00 90 3C 7F')

    def test_note_off(self):
        note_off = NoteOff(96, 1, 60, 64)
        logging.info(hexify(note_off))
        assert note_off.encode(
            Encoding.MIDI) == bytes.fromhex('60 81 3C 40')

    def test_aftertouch(self):
        aftertouch = Aftertouch(5, 9, 73)
        logging.info(hexify(aftertouch))
        assert aftertouch.encode(
            Encoding.MIDI) == bytes.fromhex('05 D9 49')

    def test_control_change(self):
        cc = ControlChange(103, 12, 18, 97)
        logging.info(hexify(cc))
        assert cc.encode(Encoding.MIDI) == bytes.fromhex('67 BC 12 61')

    def test_pitch_bend(self):
        pb = PitchBend(0, 1, 127)
        logging.info(hexify(pb))
        assert pb.encode(Encoding.MIDI) == bytes.fromhex('00 E1 00 7F')

    def test_polyphonic_key(self):
        pk = PolyphonicKey(0, 0, 69, 92)
        logging.info(hexify(pk))
        assert pk.encode(Encoding.MIDI) == bytes.fromhex('00 A0 45 5C')

    def test_program_change(self):
        pc = ProgramChange(42, 7, 19)
        logging.info(hexify(pc))
        assert pc.encode(Encoding.MIDI) == bytes.fromhex('2A C7 13')


class TestMidiMeta:
    def test_channel_prefix(self):
        cp = ChannelPrefix(37291, 10)
        logging.info(hexify(cp))
        assert cp.encode(Encoding.MIDI) == bytes.fromhex(
            '91 AB FF 20 01 0A')

    def test_end_of_track(self):
        eot = EndOfTrack()
        logging.info(hexify(eot))
        assert eot.encode(Encoding.MIDI) == bytes.fromhex('00 FF 2F 00')

    def test_key_signature(self):
        ks = KeySignature(500000, -3, 1)
        logging.info(hexify(ks))
        assert ks.encode(Encoding.MIDI) == bytes.fromhex(
            '07 A1 20 FF 59 02 FD 01')

    def test_sequence_number(self):
        sn = SequenceNumber(0, 2)
        logging.info(hexify(sn))
        assert sn.encode(Encoding.MIDI) == bytes.fromhex(
            '00 FF 00 02 00 02')

    def test_smpte(self):
        smpte = SMPTE(0, 10, 20, 30, 40, 50)
        logging.info(hexify(smpte))
        assert smpte.encode(Encoding.MIDI) == bytes.fromhex(
            '00 FF 54 05 0A 14 1E 28 32')

    def test_tempo(self):
        tempo = Tempo(0, 140)
        logging.info(hexify(tempo))
        assert tempo.encode(Encoding.MIDI) == bytes.fromhex(
            '00 FF 51 03 00 00 8C')

    def test_time_signature(self):
        ts = TimeSignature(0, 6, 8)
        logging.info(hexify(ts))
        assert ts.encode(Encoding.MIDI) == bytes.fromhex(
            '00 FF 58 04 06 08 00 18')

    def test_track_number(self):
        tn = TrackNumber(0, 5)
        logging.info(hexify(tn))
        assert tn.encode(Encoding.MIDI) == bytes.fromhex(
            '00 FF 00 02 00 05')


class TestMidiMetaText:
    def test_copyright(self):
        copyright = Copyright(0, '(c)2024 That\'s Some Record Label!')
        logging.info(hexify(copyright))
        assert copyright.encode(Encoding.MIDI) == bytes.fromhex(
            '00 FF 02 21 28 63 29 32 30 32 34 20 54 68 61 74 27 73 20 53 6F 6D 65 20 52 65 63 6F 72 64 20 4C 61 62 65 6C 21')

    def test_cue_point(self):
        cp = CuePoint(11, 'Verse 1')
        logging.info(hexify(cp))
        assert cp.encode(Encoding.MIDI) == bytes.fromhex(
            '0B FF 07 07 56 65 72 73 65 20 31')

    def test_instrument(self):
        i = Instrument(5, 'Grand Piano')
        logging.info(hexify(i))
        assert i.encode(Encoding.MIDI) == bytes.fromhex(
            '05 FF 04 0B 47 72 61 6E 64 20 50 69 61 6E 6F')

    def test_lyric(self):
        l = Lyric(
            123456789, 'Louisiana / Born on the bayou I go / Looking for crawdads')
        logging.info(hexify(l))
        assert l.encode(Encoding.MIDI) == bytes.fromhex(
            '07 5B CD 15 FF 05 39 4C 6F 75 69 73 69 61 6E 61 20 2F 20 42 6F 72 6E 20 6F 6E 20 74 68 65 20 62 61 79 6F 75 20 49 20 67 6F 20 2F 20 4C 6F 6F 6B 69 6E 67 20 66 6F 72 20 63 72 61 77 64 61 64 73')

    def test_marker(self):
        m = Marker(0, 'Chorus')
        logging.info(hexify(m))
        assert m.encode(Encoding.MIDI) == bytes.fromhex(
            '00 FF 06 06 43 68 6F 72 75 73')

    def test_sequence_name(self):
        sn = SequenceName(0, 'Melody Sequence 1')
        logging.info(hexify(sn))
        assert sn.encode(Encoding.MIDI) == bytes.fromhex(
            '00 FF 03 11 4D 65 6C 6F 64 79 20 53 65 71 75 65 6E 63 65 20 31')

    def test_text(self):
        t = Text(0, 'Don\'t @ Me, Bruh!')
        logging.info(hexify(t))
        assert t.encode(Encoding.MIDI) == bytes.fromhex(
            '00 FF 01 11 44 6F 6E 27 74 20 40 20 4D 65 2C 20 42 72 75 68 21')

    def test_track_name(self):
        tn = TrackName(text='The Cooliest Track Name')
        logging.info(hexify(tn))
        assert tn.encode(Encoding.MIDI == bytes.fromhex(
            '00 FF 03 17 54 68 65 20 43 6F 6F 6C 69 65 73 74 20 54 72 61 63 6B 20 4E 61 6D 65'))

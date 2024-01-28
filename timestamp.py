# This library determines the starting beats and note lengths
#    based on 32nd notes.


class TimeSig:
    def __init__(self, num_beats=4, note_per_beat=4):
        self.num_beats     = num_beats
        self.note_per_beat = note_per_beat


# This class expects standard measure/beat counting as input, so the very
#      first note would be at measure 1, starting beat 1, sub beat 1.
#      Do not use 0s.
class TimeStamp:
    def __init__(self, starting_measure, starting_beat, starting_sub_beat=1):
        self.starting_measure  = starting_measure
        self.starting_beat     = starting_beat
        self.starting_sub_beat = starting_sub_beat

    def __str__(self):
        return f'TimeStamp({self.starting_measure}, {self.starting_beat}, {self.starting_sub_beat})'

    def beats_to_ticks(self, timestamp, ticks_per_quarter_note, time_sig):
        bt     = 32 * (4 / time_sig.note_per_beat)
        mbeats = bt * time_sig.num_beats * (timestamp.starting_measure - 1)
        bbeats = bt * (timestamp.starting_beat - 1)
        total_beats = mbeats + bbeats + (timestamp.starting_sub_beat - 1)
        return int((total_beats / 32) * ticks_per_quarter_note)

    def to_midi_ticks(self, ticks_per_quarter_note, last_timestamp, time_signature):
        current = self.beats_to_ticks(self, ticks_per_quarter_note, time_signature)
        prior   = self.beats_to_ticks(last_timestamp, ticks_per_quarter_note, time_signature)
        if current > prior:
            return current - prior
        else:
            return 0

    def to_jack_time(self, sample_rate, tempo, time_signature):
        bf = ((1 / (tempo / 60)) * sample_rate)
        measures  = (self.starting_measure  - 1)  * time_signature.num_beats * bf
        beats     = (self.starting_beat     - 1) * bf
        sub_beats = (self.starting_sub_beat - 1) * (bf / 32)
        return (measures + beats + sub_beats)

# This library determines the starting beats and note lengths
#    based on 32nd notes.


# This class expects standard measure/beat counting as input, so the very
#      first note would be at measure 1, starting beat 1, sub beat 1.
#      Do not use 0s.
class TimeStamp:
    def __init__(self, starting_measure, starting_beat, starting_sub_beat=1, sub_beats_per_beat=8):
        self.starting_measure = starting_measure
        self.starting_beat = starting_beat
        self.starting_sub_beat = starting_sub_beat
        # Below determines smallest note possible in a song.
        # Assuming 4/4 time, 2 = 8th notes, 4 = 16th notes, 8 = 32nd notes, etc.
        # Assuming 6/8 time, 2 = 16th notes, 4 = 32nd notes, 8 = 64th notes, etc.
        self.sub_beats_per_beat = sub_beats_per_beat

    def __repr__(self):
        return f'TimeStamp({self.starting_measure}, {self.starting_beat}, {self.starting_sub_beat})'

    def beats_to_ticks(self, timestamp, ticks_per_quarter_note, time_sig):
        bt = self.sub_beats_per_beat * (4 / time_sig.note_per_beat)
        mbeats = bt * time_sig.num_beats * (timestamp.starting_measure - 1)
        bbeats = bt * (timestamp.starting_beat - 1)
        sbeats = (timestamp.starting_sub_beat - 1)
        total_beats = mbeats + bbeats + sbeats
        return int((total_beats / self.sub_beats_per_beat) * ticks_per_quarter_note)

    def to_midi_ticks(self, ticks_per_quarter_note, last_timestamp, time_signature):
        current = self.beats_to_ticks(
            self, ticks_per_quarter_note, time_signature)
        prior = self.beats_to_ticks(
            last_timestamp, ticks_per_quarter_note, time_signature)
        if current > prior:
            return current - prior
        else:
            return 0

    def to_jack_time(self, sample_rate, tempo, time_signature):
        bf = ((1 / (tempo / 60)) * sample_rate)
        measures = (self.starting_measure - 1) * time_signature.num_beats * bf
        beats = (self.starting_beat - 1) * bf
        sub_beats = (self.starting_sub_beat - 1) * (bf / 32)
        return (measures + beats + sub_beats)

    def to_sub_beats(self, time_sig):
        current = self.starting_measure * time_sig.num_beats * self.sub_beats_per_beat
        current += self.starting_beat * self.sub_beats_per_beat
        current += self.starting_sub_beat
        return current

    # The following function is to calculate and return a new timestamp for use in my
    #    AI.  Note lengths will for the time being be a floating point value with 1.0 = quarter note,
    #    so half note = 2.0, quarter note = 0.5, etc.
    def add(self, note_length, time_sig):
        # convert curr_ts to all sub_beats
        # Calculate number of sub_beats for new note_length
        current = self.to_sub_beats(time_sig)
        # Add numbers together
        new_sub_beats = current + (self.sub_beats_per_beat * note_length)
        # determine new timestamp based on new sub_beat total
        new_measure = int(new_sub_beats // (self.sub_beats_per_beat * time_sig.num_beats))
        new_beat    = int(new_sub_beats %  (self.sub_beats_per_beat * time_sig.num_beats) // self.sub_beats_per_beat)
        new_subbeat = int(new_sub_beats %  (self.sub_beats_per_beat * time_sig.num_beats) %  self.sub_beats_per_beat)
        return TimeStamp(new_measure, new_beat, new_subbeat)

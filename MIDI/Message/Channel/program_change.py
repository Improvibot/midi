from MIDI.Message.Template import ChannelMessage


class ProgramChange(ChannelMessage):
    def __init__(self, timestamp, channel, program_number):
        super().__init__(timestamp, channel)
        self._event_code = (0xC0).to_bytes(1, 'big')
        self.program_number = program_number.to_bytes(1, 'big')

    def data(self):
        return self.program_number

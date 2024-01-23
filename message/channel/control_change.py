from MIDI.message.internal import ChannelMessage


class ControlChange(ChannelMessage):
    def __init__(self, timestamp, channel, controller, value):
        super().__init__(timestamp, channel)
        self._event_code = (0xB0).to_bytes(1, 'big')
        self.controller = controller.to_bytes(1, 'big')
        self.value = value.to_bytes(1, 'big')

    def data(self):
        return self.controller + self.value

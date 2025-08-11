import device


class MidiForwarder:
    def __init__(self, receiver_index=0, debug=False):
        self.receiver_index = receiver_index
        self.debug = debug
        self.receiver_exists = device.dispatchReceiverCount() >= self.receiver_index + 1

    def forward(self, event):
        if self.receiver_exists:
            self._forward_midi_event(event)

    def _forward_midi_event(self, event):
        if self.debug:
            self._log_midi_event(event)

        event_sysex = self._get_sysex(event)
        message = self._pack_midi_message(event.status, event.data1, event.data2)

        if event_sysex is not None:
            device.dispatch(self.receiver_index, message, event_sysex)
        else:
            device.dispatch(self.receiver_index, message)

    def _pack_midi_message(self, status, data1, data2):
        return (data2 << 16) | (data1 << 8) | status
    
    def _log_midi_event(self, event):
        destination_port = device.dispatchGetReceiverPortNumber(self.receiver_index)
        event_sysex = self._get_sysex(event)
        print(f"Forwarding MIDI to port {destination_port}: {event.status}, {event.data1}, {event.data2}, sysex={event_sysex}")

    def _get_sysex(self, event):
        return event.sysex if hasattr(event, 'sysex') else None


class MidiForwarderAsSysex:
    def __init__(self, receiver_index=0, debug=False, sysex_signature=None):
        self.receiver_index = receiver_index
        self.debug = debug
        self.sysex_signature = sysex_signature if sysex_signature is not None else b'\x0E\x90\x01'
        self.receiver_exists = device.dispatchReceiverCount() >= self.receiver_index + 1

    def forward(self, event):
        if self.receiver_exists:
            self._forward_midi_event(event)

    def _forward_midi_event(self, event):
        if self.debug:
            self._log_midi_event(event)

        if hasattr(event, 'sysex') is False or event.sysex is None:
            self._send_custom_sysex(event.status, event.data1, event.data2)

    def _log_midi_event(self, event):
        destination_port = device.dispatchGetReceiverPortNumber(self.receiver_index)
        print(f"Forwarding MIDI to port {destination_port} as SYSEX: {event.status}, {event.data1}, {event.data2}")

    def _send_custom_sysex(self, status, data1, data2):
        payload = [status, data1, data2]
        sysex_message = b'\xF0' + self.sysex_signature + bytes(payload) + b'\xF7'
        device.dispatch(self.receiver_index, 0, sysex_message)
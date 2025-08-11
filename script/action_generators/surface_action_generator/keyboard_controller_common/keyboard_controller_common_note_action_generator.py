from script.action_generators.surface_action_generator.surface_actions import (
    NoteOnAction,
    NoteOffAction,
    PitchBendAction,
)


class KeyboardControllerCommonNoteActionGenerator:
    def __init__(self, sysex_signature = None):
        self.sysex_signature = b'\xF0' + (sysex_signature if sysex_signature else b'\x0E\x90\x01')

    def handle_midi_event(self, fl_event):
        if fl_event.status == 0 and fl_event.sysex is not None and fl_event.sysex.startswith(self.sysex_signature):
            msg_type = fl_event.sysex[4]
            data1 = fl_event.sysex[5]
            data2 = fl_event.sysex[6]
            if msg_type == 0x90 and data2 > 0:
                return [NoteOnAction(note=data1, velocity=data2)]
            elif (msg_type == 0x90 and data2 == 0) or msg_type == 0x80:
                return [NoteOffAction(note=data1, velocity=data2)]
            elif msg_type == 0xE0:
                return [PitchBendAction(value=data2)]
        return []

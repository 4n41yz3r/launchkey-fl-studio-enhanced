# name=Milos Launchkey MK4 MIDI
# supportedHardwareIds=00 20 29 46 01 00 00,00 20 29 45 01 00 00,00 20 29 44 01 00 00,00 20 29 43 01 00 00
from script.fl import FL
from script.midi_utils import MidiBypass, MidiForwarderAsSysex
import device

DAW_RECEIVER_INDEX = 0

fl = FL()
midi_bypass = MidiBypass(fl)
midi_forwarder = MidiForwarderAsSysex(receiver_index=DAW_RECEIVER_INDEX, debug=False)

def OnInit():
    print("Assigned port number:", device.getPortNumber())
    check_daw_receiver()

def OnMidiMsg(fl_event):
    if is_note_aftertouch_or_pitchbend(fl_event):
        midi_forwarder.forward(fl_event)
    fl_event.handled = False

def OnPitchBend(fl_event):
    midi_bypass.on_pitch_bend(fl_event)

def check_daw_receiver():
    receiver_count = device.dispatchReceiverCount()
    if (receiver_count < 1):
        print("Warning: No DAW MIDI receivers connected! Some DAW integration features may not work.")
    if (receiver_count > 1):
        print("Warning: More than one DAW MIDI receiver connected! This may cause unexpected behavior.")

def is_note_aftertouch_or_pitchbend(fl_event):
    msg_type = fl_event.status & 0xF0
    velocity = fl_event.data2

    return (
        # Note On (velocity > 0)
        (msg_type == 0x90 and velocity > 0) or
        # Note Off (explicit or Note On with velocity 0)
        (msg_type == 0x90 and velocity == 0) or
        (msg_type == 0x80) or
        # Polyphonic Aftertouch
        (msg_type == 0xA0) or
        # Channel Aftertouch (Mono)
        (msg_type == 0xD0) or
        # Pitch Bend Change
        (msg_type == 0xE0)
    )
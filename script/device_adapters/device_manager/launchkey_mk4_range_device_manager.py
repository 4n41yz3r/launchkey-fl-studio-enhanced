class LaunchkeyMk4RangeDeviceManager:
    sysex_message_header = [0x00, 0x20, 0x29, 0x02]
    set_tempo_command = 0x0A

    def __init__(self, sender, product_defs):
        self.sender = sender
        self.product_defs = product_defs

    def enable_encoder_mode(self):
        self.sender.send_message(0xB6, 0x45, 0x7F)

    def select_encoder_layout(self, layout):
        self.sender.send_message(*self.product_defs.SurfaceEvent.EncoderLayout.value, layout)

    def return_to_previous_encoder_layout(self):
        self.sender.send_message(
            *self.product_defs.SurfaceEvent.EncoderLayout.value, self.product_defs.EncoderLayout.Revert.value
        )

    def set_tempo(self, tempo):
        msb = (int(tempo) >> 7) & 0x7F
        lsb = int(tempo) & 0x7F
        set_tempo_sysex_message = self.sysex_message_header + [
            self.product_defs.Constants.NovationProductId.value,
            self.set_tempo_command,
            msb,
            lsb,
        ]
        self.sender.send_sysex(set_tempo_sysex_message)
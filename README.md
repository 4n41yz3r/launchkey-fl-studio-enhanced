# FL Studio Novation Launchkey MK4 Advanced MIDI Script

An advanced FL Studio MIDI script for Novation Launchkey MK4 series controllers that provides deep DAW integraion including FLKey-style step sequencer, encoder parameter pagination, plugin preset switching, comprehensive display feedback, and much more.


## 🚀 Features

### 🥁 Step Sequencer
- **Full FLKey-style step sequencer**: Complete sequencing workflow with visual feedback and real-time editing
- **Multi-parameter editing**: Adjust pitch, velocity, release, fine pitch, pan, mod X/Y, and time shift per note
- **Play cursor visualization**: Real-time playback position indicator synchronized with FL Studio

### 🎛️ Plugin Parameter Control
- **Encoder parameter pages**: Navigate through plugin parameters in multiple organized 8-parameter chunks
- **Plugin preset navigation**: Browse through plugin presets with dedicated encoder controls (FL Studio plugins only)
- **Extended plugin support**: Pre-configured parameter mappings for popular FL Studio plugins
- **Custom parameter mappings**: Add your own parameter definitions for any plugin

### 🎚️ Multi-Mode Fader Control
- **Three fader modes**: Cycle between Mixer and Channel control modes using the ArmSelect button
- **New Channel Volume fader mode**: Faders control channel rack volume levels, fader buttons control channel mute

### 📊 Additional Improvements
- **Current mixer encoder mode indicators**: Visual display of the currently selected mixer mode
- **New Plugin Mix Level encoder mode**: Control mix level of the currently selected mixer track plugins using encoders
- **Pattern selection**: Navigate patterns with previous/next buttons and on-screen feedback in Sequencer/Drum pad mode
- **Mixer track plugin selection**: Switch between mixer track plugins using navigation buttons in DAW pad mode

## 📋 Supported Hardware

- Novation Launchkey MK4 25/37/49/61
- Hardware IDs: `00 20 29 46 01 00 01`, `00 20 29 45 01 00 01`, `00 20 29 44 01 00 01`, `00 20 29 43 01 00 01`


## 🛠️ Installation

1. **Download** the script files
2. **Copy** the entire folder to your FL Studio MIDI Scripts directory:
   ```
   C:\Users\[Username]\Documents\Image-Line\FL Studio\Settings\Hardware\[NewFolderName]
   ```
3. **Restart** FL Studio
4. **Configure** your Launchkey MK4 in FL Studio's MIDI settings:
   - Go to `Options > MIDI Settings`
   - Select your DAW Launchkey MK4 device (`MIDIIN2`) under `Input` tab
   - Set the `Controller type` to `Milos Launchkey MK4 DAW`


## 🎮 Usage

### Step Sequencer (Drum Pad Mode)
- **Activation**: Switch to drum mode using `Shift + Drum` pad
- **Channel navigation**: Use `Pad Up/Down` buttons to switch between channels
- **Sequencer Bank selection**: Use `Track Left/Right` buttons to navigate between sequencer banks.
- **Pattern selection**: Use `Shift + Pad Up/Down` buttons to navigate between patterns
- **Note toggle**: Press any pad to toggle notes on/off at the corresponding step position
- **Play cursor**: Visual playback indicator moves across pads in sync with FL Studio playback
- **Multi-parameter editing**: Hold any pad + turn encoders to adjust:
  - **Pitch**: Change note pitch
  - **Velocity**: Adjust note velocity/volume
  - **Release**: Control note release time
  - **Fine pitch**: Fine-tune pitch with precision
  - **Pan**: Adjust stereo positioning
  - **Mod X/Y**: Control modulation parameters
  - **Time shift**: Micro-timing adjustments
- **Multi-edit mode**: Hold any pad for 1 second to enter multi-edit mode for batch parameter adjustments:
  - **Select**: Press any number of pads to toggle note selection on/off
  - **Update**: Turn encoders to adjust the selected notes' parameters simultaneously
  - **Exit**: Pres `Function` button to exit multi-edit mode

### Plugin Encoder Parameter Control
- **Encoder knobs**: Control plugin parameters 1-8 on current page
- **Parameter Page navigation**: Navigate between parameter pages using `Encoder Up/Down` buttons (Plugin Encoder mode)
- **Preset navigation**: Navigate through plugin presets using `Shift + Encoder Up/Down` buttons (Plugin Encoder mode)
- **Mixer Track Plugin selection**: Use `Shift + Pad Up/Down` buttons to switch between mixer track plugins in (DAW Pad Mode)
- **Idle screen display**: Shows parameter names with smart truncation

### Multi-Mode Fader Control (Launchkey MK4 49/61 only)
- **Mode cycling**: Press the `ArmSelect` button to cycle between multiple fader control modes:
  - Mixer Track Volume / Arm
  - Mixer Track Volume / Mute
  - Channel Volume / Mute
- **Channel Volume / Mute mode**:
  - Faders control channel rack volume levels independent of mixer tracks
  - Buttons control channel mute states with LED feedback corresponding to the channel color
  - Controls the currenty selected channel bank
  - The 9th fader controls master mixer volume
- **Visual feedback**:
  - Screen displays current mode when switching
  - The `ArmSelect` button's color indicates the sellected mode
  - Automatically focuses the appropriate FL Studio window

### Mixer Encoder Mode Features
- **Current mode indicators**: Clear display of current mixer mode
- **New Plugin Mix Level control**: Dedicated encoder mode for controlling mixer track plugin mix levels
  - **Access**: Navigate to "Plugin Mix" encoder mode using encoder navigation buttons
  - **Control**: Each encoder (1-8) controls the mix level of plugin slots 0-7 on the selected mixer track
  - **Display**: Shows track name, plugin slot number, and mix percentage (e.g., "Kick", "Slot 1 Mix", "75%")
  - **Preview**: Touch encoders with shift to see current mix levels without changing them

### Plugin Parameter Mappings
The script includes pre-configured parameter mappings for popular FL Studio plugins, with support for multiple pages of parameters per plugin. Users can easily extend this by adding their own custom parameter definitions.

## 🔧 Customization

### Adding Custom Plugin Parameters
You can add parameter mappings for your favorite plugins by editing the user plugin parameters dictionary:

```python
# In user/user_defined_plugin_mappings.py
user_plugin_parameter_mappings = {
    "Your Plugin Name": [
        # Page 1 parameters (0-7)
        PluginParameter(name="Param 1", index=0),
        PluginParameter(name="Param 2", index=1),
        PluginParameter(name="Param 3", index=2),
        # ... add up to 8 parameters per page
        
        # Page 2 parameters (8-15)
        PluginParameter(name="Param 9", index=8),
        PluginParameter(name="Param 10", index=9),
        # ... continue for additional pages
    ],
    "Another Plugin": [
        # Add parameters for other plugins
    ]
}
```

### Finding Plugin Parameter Indices
To find the correct parameter indices for your plugins:
1. Open FL Studio and load your plugin
2. Left-click on the plugin in the browser window to see the parameters
3. The parameter position usually corresponds to their index numbers starting with 0
4. Add the most useful parameters to your custom mapping

### Adding More Pages
Configure the number of pages in the layout manager:

```python
# In plugin_encoder_layout_manager.py
def __init__(self, ..., num_pages=4):  # Increase from default 3 to 4 pages
```


## 🤝 Contributing

1. **Clone** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request


## 📝 License

This project is licensed under the GNU GPL v3.0 License.


## 🙏 Acknowledgments

- **Novation** for the excellent Launchkey MK4 hardware
- **Image-Line** for FL Studio and the MIDI script API
- **FL Studio community** for inspiration and feedback


## 📞 Support

If you encounter any issues or have feature requests:

1. **Check** the existing issues on GitHub
2. **Create** a new issue with detailed information about your problem
3. **Include** your FL Studio version, Launchkey model, and any error messages

---

**Made with ❤️ for the FL Studio community**

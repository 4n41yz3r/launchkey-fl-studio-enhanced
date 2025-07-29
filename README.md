# FL Studio Novation Launchkey MK4 Enhanced MIDI Script

A custom FL Studio MIDI script for Novation Launchkey MK4 series controllers with enhanced features including FLKey-style step sequencer, advanced parameter pagination, and comprehensive display feedback.


## 🚀 Features

### 🥁 Step Sequencer
- **Full FLKey-style step sequencer**: Complete sequencing workflow with visual feedback and real-time editing
- **Multi-parameter editing**: Adjust pitch, velocity, release, fine pitch, pan, mod X/Y, and time shift per note
- **Play cursor visualization**: Real-time playback position indicator synchronized with FL Studio

### 🎛️ Plugin Parameter Control
- **Encoder parameter pages**: Navigate through plugin parameters in multiple organized 8-parameter chunks
- **Extended plugin support**: Pre-configured parameter mappings for popular FL Studio plugins
- **Custom parameter mappings**: Add your own parameter definitions for any plugin

### 🎵 Pattern Navigation
- **Simple pattern selection**: Navigate patterns with previous/next buttons and on-screen feedback

### 📊 Additional Improvements
- **Current mixer mode indicators**: Visual display of the currently selected mixer mode


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

### Step Sequencer (Drum Mode)
- **Activation**: Switch to drum mode using `Shift + Drum` button
- **Channel navigation**: Use `Pad Up/Down` buttons to switch between channels
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
- **Multi-edit mode**: Hold a pad to enter multi-edit mode for batch parameter adjustments

### Plugin Parameter Navigation
- **Encoder knobs**: Control parameters 1-8 on current page
- **Encoder Up/Down buttons**: Navigate between parameter pages
- **Idle screen display**: Shows parameter names with smart truncation
- **Real-time feedback**: Parameter values/display update in real-time

### Pattern Navigation
- **Shift + Pad Up/Down buttons**: Navigate between patterns when in DAW or Drum pad mode
- **Visual feedback**: Current pattern number notification display when switching

### Mixer Mode Features
- **Current mode indicators**: Clear display of current mixer mode


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

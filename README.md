**Text Morse Code Converter Desktop**

Desktop app to convert text to Morse code and vice versa, with real-time conversion and Morse code audio playback. Developed using PyQt6 for a clean and responsive interface.

**Features** ✨
- 🔄 **Real-time bidirectional conversion**: text ↔ Morse code 
- 🎵 **Morse code audio playback**: **Play / Pause / Stop** controls 
- 💡 **Highlight** of the currently played Morse character 
- 📜 **Auto-scroll** Morse view to keep highlight visible 
- 🔘 Buttons **enable/disable automatically** based on context
- ⏹ Playback stops automatically if Morse content changes 
- 🧩 **Modular code** with UI, conversion logic, and player separated

**Usage** 🛠️
- Run the application:
  ```bash
  python main.py
  ```
- Enter text in the left box or Morse code in the right box — conversion happens automatically
- Use the Play / Pause / Stop buttons to control Morse audio playback
- The currently played character is highlighted and the view scrolls automatically to follow it

**Requirements** 📦
- Python 3.10 or higher
- PyQt6
- pygame

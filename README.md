# Brewify
## Features
1. **Install/Uninstall**
   - Lets you **install** (formula, cask, or bundle) or **uninstall** existing Homebrew packages.
2. **Bundle Mode**
   - Build a list (formula or cask mix) and install them all at once.
3. **Interactive Search**
   - Uses [pyfzf](https://pypi.org/project/pyfzf/) and `fzf` for fuzzy searching across available Homebrew packages.

## Requirements
- **macOS** with Xcode Command Line Tools (the script itself checks and installs if necessary)
- **Homebrew** (the script also checks and installs if necessary)
- **Python 3.6+**
- **`pip`** to install any missing Python dependencies

## Setup and Usage

1. Clone this repository onto your macOS system.
```bash
git clone https://github.com/stowyh/brewify.git
```

2. **Create and activate a Python 3 virtual environment**:
   ```bash
   # Create a new virtual environment in a folder called 'venv'
   python3 -m venv venv
   # Activate the virtual environment
   source venv/bin/activate
   ```
   > **Why a virtual environment?**
   > Ensures the script installs Python dependencies (like `pyfzf`, `requests`) into a separate, safe environment without cluttering your global Python installation.

3. **Run the script**:
   ```bash
   python3 homebrew_installer.py
   ```

## Important Notes

1. **Potential Additional Permissions**
   - Installing Xcode CLT or Homebrew might prompt you for your **administrator password** or require you to accept Apple’s license agreement.

3. **Using Another Shell**
   - If you use `zsh`, `fish`, or another shell, activating the virtual environment is slightly different (e.g. `source venv/bin/activate.fish` for `fish`). Check your shell’s documentation.

## Demo
![demo](images/demo.gif)

## Contributing
Pull requests and issue reports are welcome. For major changes, open an issue first to discuss what you would like to change.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

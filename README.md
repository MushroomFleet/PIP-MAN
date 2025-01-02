# PIP-MAN (PIP Manager)
![Demo UI](https://raw.githubusercontent.com/MushroomFleet/PIP-MAN/main/images/pip-man-demo.png)

A user-friendly Python package manager with both GUI and CLI interfaces. PIP-MAN provides an intuitive way to manage Python packages in any Python environment, particularly useful for managing packages in embedded Python installations.

## Features

- **Dual Interface**: Choose between a web-based GUI (powered by Gradio) or a traditional command-line interface
- **Environment Management**: Easily switch between different Python environments by updating the Python path
- **Package Operations**:
  - Update pip to the latest version
  - Install new packages (with version specification support)
  - Remove existing packages
  - Check package versions
  - List all installed packages
- **Configuration Persistence**: Saves your Python path configuration between sessions
- **Secure By Default**: Web interface runs locally only, no external access
- **User-Friendly Interface**: Dynamic UI with helpful tooltips and instructions

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/pip-man.git
cd pip-man
```

2. Run the installation script:
```bash
install-pipman.bat
```

The installation script will:
- Create a Python virtual environment
- Install all required dependencies
- Set up the configuration files

## Usage

### Starting PIP-MAN

You can run PIP-MAN in two ways:

1. **GUI Mode** (Default):
```bash
run-pipman.bat
```

2. **CLI Mode**:
```bash
run-pipman.bat --cli
```

### GUI Interface

The web interface provides the following features:

1. **Operation Selection**:
   - Use the radio buttons to select the desired operation
   - Input fields dynamically appear based on the selected operation

2. **Available Operations**:
   - **Update PIP**: Updates pip to the latest version
   - **Install Package**: Install a new package
     - Supports version specification (e.g., requests==2.31.0)
   - **Remove Package**: Uninstall an existing package
   - **Check Version**: View the installed version of a package
   - **List Packages**: Display all installed packages
   - **Update Python Path**: Change the target Python environment

3. **Output**:
   - Results are displayed in a copyable text area
   - Use the "Clear Output" button to reset the display

### CLI Interface

The command-line interface offers the same functionality through a text-based menu:

1. Select operations by entering numbers 1-7:
   - 1: Update PIP
   - 2: Install Package
   - 3: Remove Package
   - 4: Check Version
   - 5: List Packages
   - 6: Update Python Path
   - 7: Exit

2. Follow the prompts to provide package names or paths as needed

### Configuration

PIP-MAN stores its configuration in `python_path.json` in the application directory. This file contains:
- The path to the Python executable being managed

The configuration file is automatically created on first run and can be updated through the interface.

## Technical Details

### Project Structure
```
pip-man/
├── requirements.txt       # Python dependencies
├── install-pipman.bat    # Installation script
├── run-pipman.bat        # Launcher script
├── pip_manager.py        # Main application code
└── python_path.json      # Configuration file (created on first run)
```

### Dependencies

- Python 3.6 or higher
- Gradio >= 4.44.1
- packaging >= 23.2
- pip >= 23.3.1

### Security Notes

- The web interface runs locally on `127.0.0.1:7860`
- Public URL sharing is disabled by default
- No external network access is required or allowed
- All package operations are executed in the specified Python environment only

## Common Issues and Solutions

1. **Python Path Not Found**
   - Ensure the path points to a valid python.exe
   - Use the full absolute path
   - Verify the Python installation is complete

2. **Package Installation Fails**
   - Check internet connectivity
   - Verify package name spelling
   - Ensure the package is available for your Python version

3. **Configuration Issues**
   - If the configuration file is corrupted, delete `python_path.json`
   - The application will create a new configuration on next run

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with [Gradio](https://www.gradio.app/)
- Inspired by the need for better package management in embedded Python environments

## Version History

- v1.0.0: Initial release
  - Dual interface support
  - Basic package management
  - Configuration persistence

# Environment Setup Guide

This guide will help you set up your environment for the AIDAChip GenAI Workshop.

## Prerequisites

### 1. Python 3.8+

Verify your Python installation:

```bash
python3 --version
```

If not installed, download from [python.org](https://www.python.org/downloads/) or use your package manager:

```bash
# macOS (with Homebrew)
brew install python3

# Ubuntu/Debian
sudo apt-get install python3 python3-pip

# Windows
# Download installer from python.org
```

### 2. Claude Code

This workshop is designed to be used with Claude Code, Anthropic's CLI tool.

Install Claude Code:

```bash
npm install -g @anthropic-ai/claude-code
```

Or if you don't have npm:

```bash
# macOS
brew install claude-code

# Other platforms - see https://claude.ai/claude-code
```

Verify installation:

```bash
claude --version
```

### 3. Code Editor (Recommended)

We recommend using **Visual Studio Code (VSCode)** for this workshop:

- Easily navigate between module folders and files
- View README.md files with rendered markdown preview
- Integrated terminal to run Claude Code alongside your editor

Download from [code.visualstudio.com](https://code.visualstudio.com/)

> **Note**: VSCode is optional. If you prefer, you can complete this workshop entirely from the terminal using your favorite text editor.

### 4. Python Libraries

Install required Python packages:

```bash
pip3 install numpy matplotlib pandas pyyaml
```

## Module-Specific Tools

Different modules require different tools. Install only what you need for the modules you plan to explore.

### Circuit Design (Module 01)

```bash
# macOS
brew install ngspice

# Ubuntu/Debian
sudo apt-get install ngspice

# Windows - download from http://ngspice.sourceforge.net/download.html
```

Verify: `ngspice --version`

### RTL Development & DV (Modules 02, 03)

```bash
# macOS
brew install icarus-verilog verilator

# Ubuntu/Debian
sudo apt-get install iverilog verilator

# Windows - download from http://iverilog.icarus.com/
```

Verify: `iverilog -V` and `verilator --version`

### Waveform Viewer (Modules 02, 03)

**Surfer** (recommended) - Modern, fast waveform viewer:

```bash
# macOS
brew install surfer

# Linux - download AppImage from https://surfer-project.org/
# Or install via cargo:
cargo install surfer

# Windows - download from https://surfer-project.org/
```

Verify: `surfer --version`

**Alternative**: GTKWave is also widely used:

```bash
# macOS
brew install gtkwave

# Ubuntu/Debian
sudo apt-get install gtkwave
```

### Physical Design (Module 04)

**Yosys** (synthesis - required before OpenROAD):

```bash
# macOS
brew install yosys

# Ubuntu/Debian
sudo apt-get install yosys

# Or build from source: https://github.com/YosysHQ/yosys
```

Verify: `yosys --version`

**OpenROAD** (place & route):

```bash
# Recommended: Use Docker
docker pull openroad/openroad

# Or use OpenROAD-flow-scripts (includes everything)
git clone --recursive https://github.com/The-OpenROAD-Project/OpenROAD-flow-scripts
cd OpenROAD-flow-scripts
./build_openroad.sh

# Or build from source: https://github.com/The-OpenROAD-Project/OpenROAD
```

> **Note**: The full RTL-to-GDS flow is: `Verilog → Yosys → OpenROAD → Layout`

### Layout (Module 05)

```bash
# KLayout
# macOS
brew install --cask klayout

# Ubuntu/Debian
sudo apt-get install klayout

# Windows - download from https://www.klayout.de/build.html
```

Verify: `klayout -v`

### Magic VLSI (for DRC/LVS)

```bash
# macOS
brew install magic

# Ubuntu/Debian
sudo apt-get install magic
```

## Quick Setup Verification

Run the setup checker from the workshop root directory:

```bash
python3 setup_check.py
```

This will verify:
- Python version and required libraries
- Claude Code installation
- Module-specific tools (optional)

## Troubleshooting

### Python Issues

**"python3: command not found"**
- Ensure Python is installed and in your PATH
- On Windows, try `python` instead of `python3`

**"pip3: command not found"**
- Try `python3 -m pip install <package>`

### Claude Code Issues

**"claude: command not found"**
- Ensure npm/node is installed: `node --version`
- Try reinstalling: `npm install -g @anthropic-ai/claude-code`
- Check your PATH includes npm global bin directory

### Tool Installation Issues

**Permission denied errors**
- Use `sudo` on Linux/macOS
- Run terminal as Administrator on Windows

**Package not found**
- Update your package manager: `brew update` or `apt-get update`
- Check the tool's official installation guide

## Recommended Directory Structure

For the best experience, clone this workshop and work within it:

```bash
git clone <workshop-repo-url>
cd AIDAChip_Workshop_Si
python3 setup_check.py
```

## What's Next?

Once your environment is set up:

1. Run `python3 setup_check.py` to verify
2. Start with [00_LLM_Fundamentals](00_LLM_Fundamentals/) to learn the basics
3. Explore modules relevant to your domain

---

*Having issues? Check the troubleshooting section above or reach out to AIDAChip for support.*

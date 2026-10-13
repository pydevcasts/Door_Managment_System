# Door Management System

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Platform](https://img.shields.io/badge/Platform-Raspberry%20Pi-c51a4a)
![Status](https://img.shields.io/badge/Status-Paused-lightgrey)
![License](https://img.shields.io/badge/License-Not%20specified-lightgrey)

An IoT-based system for remote door access control, written in Python and designed to run on a Raspberry Pi. It supports single-door and multi-door control over multiple channels, scheduled open/close operations, and real-time status monitoring.

<!-- Add a screenshot or architecture diagram from the images/ folder:
![Screenshot](images/screenshot.png)
-->

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Multilingual Support](#multilingual-support)
- [Project Status](#project-status)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)

---

## Overview

Door Management System is a modular client–server platform for controlling and monitoring one or more doors remotely. It is aimed at residential, office, and small commercial environments where centralized access control is needed.

The **server** runs on a Raspberry Pi and communicates with the door hardware. **Clients** connect to the server through Bluetooth, a mobile interface, or a web service.

## Features

- **Single- and multi-door control** — operate one door or a group of doors at once
- **Multiple access channels** — Bluetooth, mobile interface, and web service/server
- **Scheduling** — define open/close times per door
- **Real-time status monitoring** — view the current state of each door
- **Multilingual UI** — Persian and English
- **Modular codebase** — separate `client`, `server`, and `common` packages

## Architecture

```
┌──────────────┐   Bluetooth   ┐
│ Mobile client│───────────────┤
└──────────────┘               │     ┌─────────────────────┐     ┌────────────┐
┌──────────────┐   Web / API   ├────▶│ Server (Raspberry Pi)│────▶│ Door relays│
│ Web client   │───────────────┤     │ scheduling · state   │     │ / hardware │
└──────────────┘               │     └─────────────────────┘     └────────────┘
┌──────────────┐   Local       │
│ Desktop (Qt) │───────────────┘
└──────────────┘
```

| Component   | Responsibility                                          |
|-------------|---------------------------------------------------------|
| `server/`   | Device communication, scheduling, door state management |
| `client/`   | User-facing interface                                   |
| `common/`   | Shared models, protocol helpers, utilities              |
| `scripts/`  | Setup and utility scripts                               |
| `lang/`     | Language/translation files                              |

## Requirements

- Python 3.x
- PyQt (desktop interface)
- Raspberry Pi with Bluetooth support (for server deployment)
- Relay or other door-control hardware
- Python packages listed in `requirements.txt`

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/pydevcasts/Door_Managment_System.git
cd Door_Managment_System

# 2. Create and activate a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

Then edit the `.ini` configuration files to match your setup (see [Configuration](#configuration)).

## Usage

**Start the server** (on the Raspberry Pi):

```bash
python Server.py
```

**Start the client:**

```bash
python Main.py
```

From the client you can:

- Open or close a single door
- Control multiple doors at the same time
- View the current status of each door
- Configure scheduled open/close times

## Configuration

Behavior is controlled through INI files. Typical settings include:

- Door identifiers and grouping
- Communication channel settings (Bluetooth, web, mobile)
- Open/close schedules
- Language and UI preferences

## Project Structure

```
Door_Managment_System/
├── client/            # Client-side code
├── common/            # Shared modules
├── lang/              # Language files
├── scripts/           # Setup and utility scripts
├── server/            # Server-side code
├── images/            # Project images
├── ExceptHook.py      # Global exception handling
├── Exit.py            # Clean shutdown logic
├── Globals.py         # Global configuration and state
├── Lang.py            # Language handling
├── Main.py            # Client entry point
├── PyQtImports.py     # PyQt imports and helpers
├── Server.py          # Server entry point
├── Version.py         # Version information
├── setup.py           # Packaging script
└── test.py            # Test / scratch script
```

## Multilingual Support

Persian and English are supported. Translation files live in `lang/`. To add a language, follow the structure of the existing files.

## Project Status

Developed between 2021 and 2024. Core features — single/multi-door control, multi-channel communication, and scheduling — are implemented. Active development is currently paused. Before reusing the project, review the code and configuration, as some parts may need adaptation to your hardware.

## Contributing

Issues and suggestions are welcome. To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes
4. Open a pull request

## Author

**Siyamak Abasnezhad Torki** — [@pydevcasts](https://github.com/pydevcasts)

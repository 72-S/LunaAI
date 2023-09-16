# Setup Instructions

## Table of Contents
- [1. Installing Python](#1-installing-python)
  * [- 1.1 Windows](#11-windows)
  * [- 1.2 macOS](#12-macos)
  * [- 1.3 Linux](#13-linux)
- [2. Running main.py](#2-running-mainpy)
- [3. Opening the link in the console](#3-opening-the-link-in-the-console)

## 1. Installing Python

### 1.1 Windows:
- Navigate to the official Python website: [Python Downloads](https://www.python.org/downloads/)
- Download the latest version suitable for Windows.
- Run the downloaded executable.
- Make sure to check the box that says "Add Python to PATH".
- Click on "Install Now".
- Once installed, open Command Prompt and verify the installation:
  ```bash
  python --version
  ```

### 1.2 macOS:
- Open your Terminal.
- First, check if Python is already installed:
  ```bash
  python3 --version
  ```
- If not installed, continue to the next step.
- Install Python using Homebrew:
  ```bash
  brew install python3
  ```

### 1.3 Linux:
For Ubuntu/Debian-based distributions:
  ```bash
  sudo apt update
  sudo apt install python3
  ```
For Red Hat/Fedora-based distributions:
  ```bash
  sudo dnf install python3
  ```

## 2. Running main.py
After Python is installed, open your console or terminal and navigate to the directory where `main.py` is present.
- You can run the script using:
  ```bash
  python3 main.py
  ```
> Note: On Windows, you might just use `python` or `py` instead of `python3`.

## 3. Accessing the Flask server
After you've executed `main.py`, the console should display an IP address and port number, typically `127.0.0.1:5000` for local development.

- On Windows: Hold `Ctrl` and click the IP address to open it in the default web browser.
- On macOS: Hold `Command` and click the IP address to open it in the default web browser.
- On Linux (depending on the terminal): Hold `Ctrl` and click the IP address, or just click the IP address directly to open it in the default web browser.

Remember, always ensure that you've satisfied all dependencies and prerequisites before executing any scripts.

# Building from Source

This guide provides instructions for creating standalone executables for Windows and Linux from the source code. We use **PyInstaller** to package the application.

---

## Prerequisites

First, ensure you have all the project dependencies installed:

```bash
pip install -r requirements.txt
```

You will also need to install PyInstaller:

```bash
pip install pyinstaller
```

---

## Building for Windows

1.  **Open a command prompt or PowerShell** in the project's root directory.

2.  **Run the PyInstaller command**:

    ```bash
    pyinstaller --name "Github&Tailscale-Automation" --onefile --windowed --icon="resources/app_icon.ico" main.py
    ```

    *   `--name`: Sets the name of the executable.
    *   `--onefile`: Packages everything into a single executable file.
    *   `--windowed`: Prevents a console window from appearing when the application is run.
    *   `--icon`: Sets the application icon.

3.  **Find the executable**: The generated `.exe` file will be located in the `dist` directory.

---

## Building for Linux

Building a Linux executable requires running the command on a Linux-based system.

1.  **Open a terminal** in the project's root directory.

2.  **Run the PyInstaller command**:

    ```bash
    pyinstaller --name "Github-Tailscale-Automation" --onefile --noconsole --icon="resources/app_icon.png" main.py
    ```

    *   `--noconsole`: The equivalent of `--windowed` for Linux/macOS.
    *   **Note**: Linux does not use `.ico` files for icons. You can use a `.png` file instead.

3.  **Find the executable**: The generated executable file will be located in the `dist` directory.

4.  **Make the file executable**: You may need to grant execute permissions to the file:

    ```bash
    chmod +x dist/Github-Tailscale-Automation
    ```

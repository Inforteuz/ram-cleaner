# RAM Cleaner

**RAM Cleaner** is a Python application developed using the PyQt5 framework to monitor and manage RAM usage. It allows users to view running processes, kill unnecessary ones, and clear RAM to optimize system performance.

## Features

- **Real-time RAM Monitoring:** Displays real-time information about used and available RAM.
- **Process List:** Shows a list of running processes with details like process name, PID, user, and memory consumption.
- **Resource Highlighting:** Processes that consume the most memory are highlighted in red for easy identification.
- **Manual RAM Clearing:** Users can manually clear RAM by pressing the "Clear RAM" button.
- **Automatic RAM Cleaning:** The application can automatically clear RAM when usage exceeds 50%, with an option to enable or disable this feature.
- **Kill Process:** Users can terminate unnecessary processes from the list, with confirmation dialogs for resource-intensive applications like Chrome, Firefox, and VSCode.
- **User-friendly Interface:** A clean, intuitive interface with colored buttons and hover effects for better user experience.

## Installation

1. Ensure that Python 3 and PyQt5 are installed on your system.
   - Install Python: [Download Python](https://www.python.org/downloads/)
   - Install PyQt5 using pip:
     ```bash
     pip install PyQt5 psutil
     ```

2. Clone the repository:
   ```bash
   git clone https://github.com/ram-cleaner/ram-cleaner.git

# SysGauge - A System Monitor Application

A simple system monitoring application built using Python and PyQt5 that tracks and displays system metrics such as CPU usage, memory usage, disk usage, and network I/O. It also provides visual graphs of CPU and memory usage over time, and alerts the user if any of the metrics exceed predefined thresholds.

![image](https://github.com/user-attachments/assets/e89a6d63-4560-41a6-9cf3-e64a16af8431)


## Features

- Displays real-time system metrics (CPU, memory, disk usage, and network I/O).
- Graphs and charts for all of the system metrics.
- Alert system for high CPU, memory, or disk usage.
- Real-time updates with automatic polling.

## Features

| Feature                                      | Status     |
|----------------------------------------------|------------|
| **Real-Time Alerts**                         | ✅   |
| **Dark/Light Theme Switching**               | ✅   |
| **Multi-Process Monitoring**                 | ❌   |
| **Interactive Visualizations**               | ❌   |
| **Customizable Update Intervals**            | ❌   |
| **Export Data**                              | ❌   |


## Requirements

- Python 3.x
- PyQt5
- psutil
- matplotlib

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/ClutchyMuffin/SysGauge.git
    cd system-monitor
    ```

2. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the application:
    ```bash
    python app.py
    ```

## Files

1. `app.py`: Entry point to start the application.
2. `system_metrics.py`: Contains the SystemMetrics class that collects and stores system data.
3. `system_monitor_view.py`: Contains the SystemMonitorView class that manages the UI and displays metrics.
4. `system_monitor_controller.py`: Contains the SystemMonitorController class that links the model and the view, and updates the system metrics periodically.


## License
This project is licensed under the MIT License - see the LICENSE file for details

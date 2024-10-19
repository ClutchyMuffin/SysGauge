import sys
from system_monitor_view import SystemMonitorView
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from system_metrics import SystemMetrics

# Controller class that connects the model and view
class SystemMonitorController:

    def __init__(self):
        self.app = QApplication(sys.argv)
        self.model = SystemMetrics()
        self.view = SystemMonitorView(self.model)

        # Create a timer to update the model and view
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_model_and_view)
        self.timer.start(250)  # Update every 250ms

    # Check if any of the metrics exceed a threshold
    def check_thresholds(self):
        cpu = self.model.get_cpu_history()[-1]
        memory = self.model.get_mem_history()[-1]
        disk = self.model.get_disk_usage()

        # Example thresholds
        if cpu > 90:
            self.view.show_alert_popup(f"High CPU Usage: {cpu}%")
            self.view.update_alert_label(f"⚠️ High CPU Usage: {cpu}%")
        elif memory > 85:
            self.view.show_alert_popup(f"High Memory Usage: {memory}%")
            self.view.update_alert_label(f"⚠️ High Memory Usage: {memory}%")
        elif disk > 80:
            self.view.show_alert_popup(f"High Disk Usage: {disk}%")
            self.view.update_alert_label(f"⚠️ High Disk Usage: {disk}%")
        else:
            # Clear alert label if no issues
            self.view.update_alert_label("")

    def update_model_and_view(self):
        self.model.update_data()
        self.view.update_metrics()
        self.view.update_plot()
        self.check_thresholds()


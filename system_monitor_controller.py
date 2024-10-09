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

    # Update the model and view when the timer times out
    def update_model_and_view(self):
        self.model.update_data()
        self.view.update_metrics()
        self.view.update_plot()

from system_metrics import SystemMetrics
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout

# The SystemMonitorView class is a subclass of QMainWindow
class SystemMonitorView(QMainWindow):

    # Initialize the view with a model
    def __init__(self, model: SystemMetrics):
        super().__init__()
        self.model = model  # Store the model
        self.initUI()

    # Initialize the UI
    def initUI(self):
        self.setup_main_window()
        self.create_metrics_layout()
        self.create_plot_layout()

    # Setup the main window
    def setup_main_window(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('System Monitor')

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)

    # Create the metrics layout (top bar)
    def create_metrics_layout(self):
        print("Creating metrics layout")
        # add stuff here

    # Create the plot layout
    def create_plot_layout(self):
        print("Creating plot layout")
        # add stuff here

    # Update the metrics displayed in the labels
    def update_metrics(self):
        print("Updating metrics")
        # add stuff here

    # Update the plots
    def update_plots(self):
        print("Updating plots")
        # add stuff here
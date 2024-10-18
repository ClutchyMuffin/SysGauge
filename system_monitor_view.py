from system_metrics import SystemMetrics
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

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
        self.metrics_layout = QHBoxLayout()
        self.main_layout.addLayout(self.metrics_layout)

        # Labels
        self.cpu_label = QLabel("CPU Usage: ")
        self.mem_label = QLabel("Memory Usage: ")
        self.disk_label = QLabel("Disk Usage: ")
        self.net_label = QLabel("Network (sent/received): ")

        self.metrics_layout.addWidget(self.cpu_label)
        self.metrics_layout.addWidget(self.mem_label)
        self.metrics_layout.addWidget(self.disk_label)
        self.metrics_layout.addWidget(self.net_label)


    # Create the plot layout
    def create_plot_layout(self):
        self.plot_layout = QVBoxLayout()
        self.main_layout.addLayout(self.plot_layout)

        # CPU Usage Graph
        self.cpu_fig = Figure()
        self.cpu_ax = self.cpu_fig.add_subplot(111)
        self.cpu_ax.set_title('CPU Usage')
        self.cpu_ax.set_ylim(0, 100)
        self.cpu_canvas = FigureCanvas(self.cpu_fig)
        self.plot_layout.addWidget(self.cpu_canvas)

        # Memory Usage Graph
        self.mem_fig = Figure()
        self.mem_ax = self.mem_fig.add_subplot(111)
        self.mem_ax.set_title('Memory Usage')
        self.mem_ax.set_ylim(0, 100)
        self.mem_canvas = FigureCanvas(self.mem_fig)
        self.plot_layout.addWidget(self.mem_canvas)

    # Update the metrics displayed in the labels
    def update_metrics(self):
        print("Updating metrics")
        # add stuff here

    # Update the plots
    def update_plots(self):
        print("Updating plots")
        # add stuff here
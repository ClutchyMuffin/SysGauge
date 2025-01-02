from system_metrics import SystemMetrics
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QMessageBox, QProgressBar, QFrame, QSizePolicy, QAction, QMenuBar)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QColor
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.gridspec import GridSpec
import platform
import numpy as np

class SystemMonitorView(QMainWindow):
    def __init__(self, model: SystemMetrics):
        super().__init__()
        self.model = model
        self.create_menu_bar()
        self.initUI()
        self.apply_dark_theme()

    def apply_dark_theme(self):
        # Set dark theme palette
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.Text, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
        self.setPalette(dark_palette)

        # Update frame styles
        self.update_frame_styles("dark")
        self.update_graph_styles("dark")

    def initUI(self):
        self.setup_main_window()
        self.create_system_info()
        self.create_metrics_layout()
        
        # Alert Label with improved styling
        self.alert_label = QLabel("")
        self.alert_label.setStyleSheet("""
            QLabel {
                color: #ff5555;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
                background-color: rgba(255, 85, 85, 0.1);
            }
        """)
        self.main_layout.addWidget(self.alert_label)

    def setup_main_window(self):
        self.setGeometry(100, 100, 1200, 800)
        self.setWindowTitle('SysGauge - System Monitor')
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(20)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.central_widget.setLayout(self.main_layout)

    def create_system_info(self):
        info_frame = QFrame()
        info_frame.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        info_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.05);
                border-radius: 10px;
                padding: 10px;
            }
        """)
        
        info_layout = QHBoxLayout()
        
        # System information
        system_info = f"""
            <b>System:</b> {platform.system()} {platform.release()}<br>
            <b>Processor:</b> {platform.processor()}<br>
            <b>Architecture:</b> {platform.machine()}
        """
        
        info_label = QLabel(system_info)
        info_label.setTextFormat(Qt.RichText)
        info_layout.addWidget(info_label)
        
        info_frame.setLayout(info_layout)
        self.main_layout.addWidget(info_frame)

    def create_metrics_layout(self):
        metrics_frame = QFrame()
        metrics_frame.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        metrics_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.05);
                border-radius: 10px;
                padding: 15px;
            }
            QLabel {
                font-size: 14px;
            }
            QProgressBar {
                border: 2px solid grey;
                border-radius: 5px;
                text-align: center;
                height: 25px;
            }
            QProgressBar::chunk {
                background-color: #3daee9;
                border-radius: 3px;
            }
        """)

        metrics_layout = QVBoxLayout()
        
        # CPU Section
        cpu_section = QHBoxLayout()
        cpu_metrics = QVBoxLayout()
        self.cpu_progress = self.create_metric_widget("CPU Usage")
        cpu_metrics.addWidget(self.cpu_progress['frame'])
        
        # CPU Graph
        self.cpu_fig = Figure(figsize=(6, 2.5), facecolor='#353535')
        self.cpu_ax = self.cpu_fig.add_subplot(111)
        self.style_plot(self.cpu_ax, 'CPU History')
        self.cpu_canvas = FigureCanvas(self.cpu_fig)
        self.cpu_fig.subplots_adjust(bottom=0.2)
        
        cpu_section.addLayout(cpu_metrics, stretch=1)
        cpu_section.addWidget(self.cpu_canvas, stretch=2)
        metrics_layout.addLayout(cpu_section)
        
        # Memory Section
        mem_section = QHBoxLayout()
        mem_metrics = QVBoxLayout()
        self.mem_progress = self.create_metric_widget("Memory Usage")
        mem_metrics.addWidget(self.mem_progress['frame'])
        
        # Memory Graph
        self.mem_fig = Figure(figsize=(6, 2.5), facecolor='#353535')
        self.mem_ax = self.mem_fig.add_subplot(111)
        self.style_plot(self.mem_ax, 'Memory History')
        self.mem_canvas = FigureCanvas(self.mem_fig)
        self.mem_fig.subplots_adjust(bottom=0.2)
        
        mem_section.addLayout(mem_metrics, stretch=1)
        mem_section.addWidget(self.mem_canvas, stretch=2)
        metrics_layout.addLayout(mem_section)
        
        # Disk Section
        disk_section = QHBoxLayout()
        disk_metrics = QVBoxLayout()
        self.disk_progress = self.create_metric_widget("Disk Usage")
        disk_metrics.addWidget(self.disk_progress['frame'])
        
        # Disk Pie Chart
        self.disk_fig = Figure(figsize=(3, 3.5), facecolor='#353535')
        self.disk_ax = self.disk_fig.add_subplot(111)
        self.style_plot(self.disk_ax, 'Disk Usage')
        self.disk_canvas = FigureCanvas(self.disk_fig)
        self.disk_fig.subplots_adjust(bottom=0.1)
        
        disk_section.addLayout(disk_metrics, stretch=1)
        disk_section.addWidget(self.disk_canvas, stretch=1)
        metrics_layout.addLayout(disk_section)
        
        # Network Section
        net_section = QHBoxLayout()
        self.net_label = QLabel("Network (sent/received): ")
        net_section.addWidget(self.net_label)
        
        # Network Graph
        self.net_fig = Figure(figsize=(6, 2.5), facecolor='#353535')
        self.net_ax = self.net_fig.add_subplot(111)
        self.style_plot(self.net_ax, 'Network I/O')
        self.net_canvas = FigureCanvas(self.net_fig)
        self.net_fig.subplots_adjust(bottom=0.2)
        
        net_section.addWidget(self.net_canvas, stretch=2)
        metrics_layout.addLayout(net_section)
        
        metrics_frame.setLayout(metrics_layout)
        self.main_layout.addWidget(metrics_frame)

    def create_metric_widget(self, title):
        frame = QFrame()
        layout = QVBoxLayout()
        
        label = QLabel(f"{title}: 0%")
        progress = QProgressBar()
        progress.setMaximum(100)
        progress.setTextVisible(True)
        
        layout.addWidget(label)
        layout.addWidget(progress)
        frame.setLayout(layout)
        
        return {'frame': frame, 'label': label, 'progress': progress}

    def style_plot(self, ax, title):
        ax.set_facecolor('#252525')
        ax.set_title(title, color='white', pad=10, fontsize=12)
        if title != 'Disk Usage':  # Don't set ylim for pie chart
            ax.set_ylim(0, 100)
        ax.grid(True, linestyle='--', alpha=0.3)
        ax.tick_params(colors='white')
        for spine in ax.spines.values():
            spine.set_color('white')

    def update_metrics(self):
        # Update CPU
        cpu_value = self.model.get_cpu_history()[-1]
        self.cpu_progress['progress'].setValue(int(cpu_value))
        self.cpu_progress['label'].setText(f"CPU Usage: {cpu_value:.1f}%")
        
        # Update Memory
        mem_value = self.model.get_mem_history()[-1]
        self.mem_progress['progress'].setValue(int(mem_value))
        self.mem_progress['label'].setText(f"Memory Usage: {mem_value:.1f}%")
        
        # Update Disk
        disk_value = self.model.get_disk_usage()
        self.disk_progress['progress'].setValue(int(disk_value))
        self.disk_progress['label'].setText(f"Disk Usage: {disk_value:.1f}%")
        
        # Update Network
        sent, received = self.model.get_network_io()
        self.net_label.setText(
            f"Network I/O: ↑ {sent:.2f} MB | ↓ {received:.2f} MB"
        )

    def update_plot(self):
        # Update CPU plot
        self.cpu_ax.clear()
        self.style_plot(self.cpu_ax, 'CPU History')
        cpu_data = self.model.get_cpu_history()
        x = range(len(cpu_data))
        self.cpu_ax.plot(x, cpu_data, color=self.plot_colors['cpu'], linewidth=2)
        self.cpu_ax.fill_between(x, cpu_data, alpha=0.3, color=self.plot_colors['cpu'])
        self.cpu_fig.tight_layout(pad=1.0)
        self.cpu_canvas.draw()

        # Update Memory plot
        self.mem_ax.clear()
        self.style_plot(self.mem_ax, 'Memory History')
        mem_data = self.model.get_mem_history()
        self.mem_ax.plot(x, mem_data, color=self.plot_colors['memory'], linewidth=2)
        self.mem_ax.fill_between(x, mem_data, alpha=0.3, color=self.plot_colors['memory'])
        self.mem_fig.tight_layout(pad=1.0)
        self.mem_canvas.draw()

        # Update Network I/O plot
        self.net_ax.clear()
        self.style_plot(self.net_ax, 'Network I/O')
        sent, received = self.model.get_network_io()
        self.net_ax.bar(['Upload', 'Download'], [sent, received], 
                       color=[self.plot_colors['network_up'], self.plot_colors['network_down']])
        self.net_fig.tight_layout(pad=1.0)
        self.net_canvas.draw()

        # Update Disk Usage pie chart
        self.disk_ax.clear()
        self.style_plot(self.disk_ax, 'Disk Usage')
        disk_used = self.model.get_disk_usage()
        disk_free = 100 - disk_used
        colors = [self.plot_colors['disk_used'], self.plot_colors['disk_free']]
        self.disk_ax.pie([disk_used, disk_free], 
                         labels=[f'Used\n({disk_used:.1f}%)', f'Free\n({disk_free:.1f}%)'],
                         colors=colors,
                         autopct='%1.1f%%',
                         textprops={'color': 'white' if self.theme_action.text() == 'Switch to Light Theme' else 'black'})
        self.disk_fig.tight_layout(pad=1.0)
        self.disk_canvas.draw()

    def show_alert_popup(self, message):
        alert = QMessageBox(self)
        alert.setIcon(QMessageBox.Warning)
        alert.setText(message)
        alert.setWindowTitle("System Alert")
        
        # Get current theme
        is_dark = self.theme_action.text() == 'Switch to Light Theme'
        
        if is_dark:
            style = """
                QMessageBox {
                    background-color: #353535;
                    color: white;
                }
                QMessageBox QLabel {
                    color: white;
                }
                QPushButton {
                    background-color: #3daee9;
                    color: white;
                    padding: 5px 15px;
                    border-radius: 3px;
                }
                QPushButton:hover {
                    background-color: #4dc4ff;
                }
            """
        else:
            style = """
                QMessageBox {
                    background-color: #ffffff;
                    color: black;
                }
                QMessageBox QLabel {
                    color: black;
                }
                QPushButton {
                    background-color: #0078d4;
                    color: white;
                    padding: 5px 15px;
                    border-radius: 3px;
                }
                QPushButton:hover {
                    background-color: #1a86d9;
                }
            """
        
        alert.setStyleSheet(style)
        alert.exec_()

    def update_alert_label(self, message):
        self.alert_label.setText(message)

    def create_menu_bar(self):
        menubar = self.menuBar()
        view_menu = menubar.addMenu('View')
        
        # Theme switcher action
        self.theme_action = QAction('Switch to Light Theme', self)
        self.theme_action.triggered.connect(self.toggle_theme)
        view_menu.addAction(self.theme_action)

    def toggle_theme(self):
        if self.theme_action.text() == 'Switch to Light Theme':
            self.apply_light_theme()
            self.theme_action.setText('Switch to Dark Theme')
        else:
            self.apply_dark_theme()
            self.theme_action.setText('Switch to Light Theme')

    def apply_light_theme(self):
        # Light theme palette
        light_palette = QPalette()
        light_palette.setColor(QPalette.Window, QColor(240, 240, 240))
        light_palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
        light_palette.setColor(QPalette.Base, QColor(255, 255, 255))
        light_palette.setColor(QPalette.AlternateBase, QColor(245, 245, 245))
        light_palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
        light_palette.setColor(QPalette.ToolTipText, QColor(0, 0, 0))
        light_palette.setColor(QPalette.Text, QColor(0, 0, 0))
        light_palette.setColor(QPalette.Button, QColor(240, 240, 240))
        light_palette.setColor(QPalette.ButtonText, QColor(0, 0, 0))
        light_palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
        light_palette.setColor(QPalette.Link, QColor(0, 100, 200))
        light_palette.setColor(QPalette.Highlight, QColor(0, 120, 215))
        light_palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
        self.setPalette(light_palette)

        # Update frame styles
        self.update_frame_styles("light")
        self.update_graph_styles("light")

    def update_frame_styles(self, theme):
        base_style = """
            QFrame {
                border-radius: 10px;
                padding: 15px;
            }
            QLabel {
                font-size: 14px;
            }
            QProgressBar {
                border: 2px solid grey;
                border-radius: 5px;
                text-align: center;
                height: 25px;
            }
        """
        
        if theme == "light":
            style = base_style + """
                QFrame {
                    background-color: rgba(0, 0, 0, 0.05);
                }
                QProgressBar::chunk {
                    background-color: #0078d4;
                }
            """
            self.alert_label.setStyleSheet("""
                QLabel {
                    color: #d83b01;
                    font-weight: bold;
                    padding: 10px;
                    border-radius: 5px;
                    background-color: rgba(216, 59, 1, 0.1);
                }
            """)
        else:
            style = base_style + """
                QFrame {
                    background-color: rgba(255, 255, 255, 0.05);
                }
                QProgressBar::chunk {
                    background-color: #3daee9;
                }
            """
            self.alert_label.setStyleSheet("""
                QLabel {
                    color: #ff5555;
                    font-weight: bold;
                    padding: 10px;
                    border-radius: 5px;
                    background-color: rgba(255, 85, 85, 0.1);
                }
            """)

        for frame in self.findChildren(QFrame):
            frame.setStyleSheet(style)

    def update_graph_styles(self, theme):
        if theme == "light":
            facecolor = '#ffffff'
            textcolor = 'black'
            gridcolor = '#cccccc'
            plot_colors = {
                'cpu': '#0078d4',
                'memory': '#d83b01',
                'network_up': '#107c10',
                'network_down': '#5c2d91',
                'disk_used': '#008272',
                'disk_free': '#e6e6e6'
            }
        else:
            facecolor = '#353535'
            textcolor = 'white'
            gridcolor = '#555555'
            plot_colors = {
                'cpu': '#3daee9',
                'memory': '#ff5555',
                'network_up': '#50fa7b',
                'network_down': '#bd93f9',
                'disk_used': '#ff79c6',
                'disk_free': '#44475a'
            }

        self.plot_colors = plot_colors
        
        for fig in [self.cpu_fig, self.mem_fig, self.disk_fig, self.net_fig]:
            fig.set_facecolor(facecolor)
            for ax in fig.get_axes():
                ax.set_facecolor(facecolor)
                ax.tick_params(colors=textcolor)
                ax.title.set_color(textcolor)
                for spine in ax.spines.values():
                    spine.set_color(textcolor)
                ax.grid(True, linestyle='--', alpha=0.3, color=gridcolor)
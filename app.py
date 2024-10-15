from system_monitor_controller import SystemMonitorController
import sys

if __name__ == '__main__':
    # Create the controller
    controller = SystemMonitorController()

    # Show the view
    controller.view.show()

    # Start the application event loop
    sys.exit(controller.app.exec_())
import psutil
from collections import deque

# Class to store system metrics
class SystemMetrics:

    def __init__(self, history_length=10):

        # Lists & Variables to hold data
        self.cpu_history = deque(maxlen=history_length)
        self.mem_history = deque(maxlen=history_length)
        self.disk_usage = 0
        self.net_io = (0, 0)

    # Update the data stored in the data structures
    def update_data(self):
        self.cpu_history.append(psutil.cpu_percent())
        self.mem_history.append(psutil.virtual_memory().percent)
        self.disk_usage = psutil.disk_usage('/').percent
        io_counters = psutil.net_io_counters()
        self.net_io = (io_counters.bytes_sent / (1024.0 **2), io_counters.bytes_recv / (1024.0 **2))

    # Getters for the data stored in the data structures
    def get_cpu_history(self):
        return list(self.cpu_history)

    def get_mem_history(self):
        return list(self.mem_history)

    def get_disk_usage(self):
        return self.disk_usage

    def get_network_io(self):
        return self.net_io
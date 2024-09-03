import psutil

# Gets all the needed information about the CPU.
class SystemInfo:

    def cpu_info():
        cpu_count_physical = psutil.cpu_count(logical=False)
        cpu_count_logical = psutil.cpu_count(logical=True)
        cpu_frequency = psutil.cpu_freq(percpu=False)
        cpu_times = psutil.cpu_times(percpu=False)
        cpu_utilization = psutil.cpu_percent(interval=0.1, percpu=False)
        cpu_stats = psutil.cpu_stats()
        return cpu_count_physical, cpu_count_logical, cpu_frequency, cpu_times, cpu_utilization, cpu_stats
    
    def memory_info():
        memory_usage = psutil.virtual_memory()
        swap_memory_stats = psutil.swap_memory()
        return memory_usage, swap_memory_stats
    
    def disks_info(diskpath):
        disk_partitions = psutil.disk_partitions(all=False)
        disk_usage_stats = psutil.disk_usage(diskpath)
        disk_io_stats = psutil.disk_io_counters(perdisk=False, nowrap=True)
        return disk_partitions, disk_usage_stats, disk_io_stats
    
    def network_info(kind):
        network_io_stats = psutil.net_io_counters(pernic=False, nowrap=True)
        network_socket_connections = psutil.net_connections(kind)
        network_cards_info =  psutil.net_if_stats()
        return network_io_stats, network_socket_connections, network_cards_info
    
    def sensors_info():
        battery_info = psutil.sensors_battery
        return battery_info
    
    def system_details():
        boot_time = psutil.boot_time()
        system_users = psutil.users()
        return boot_time, system_users
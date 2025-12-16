
import psutil

def close_all_ports():
    """
    Closes all open network ports by terminating the processes using them.
    """
    for conn in psutil.net_connections():
        if conn.pid and conn.status == 'LISTEN':
            try:
                process = psutil.Process(conn.pid)
                print(f"Terminating process {process.name()} (PID: {conn.pid}) using port {conn.laddr.port}")
                process.terminate()
            except psutil.NoSuchProcess:
                print(f"Process with PID {conn.pid} not found.")
            except psutil.AccessDenied:
                print(f"Access denied to terminate process with PID {conn.pid}.")

if __name__ == "__main__":
    close_all_ports()

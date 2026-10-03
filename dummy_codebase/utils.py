import time

def log_event(event_type, message):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {event_type}: {message}")

def system_health_check():
    # Check memory and CPU
    # This is a dummy implementation
    return {"status": "OK", "cpu": 15, "mem": 42}

class Logger:
    def __init__(self, log_file):
        self.log_file = log_file

    def write_log(self, message):
        with open(self.log_file, "a") as f:
            f.write(message + "\n")

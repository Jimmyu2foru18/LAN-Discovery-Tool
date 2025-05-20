import socket
import time
import json
import platform

class Broadcaster:
    def __init__(self, port=5000, broadcast_interval=5):
        self.port = port
        self.broadcast_interval = broadcast_interval
        self.socket = None
        self.running = False
        self.hostname = platform.node()
        
    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.running = True
        
    def stop(self):
        self.running = False
        if self.socket:
            self.socket.close()
            self.socket = None
    
    def broadcast(self):
        if not self.socket or not self.running:
            return
            
        # Get local IP address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('10.255.255.255', 1))
            ip_address = s.getsockname()[0]
        except Exception:
            ip_address = '127.0.0.1'
        finally:
            s.close()
        
        # Create message
        message = {
            'hostname': self.hostname,
            'ip_address': ip_address,
            'timestamp': time.time()
        }
        
        # Send broadcast
        try:
            self.socket.sendto(json.dumps(message).encode(), ('<broadcast>', self.port))
        except Exception as e:
            print(f"Error broadcasting message: {e}")
    
    def run(self):
        self.start()
        while self.running:
            self.broadcast()
            time.sleep(self.broadcast_interval)
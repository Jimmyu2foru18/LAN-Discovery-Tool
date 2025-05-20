import socket
import json
import threading
import time

class Listener:
    def __init__(self, port=5000, callback=None):
        self.port = port
        self.callback = callback
        self.socket = None
        self.thread = None
        self.running = False
        self.hosts = {}
        self.hosts_lock = threading.Lock()
        
    def start(self):
        if self.running:
            return
            
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(('', self.port))
        
        self.running = True
        self.thread = threading.Thread(target=self._listen)
        self.thread.daemon = True
        self.thread.start()
        
    def stop(self):
        self.running = False
        if self.socket:
            self.socket.close()
            self.socket = None
        if self.thread:
            self.thread.join(timeout=1.0)
            self.thread = None
    
    def _listen(self):
        while self.running:
            try:
                data, addr = self.socket.recvfrom(1024)
                self._process_message(data, addr)
            except Exception as e:
                if self.running:
                    print(f"Error receiving message: {e}")
    
    def _process_message(self, data, addr):
        try:
            message = json.loads(data.decode())
            
            if not all(k in message for k in ['hostname', 'ip_address', 'timestamp']):
                return
                
            # Update hosts list
            with self.hosts_lock:
                host_id = f"{message['ip_address']}_{message['hostname']}"
                message['last_seen'] = time.time()
                self.hosts[host_id] = message
                
            # Call callback
            if self.callback:
                self.callback(self.get_hosts())
                
        except json.JSONDecodeError:
            print(f"Received invalid JSON from {addr}")
        except Exception as e:
            print(f"Error processing message: {e}")
    
    def get_hosts(self):
        with self.hosts_lock:
            return list(self.hosts.values())
    
    def cleanup_stale_hosts(self, max_age=30):
        current_time = time.time()
        with self.hosts_lock:
            stale_hosts = []
            for host_id, host in self.hosts.items():
                if current_time - host['last_seen'] > max_age:
                    stale_hosts.append(host_id)
            
            for host_id in stale_hosts:
                del self.hosts[host_id]
                
            if stale_hosts and self.callback:
                self.callback(self.get_hosts())
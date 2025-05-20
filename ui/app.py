import tkinter as tk
from tkinter import ttk
import threading
import time

class DiscoveryApp(tk.Tk):
    def __init__(self, broadcaster, listener):
        super().__init__()
        
        self.broadcaster = broadcaster
        self.listener = listener
        
        self.title("LAN Discovery Tool")
        self.geometry("800x500")
        self.minsize(600, 400)
        
        self._create_widgets()
        self._setup_layout()
        
        # Set up listener callback
        self.listener.callback = self._update_hosts
        self._start_services()
        self._setup_cleanup_timer()
        
    def _create_widgets(self):
        self.control_frame = ttk.Frame(self)
        
        # Status label
        self.status_var = tk.StringVar(value="Starting...")
        self.status_label = ttk.Label(self.control_frame, textvariable=self.status_var)
        self.refresh_button = ttk.Button(self.control_frame, text="Refresh", command=self._manual_refresh)   
        # Host list
        self.tree_columns = ("hostname", "ip_address", "last_seen")
        self.tree = ttk.Treeview(self, columns=self.tree_columns, show="headings")
        # Set column headings
        self.tree.heading("hostname", text="Hostname")
        self.tree.heading("ip_address", text="IP Address")
        self.tree.heading("last_seen", text="Last Seen")
        self.tree.column("hostname", width=200)
        self.tree.column("ip_address", width=150)
        self.tree.column("last_seen", width=200)
        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        
    def _setup_layout(self):
        self.control_frame.pack(fill=tk.X, padx=10, pady=10)
        self.status_label.pack(side=tk.LEFT, padx=5)
        self.refresh_button.pack(side=tk.RIGHT, padx=5)
        
        # Tree and scrollbar
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
    def _start_services(self):
        self.listener.start()
        self.broadcaster_thread = threading.Thread(target=self.broadcaster.run)
        self.broadcaster_thread.daemon = True
        self.broadcaster_thread.start()
        
        self.status_var.set("Running - Broadcasting and listening for devices")
        
    def _update_hosts(self, hosts):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for host in hosts:
            last_seen_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(host['last_seen']))
            self.tree.insert(
                "", 
                tk.END, 
                values=(host['hostname'], host['ip_address'], last_seen_str)
            )
            
    def _manual_refresh(self):
        self.broadcaster.broadcast()
        self._update_hosts(self.listener.get_hosts())
        
        self.status_var.set("Manually refreshed at " + time.strftime("%H:%M:%S"))
        
    def _setup_cleanup_timer(self):
        def cleanup():
            if self.winfo_exists():
                self.listener.cleanup_stale_hosts()
                self.after(10000, cleanup)
        self.after(10000, cleanup)
        
    def on_closing(self):
        self.listener.stop()
        self.broadcaster.stop()
        self.destroy()
        
    def run(self):
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.mainloop()
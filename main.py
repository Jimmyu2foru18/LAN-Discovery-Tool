import os
import sys
import threading

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from broadcaster import Broadcaster
from listener import Listener
from ui.app import DiscoveryApp

def main():
    """Main entry point for the application"""
    broadcaster = Broadcaster(port=5000, broadcast_interval=5)
    listener = Listener(port=5000)
    
    app = DiscoveryApp(broadcaster, listener)
    
    try:
        app.run()
    except KeyboardInterrupt:
        print("Shutting down...")
        broadcaster.stop()
        listener.stop()
    except Exception as e:
        print(f"Error: {e}")
        broadcaster.stop()
        listener.stop()

if __name__ == "__main__":
    os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), "ui"), exist_ok=True)
    main()
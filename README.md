# LAN Discovery Tool

A simple network utility that allows devices on a Local Area Network (LAN) to discover each other using UDP broadcast messages.

# LAN Discovery Tool
## Features

- Broadcasts presence messages on the local network using UDP
- Listens for broadcast messages from other devices
- Maintains a list of active hosts on the network
- Simple user interface to view discovered devices
- Displays device information including IP address, hostname, and last seen time
- Automatic cleanup of stale hosts
- Manual refresh capability

## Project Structure

```
.
├── README.md         
├── main.py          
├── broadcaster.py 
├── listener.py    
└── ui/             
	└── app.py    
```

## Requirements

- Python 3.6+
- tkinter (for GUI)

## How to Run

```bash
python main.py
```

## How It Works

1. The application sends UDP broadcast messages to announce its presence on the network
2. It simultaneously listens for similar broadcast messages from other devices
3. When a message is received, the device information is added to the active hosts list
4. The UI displays the list of discovered devices and updates it in real-time
5. Devices that haven't sent a message within a certain timeframe are marked as inactive

## Protocol Details

The discovery protocol uses UDP broadcast messages on port 5000. Each message contains:
- Device hostname
- Device IP address
- Timestamp

# Centralized tooltips for the GUI elements.
# This file is part of NeveBit.

tooltips = {
    "main_window": {
        "log_viewer": "Display the Log Viewer window",
        "stream_viewer": "Display the Stream Viewer window",
        "support": "Click to support my work with a coffee! ☕",
    },
    "title_bar": {
        "uplink": "Uplink data rate (device -> interface)",
        "downlink": "Downlink data rate (interface -> device)",
        "info": "Display information bar",
        "theme": "Change the program color theme",
        "adder": "Display uplink notification counter",
        "autosync": "Change device autosync mode",
        "move_left": "Show previous tab",
        "move_right": "Show next tab",
        "always_on_top": "Change always-on-top mode",
        "fullscreen": "Switch fullscreen mode",
    },
    "win_log": {
        "copy": "Copy this error to the clipboard",
    },
    "interface_select": {
        "usb": "Connect to a USB/UART device",
        "bluetooth": "Connect to a Bluetooth device",
        "wifi": "Connect to a WiFi device",
        "ethernet": "Connect to an Ethernet device",
        "mqtt": "Connect to an MQTT broker",
        "error": "Network or adapter not found for this interface",
    },
    "connection_windows": {
        "scan": "Scan for available devices in the interface",
        "connect": "Connect to the selected device",
        "disconnect": "Disconnect from the connected device",
        "exit": "Close the connection and return to the main window",
        "list": "Double-click on a device to connect",
        "uart_baudrate": "Baud rate for UART communication",
        "wifi_network": "Network CIDR to scan for devices",
        "wifi_subnet": "Network subnet to scan for devices",
        "ethernet_network": "Network CIDR to scan for devices",
        "ethernet_subnet": "Network subnet to scan for devices",
        "mqtt_broker_address": "Address of the MQTT broker to connect to",
        "mqtt_broker_port": "Port number of the MQTT broker",
        "mqtt_broker_username": "Username for authenticating with the MQTT broker",
        "mqtt_broker_password": "Password for authenticating with the MQTT broker",
        "encryption_enable": "Enable secure communication with the device",
        "encryption_key": "AES-256 encryption key for secure communication",
    },
    "terminal": {
        "start": "Start/resume data display in the console",
        "stop": "Pause data display in the console",
        "clear": "Clear the entire console",
        "copy": "Copy the console content to the clipboard",
        "log": "Start/stop data logging to a file",
        "text_wrap": "Toggle text wrapping in the console",
        "autoscroll": "Toggle autoscrolling in the console",
        "send": "Send data to device",
        "send_save": "Send data and save as quick command",
        "quick_command": "Display quick command shortcuts",
        "quick_command_shortcut": "Click to send this command",
        "delete_quick_command": "Clears the quick command list",
        "show_metadata": "Toggle stats bar",
    },
    "updater": {
        "start": "Initiate firmware update",
        "stop": "Abort firmware update",
        "clear": "Clear firmware information",
        "reload_button": "Reload firmware file",
        "folder_button": "Choose firmware (.bin) file",
    },
    "graph": {
        "start": "Start data plotting",
        "stop": "Stop data plotting",
        "clear": "Clear graph",
        "show_var_list_button": "Toggle graph list",
        "show_metadata": "Toggle stats bar",
        "show_button": "Display selected graph",
        "show_button_vis": "Toggle graph visibility",
        "set_range_button": "Adjust Y-axis range",
        "cb_autorange": "Toggle auto Y-axis range",
        "set_range_min": "Set Y-axis min value",
        "set_range_max": "Set Y-axis max value",
        "txt_max_x": "Set max sample display",
    },
    "map": {
        "start": "Start trace recording",
        "stop": "Stop trace recording",
        "clear": "Clear trace",
        "copy": "Copy trace to clipboard",
        "save_button": "Save trace to file",
    },
    "camera": {
        "start": "Start camera feed",
        "stop": "Stop camera feed",
        "clear": "Clear camera feed",
        "copy": "Copy camera feed to clipboard",
        "save_button": "Save camera feed to file",
    },
    "lidar": {
        "start": "Start LiDAR feed",
        "stop": "Stop LiDAR feed",
        "clear": "Clear LiDAR feed",
        "copy": "Copy LiDAR feed to clipboard",
        "save_button": "Save LiDAR feed to file",
    },
    "joystick": {
        "scan_joystick": "Scan for available joysticks",
        "connect_joystick": "Connect to the selected joystick",
        "disconnect_joystick": "Disconnect from the connected joystick",
        "list": "Double-click on a joystick to connect",
    },
    "task_monitor": {
        "start": "Start device task",
        "stop": "Stop device task",
        "pause_button": "Pause device task",
        "resume_button": "Resume device task",
    },
}

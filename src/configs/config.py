# Global configuration file for the application.
# This file is part of NeveBit.

globals = {
    "win_app": {
        "name": "FemtoEncoder",  # Name of the application
        "def_size": (750, 400),  # Default size of the application window
        "minimum_size": (750, 400),  # Minimum size of the application window
        "version": "v1.1.0",  # Version of the application
        "debug_mode": False,  # Indicates if the application is in debug mode
    },
    "win_title": {
        "height": 32,  # Height of the title bar
    },
    "win_log": {
        "name": "FemtoEncoder Logs",  # Name of the error report window
        "def_size": (750, 400),  # Size of the error report window
        "minimum_size": (750, 400),  # Minimum size of the error report window
        "line_limit": 100,  # Maximum number of lines in the viewer
        "font": "Inconsolata",  # Font for the viewer
        "font_size": 10,  # Font size for the viewer
    },
    "win_support": {
        "name": "NeveBit Support",  # Name of the support window
        "def_size": (400, 150),  # Default size of the support window
        "minimum_size": (400, 150),  # Minimum size of the support window
    },
    "win_theme": {
        "name": "NeveBit Theme Selector",  # Name of the theme selector window
        "def_size": (400, 400),  # Default size of the theme selector window
        "minimum_size": (400, 400),  # Minimum size of the theme selector window
    },
    "gui": {
        "theme": "night",  # Theme of the GUI
        "custom_bar_button_size": (30, 30),  # Size of buttons in title bar
        "def_button_size": (31, 31),  # Default size of buttons in the GUI
        "widget_stats_height": 20,  # Height of the stats bar
        "error_icon_size": (30, 30),  # Size of the error icon
        "error_button_size": (35, 35),  # Size of the error button
    },
    "adapter": {
        "network_verifier": False,  # Enabled global network veryfier
    },
    "usb": {
        "enabled": True,  # Enable UART functionality
        "icon_size": (120, 120),  # Size of the UART icon
        "name": "USB",  # Title of the UART tab
        "baudrate": 921600,  # Baud rate for UART communication
        "keepalive": 400,  # Keepalive interval for UART
        "con_retries": 5,  # Number of retries for UART reconnection
        "act_timeout": 2000,  # Timeout to declare UART connection lost in ms
        "updater_chunk_size": 4096,  # Data chunk size for UART updates
        "updater_ack_timeout": 0.5,  # Timeout for acknowledgements during UART updates
        "updater_ack_retries": 5,  # Number of retries for acknowledgements during UART updates
        "scape_sequence": b"</AS>",  # Escape sequence for UART data (encoded)
        "keepalive_sequence": b"</KA>",  # Keepalive sequence for UART data (encoded)
        "receive_timeout": 0.005,  # Timeout for UART data reception
        "uplink_chunk_size": 16,  # Chunk size for UART uplink data
        "network_verify": False,  # Enabled auto-diagnose network status
    },
    "bluetooth": {
        "enabled": True,  # Enable Bluetooth functionality
        "icon_size": (125, 125),  # Size of the Bluetooth icon
        "name": "BLE",  # Title of the BLE tab
        "scan_timeout": 5,  # Timeout for Bluetooth scanning
        "connection_timeout": 8,  # Connection timeout for Blutetooth
        "con_retries": 5,  # Number of retries for Bluetooth reconnection
        "updater_chunk_size": 500,  # Data chunk size for Blueooth updates
        "updater_ack_timeout": 0.5,  # Timeout for acknowledgements during Bluetooth updates
        "updater_ack_retries": 3,  # Number of retries for acknowledgements during Bluetooth updates
        "network_verify": False,  # Enabled auto-diagnose network status
    },
    "wifi": {
        "enabled": True,  # Enable WiFi functionality
        "icon_size": (130, 130),  # Size of the WiFi icon
        "name": "Wi-Fi",  # Title of the WiFi tab
        "network": "192.168.1.0/24",  # Network IP range for WiFi
        "port_uplink": 56320,  # Uplink port number for WiFi
        "port_downlink": 56321,  # Downlink port number for WiFi
        "con_retries": 5,  # Number of retries for WiFi reconnection
        "act_timeout": 2000,  # Timeout to declare WiFi connection lost in ms
        "updater_chunk_size": 4096,  # Data chunk size for WiFi updates
        "updater_ack_timeout": 0.5,  # Timeout for acknowledgements during WiFi updates
        "updater_ack_retries": 5,  # Number of retries for acknowledgements during WiFi updates
        "scape_sequence": b"</AS>",  # Escape sequence for WiFi data (encoded)
        "keepalive_sequence": b"</KA>",  # Keepalive sequence for WiFi data (encoded)
        "receive_timeout": 0.005,  # Timeout for WiFi data reception
        "uplink_chunk_size": 2048,  # Chunk size for WiFi uplink data
        "network_verify": False,  # Enabled auto-diagnose network status
    },
    "ethernet": {
        "enabled": True,  # Enable Ethernet functionality
        "icon_size": (115, 115),  # Size of the Ethernet icon
        "name": "Ethernet",  # Title of the Ethernet tab
        "network": "192.168.1.0/24",  # Default Ethernet network CIDR
        "port_uplink": 5000,  # Default port for receiving data from the device
        "port_downlink": 5001,  # Default port for sending data to the device
        "con_retries": 5,  # Number of retries for Ethernet reconnection
        "act_timeout": 2000,  # Timeout to declare Ethernet connection lost in ms
        "updater_chunk_size": 4096,  # Data chunk size for Ethernet updates
        "updater_ack_timeout": 0.5,  # Timeout for acknowledgements during Ethernet updates
        "updater_ack_retries": 5,  # Number of retries for acknowledgements during Ethernet updates
        "scape_sequence": b"</AS>",  # Escape sequence for Ethernet data (encoded)
        "keepalive_sequence": b"</KA>",  # Keepalive sequence for Ethernet data (encoded)
        "receive_timeout": 0.005,  # Timeout for Ethernet data reception
        "uplink_chunk_size": 2048,  # Chunk size for Ethernet uplink data
        "network_verify": False,  # Enabled auto-diagnose network status
    },
    "mqtt": {
        "enabled": True,  # Enable MQTT functionality
        "icon_size": (100, 100),  # Size of the MQTT icon
        "name": "MQTT",  # Title of the MQTT tab
        "broker_address": "mqtt.eclipse.org",  # Default MQTT broker address
        "broker_port": 1883,  # Default MQTT broker port
        "client_id": "NeveBit",  # Client ID for MQTT connection
        "keepalive": 60,  # Keepalive interval for MQTT
        "con_retries": 5,  # Number of retries for MQTT reconnection
        "act_timeout": 2000,  # Timeout to declare MQTT connection lost in ms
        "updater_chunk_size": 4096,  # Data chunk size for MQTT updates
        "updater_ack_timeout": 0.5,  # Timeout for acknowledgements during MQTT updates
        "updater_ack_retries": 5,  # Number of retries for acknowledgements during MQTT updates
        "scape_sequence": b"</AS>",  # Escape sequence for MQTT data (encoded)
        "keepalive_sequence": b"</KA>",  # Keepalive sequence for MQTT data (encoded)
        "receive_timeout": 0.005,  # Timeout for MQTT data reception
        "uplink_chunk_size": 2048,  # Chunk size for MQTT uplink data
        "username": "",  # Default MQTT username (optional)
        "password": "",  # Default MQTT password (optional)
        "network_verify": False,  # Enabled auto-diagnose network status
    },
    "terminal": {
        "line_limit": 1000,  # Maximum number of lines in the console log
        "fade_layout_height": 30,  # Height for the stack layout container
    },
    "updater": {
        "enable_output_debug": False,  # Enable debug output for the updater
        "drag_placeholder": "Drag your firmware here or select your firmware path",
    },
    "graph": {
        "splitter_width": 600,  # Default width for splitter
        "def_title": "Graph",  # Default title of the graph widget
        "def_x_label": "X Axis",  # Default x-axis label of the graph widget
        "def_y_label": "Y Axis",  # Default y-axis label of the graph widget
        "def_samples": 100,  # Default number of samples to display in the graph
        "def_colors": [
            (255, 0, 0),  # Red
            (0, 255, 0),  # Green
            (0, 0, 255),  # Blue
            (255, 255, 0),  # Yellow
            (255, 0, 255),  # Magenta
            (0, 255, 255),  # Cyan
            (255, 128, 0),  # Orange
            (128, 0, 255),  # Purple
            (255, 0, 128),  # Pink
            (128, 255, 0),  # Lime
        ],
    },
    "debug": {
        "inhibit_uplink": False,  # Inhibit uplink data in debug mode
        "inhibit_downlink": False,  # Inhibit downlink data in debug mode
    },
}

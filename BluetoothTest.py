import tkinter as tk
import bluetooth

def receive_bluetooth_data():
    # Discover nearby Bluetooth devices
    devices = bluetooth.discover_devices(duration=2, lookup_names=True)
    if not devices:
        print("No Bluetooth devices found.")
        return

    # Create a simple GUI with a dropdown menu to select the device
    root = tk.Tk()
    root.title("Bluetooth Device Selection")
    label = tk.Label(root, text="Select a Bluetooth device:")
    label.pack(pady=10)
    device_var = tk.StringVar(root)
    device_var.set(devices[0][1])
    dropdown = tk.OptionMenu(root, device_var, *[device[1] for device in devices])
    dropdown.pack(pady=10)
    connect_button = tk.Button(root, text="Connect", command=root.quit)
    connect_button.pack(pady=10)
    root.mainloop()
    root.destroy()

    # Retrieve the address of the selected device
    device_address = None
    for device in devices:
        if device[1] == device_var.get():
            device_address = device[0]
            break
    if device_address is None:
        print("Invalid device selection.")
        return

    # Connect to the selected device and receive data
    port = 1  # The RFCOMM channel used by the Bluetooth device
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((device_address, port))
    print("Connected to {}".format(device_var.get()))
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            print(data.decode(), end='')
        except bluetooth.btcommon.BluetoothError:
            print("Connection closed.")
            break
    sock.close()

receive_bluetooth_data()
import machine

# Initialize I2C on default ESP32 pins
i2c = machine.I2C(0, sda=machine.Pin(21), scl=machine.Pin(22), freq=400000)

print("Scanning I2C bus...")
devices = i2c.scan()

if len(devices) == 0:
    print("No I2C devices found. Check your wiring!")
else:
    print("I2C devices found:")
    for device in devices:
        print(f"Decimal address: {device} | Hex address: {hex(device)}")

import serial
import serial.tools.list_ports

PortData = serial.tools.list_ports.comports()
print(PortData)
for port in PortData:
    print(f"\033[1;31m{port}\033[0m")
from bluepy.btle import Peripheral, UUID
import json

# Define the UUIDs of the service and characteristic you want to interact with
# SERVICE_UUID = "0000180a-0000-1000-8000-00805f9b34fb"  # Example: Device Information Service
# CHARACTERISTIC_UUID = "00002a29-0000-1000-8000-00805f9b34fb"  # Example: Manufacturer Name String

# MAC address of your BLE device
DEVICE_MAC_ADDRESS = "D2:B5:31:AC:FE:C5"
indent = "  "
try:
    # Connect to the peripheral
    peripheral = Peripheral(DEVICE_MAC_ADDRESS)

    # Discover services
    services = peripheral.getServices()
    # for svc in services:
        # print(f"{svc}: {svc.uuid}")

    # Find the service with the desired UUID
    service = None
    for svc in services:
        print(f"{svc.uuid}: {svc.uuid.getCommonName()}")
        for char in svc.getCharacteristics():
       #     # convert char to json and print
            # print(indent + char.uuid.getCommonName())
            print(f"{char.uuid}")
        #     if char.supportsRead():
        #         print(f"{indent*2}{char.read()}")

    # if service:
    #     # Find the characteristic with the desired UUID within the service
    #     characteristic = None
    #     for char in service.getCharacteristics():
    #         if char.uuid == UUID(CHARACTERISTIC_UUID):
    #             characteristic = char
    #             break
    #
    #     if characteristic:
    #         # Read the value of the characteristic
    #         value = characteristic.read()
    #         print("Value:", value)
    #     else:
    #         print("Characteristic not found")
    # else:
    #     print("Service not found")

finally:
    # Make sure to disconnect from the peripheral when done
    peripheral.disconnect()


from bluepy.btle import Peripheral, UUID
import json
from time import sleep

# Define the UUIDs of the service and characteristic you want to interact with
# SERVICE_UUID = "0000180a-0000-1000-8000-00805f9b34fb"  # Example: Device Information Service
# CHARACTERISTIC_UUID = "00002a29-0000-1000-8000-00805f9b34fb"  # Example: Manufacturer Name String

# MAC address of your BLE device
DEVICE_MAC_ADDRESS = "D2:B5:31:AC:FE:C5"
indent = "  "

EXCLUDED_SERVICES = [
    "00001812-0000-1000-8000-00805f9b34fb",  # Human Interface Device
]

EXCLUDED_CHARACTERISTICS = [
]

UUID_SERVICE_DEVICE_INFORMATION = "0000180a-0000-1000-8000-00805f9b34fb"
try:
    # Connect to the peripheral
    peripheral = Peripheral(DEVICE_MAC_ADDRESS)

    # Discover services
    services = peripheral.getServices()
    # for svc in services:
        # print(f"{svc}: {svc.uuid}")
        
    # JSON TEMPLATE
    # {
    #     "services": [
    #   {   "uuid": "0000180a-0000-1000-8000-00805f9b34fb",
    #           "name": "Device Information Service",
    #           "characteristics": [
    #               {
    #                   "uuid": "00002a29-0000-1000-8000-00805f9b34fb",
    #                   "properties": "READ",
    #                   "value": "Manufacturer Name"
    #               }
    #           ]
    #       }
    #    ]
    # }
    svc_dict = {}
    for svc in services:
        if svc.uuid not in EXCLUDED_SERVICES:
            svc_dict[svc.uuid.getCommonName()] = {}
            svc_dict[svc.uuid.getCommonName()]["uuid"] = str(svc.uuid)
            svc_dict[svc.uuid.getCommonName()]["characteristics"] = []
            for char in svc.getCharacteristics():
                name = char.uuid.getCommonName()
                uuid = char.uuid
                properties = char.propertiesToString()
                if "READ" in properties and uuid not in EXCLUDED_CHARACTERISTICS:
                    value = char.read()
                else:
                    value = ""
                svc_dict[svc.uuid.getCommonName()]["characteristics"].append({
                    "name": name,
                    "uuid": str(uuid),
                    "properties": properties,
                    "value": str(value)
                })
    print(json.dumps(svc_dict, indent=4))

    # # Find the service with the desired UUID
    # service = None
    # for svc in services:
    #     if svc.uuid not in EXCLUDED_SERVICES:
    #         print(f"{svc.uuid}: {svc.uuid.getCommonName()}")
    #         for char in svc.getCharacteristics():
    #             uuid = char.uuid
    #             print(f"{indent*2}{uuid}")
    #             properties = char.propertiesToString()
    #             print(f"{indent*2}{properties}")
    #             print(f"{indent*2}{char}")
    #             if "READ" in properties and uuid not in EXCLUDED_CHARACTERISTICS:
    #                 print(f"{indent*2}{char.read()}")
    #         sleep(1)
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


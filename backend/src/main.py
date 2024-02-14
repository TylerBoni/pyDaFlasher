from bluepy.btle import Peripheral, BTLEException, DefaultDelegate
from time import sleep
from utils import bytes

#import library for handling os environment variables
import os

class NotificationDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
        
    def handleNotification(self, cHandle, data):
        print("Notification:", data)
        
class FitUUIDs:
    Main_Characteristic_Write = "0000fee2-0000-1000-8000-00805f9b34fb"
    Main_Characteristic_Notify = "0000fee3-0000-1000-8000-00805f9b34fb"
    HR_Service = "0000180d-0000-1000-8000-00805f9b34fb"
    HR_Measurement_Notify = "00002a37-0000-1000-8000-00805f9b34fb"
    Service_Decive_Information = "0000180a-0000-1000-8000-00805f9b34fb"
    Characteristic_Manufacturer_Name = "00002a29-0000-1000-8000-00805f9b34fb"
    Notify_Config = "00002902-0000-1000-8000-00805f9b34fb"
    Main_Service = "0000feea-0000-1000-8000-00805f9b34fb"

class DFUActivity:
    def __init__(self):
        self.selected_name = None
        self.uri = None
        self.peripheral = None
        self.selected_mac = None
        
    # enable notifications
    def enable_notifications(self, service_uuid, characteristic_uuid):
        service = self.get_service(uuid=service_uuid)
        if service is None:
            print("BLE service is null")
        characteristic = self.get_characteristic(service, uuid=characteristic_uuid)
        if "NOTIFY" in characteristic.propertiesToString():
            print("Enabling notifications")
            self.peripheral.setDelegate(NotificationDelegate())
            valHandle = characteristic.valHandle
            print(f"valHandle = {valHandle}")
            self.peripheral.writeCharacteristic(characteristic.valHandle + 1, b"\x01\x00", withResponse=True)
            print("Notifications enabled!")
        else:
            print("This characteristic does not support notifications!")
        
    # Callback for when characteristic changes
    def handle_notification(self, cHandle, data):
        print("Notification:", data)
        self.abort_update()
        
    def send_reboot_cmd(self):
        print("Starting reboot cmd")
        self.send_cmd(0x63, bytes.int_to_byte_array(0))

    def send_update_boot_cmd(self, loadedUpdateFile):
        print("Starting boot update")
        # load binary file
        file = open(loadedUpdateFile, "rb")
        size = len(file.read())
        print(f"file_size = {size}")
        self.send_cmd(0x63, bytes.int_to_byte_array(size))  # Convert size to little-endian bytes
        rebootStarted = True
        updateStarted = True
        fullCRC = bytes.crc16(file)
        # time.sleep(30)  
    
    def abort_update(self):
        print("Aborting update")
        self.send_cmd(0x63, bytes.int_to_byte_array(0xffffffff))

    def get_service(self, uuid=FitUUIDs.Main_Service):
        services = self.peripheral.getServices()
        for service in services:
            if service.uuid == uuid:
                return service

    def get_characteristic(self, service, uuid):
        characteristics = service.getCharacteristics()
        for characteristic in characteristics:
            if characteristic.uuid == uuid:
                return characteristic

    def send_cmd(self, cmd, data):
        print("Sending command", cmd)
        print("Data:", data)
        data_length = 0
        if data is not None:
            data_length = len(data)
        startBytes = bytearray([0xFE, 0xEA, 0x10, 0x00, 0x00])
        startBytes[3] = len(startBytes) + data_length
        startBytes[4] = cmd

        if data is not None:
            cmd_bytes = startBytes + data
        else:
            cmd_bytes = startBytes
        self.write_characteristic(cmd_bytes)
        
    def wait_for_notifications(self):
        print("Waiting for notifications")
        while os.environ.get("BLE_WAIT") == "1":
            self.peripheral.waitForNotifications(5)
        print("Done waiting for notifications")

    def write_characteristic(self, data):
        if data is None:
            return "the data to be written is empty"
        else:
            try:
                service = self.get_service()
                if service is None:
                    return "BLE service is null"
                characteristic = self.get_characteristic(service, FitUUIDs.Main_Characteristic_Write)
                if "WRITE" in characteristic.propertiesToString():
                    # if callback is not None and "NOTIFY" in characteristic.propertiesToString():
                    print("Writing with callback")
                    characteristic.write(data, withResponse=True)
                    print("Wrote to Characteristic!")
                else:
                    return "This characteristic does not support write!"
            except BTLEException as e:
                print("Error:", e)
                return "Failed to write characteristic"

    def start(self):
        self.selected_mac = "D2:B5:31:AC:FE:C5"
        self.connect(self.selected_mac)
        # self.send_update_boot_cmd("../bootfiles/1_DaFitBootloader23Hacked.bin")
        # self.abort_update()
        self.send_reboot_cmd()
        self.reconnect()
        self.wait_for_notifications()
        # bytes.int_to_byte_array(4, True)

    def reconnect(self):
        i = 0
        while i < 10:
            try:
                self.connect(self.selected_mac)
                print("Reconnected to", self.selected_mac)
                return
            except BTLEException as e:
                print("Trying to reconnect...")
                i += 1
                sleep(1)
                
    def connect(self, mac_address):
        print("Connecting to", mac_address)
        self.selected_mac = mac_address
        self.peripheral = Peripheral(mac_address)
        print("Connected to", self.selected_mac)
        # self.enable_notifications(FitUUIDs.HR_Service, FitUUIDs.HR_Measurement_Notify)
        self.enable_notifications(FitUUIDs.Main_Service, FitUUIDs.Main_Characteristic_Notify)
if __name__ == "__main__":
    try:  
        self = DFUActivity()
        self.start()
    finally:
        if self.peripheral is not None:
            self.peripheral.disconnect()
        print("Disconnected from", self.selected_mac)


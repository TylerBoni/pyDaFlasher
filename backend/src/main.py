from bluepy.btle import Peripheral, Scanner, DefaultDelegate, BTLEException
from time import sleep

class FitUUIDs:
    Main_Characteristic_Write = "0000fee2-0000-1000-8000-00805f9b34fb"
    Main_Characteristic_Notify = "0000fee3-0000-1000-8000-00805f9b34fb"
    Service_Decive_Information = "0000180a-0000-1000-8000-00805f9b34fb"
    Characteristic_Manufacturer_Name = "00002a29-0000-1000-8000-00805f9b34fb"
    Notify_Config = "00002902-0000-1000-8000-00805f9b34fb"
    Main_Service = "0000feea-0000-1000-8000-00805f9b34fb"


class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print("Discovered device", dev.addr)
        elif isNewData:
            print("Received new data from", dev.addr)

class Utils:
    def int_to_byte_array(a):
        ret = bytearray(4)
        ret[3] = a & 0xFF
        ret[2] = (a >> 8) & 0xFF
        ret[1] = (a >> 16) & 0xFF
        ret[0] = (a >> 24) & 0xFF
        return bytes(ret)

    def crc16(buffer):
        crc = 0xFEEA
        for b in buffer:
            b_int = b if isinstance(b, int) else ord(b)  # Convert to integer if necessary
            crc = ((crc >> 8) | (crc << 8)) & 0xffff
            crc ^= (b_int & 0xff)
            crc ^= ((crc & 0xff) >> 4)
            crc ^= (crc << 12) & 0xffff
            crc ^= ((crc & 0xFF) << 5) & 0xffff
        crc &= 0xffff
        return bytes([(crc >> 8) & 255, crc & 255])
    
class DFUActivity:
    def __init__(self):
        self.selected_name = None
        self.uri = None
        self.peripheral = None

    def send_reboot_cmd(self):
        print("Starting reboot cmd")
        
        self.send_cmd(0x63, Utils.int_to_byte_array(0))

    def send_update_boot_cmd(self, loadedUpdateFile):
        print("Starting boot update")
        size = len(loadedUpdateFile)
        print(f"file_size = {size}")
        self.send_cmd(0x63, Utils.int_to_byte_array(size))  # Convert size to little-endian bytes
        rebootStarted = True
        updateStarted = True
        fullCRC = Utils.crc16(loadedUpdateFile)
        # time.sleep(30)  # Import the time module and use sleep function for the delay
    
    def abort_update(self):
        print("Aborting update")
        
        self.send_cmd(0x63, Utils.int_to_byte_array(0xffffffff))

    def get_dfu_service(self):
        services = self.peripheral.getServices()
        for service in services:
            if service.uuid == FitUUIDs.Main_Service:
                return service

    def get_dfu_characteristics(self, service, uuid):
        characteristics = service.getCharacteristics()
        for characteristic in characteristics:
            if characteristic.uuid == uuid:
                return characteristic

    def send_cmd(self, cmd, data):
        print("Sending command", cmd)
        print("Data:", data)
        data_length = 0
        if data is not None:
            data_lenth = len(data)
        startBytes = bytearray([0xFE, 0xEA, 0x10, 0x00, 0x00])
        startBytes[3] = len(startBytes) + data_length
        startBytes[4] = cmd

        if data is not None:
            c = startBytes + data
        else:
            c = startBytes
        print(self.write_characteristic(c))

    def write_characteristic(self, data):
        if data is None:
            return "the data to be written is empty"
        else:
            try:
                service = self.get_dfu_service()
                if service is None:
                    return "BLE service is null"
                characteristic = self.get_dfu_characteristics(service, FitUUIDs.Main_Characteristic_Write)
                if "WRITE" in characteristic.propertiesToString():
                    characteristic.write(data)
                    return "Wrote to Characteristic!"
                else:
                    return "This characteristic does not support write!"
            except BTLEException as e:
                print("Error:", e)
                return "Failed to write characteristic"
    def start(self):
        # self.send_update_boot_cmd("somefile.bin")
        # self.abort_update()
        self.send_reboot_cmd()
if __name__ == "__main__":
    try:  
        dfu_activity = DFUActivity()
        dfu_activity.selected_mac = "D2:B5:31:AC:FE:C5"  # Replace with your selected MAC address
        print("Connecting to", dfu_activity.selected_mac)
        dfu_activity.peripheral = Peripheral(dfu_activity.selected_mac)
        print("Connected to", dfu_activity.selected_mac)
        dfu_activity.start()
    finally:
        dfu_activity.peripheral.disconnect()
        print("Disconnected from", dfu_activity.selected_mac)


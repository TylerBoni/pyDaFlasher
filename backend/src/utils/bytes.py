
def int_to_byte_array(a, debug=False):
    byte_array = bytearray(4)
    byte_array[3] = a & 0xFF
    byte_array[2] = (a >> 8) & 0xFF
    byte_array[1] = (a >> 16) & 0xFF
    byte_array[0] = (a >> 24) & 0xFF
    if debug:
        print("Int to byte array:", a, "=>", byte_array)
    return bytes(byte_array)

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
    
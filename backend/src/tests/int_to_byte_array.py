from utils.bytes import int_to_byte_array

# Check if running as a script
if __name__ == "__main__":
    # Test the int_to_byte_array function
    print(int_to_byte_array(0))
    print(int_to_byte_array(1))
    print(int_to_byte_array(256))
    print(int_to_byte_array(0x12345678))
    print(int_to_byte_array(0x1234567890abcdef))
    print(int_to_byte_array(0xffffffffffffffff))
    print(int_to_byte_array(0x1234567890abcdef1234567890abcdef))
    print(int_to_byte_array(0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef))
    print(int_to_byte_array(0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef))
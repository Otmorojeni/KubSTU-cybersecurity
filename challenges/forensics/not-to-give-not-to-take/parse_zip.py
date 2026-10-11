import struct
import zlib
import binascii

with open('Not to give, not to take.zip', 'rb') as f:
    data = f.read()

print(f"Total zip file length: {len(data)} bytes")

pos = 0
entry_idx = 0
while pos < len(data):
    if not data.startswith(b'PK\x03\x04', pos):
        print(f"\nAt offset {pos} (0x{pos:x}): Not PK\\x03\\x04!")
        print(f"Remaining bytes: {len(data) - pos}")
        print(f"Remaining hex: {binascii.hexlify(data[pos:])}")
        print(f"Remaining text (latin1): {repr(data[pos:])}")
        break
    
    entry_idx += 1
    header = data[pos:pos+30]
    magic, ver, flag, method, mtime, mdate, crc, csize, usize, fn_len, extra_len = struct.unpack('<4sHHHHHIIIHH', header)
    fn_start = pos + 30
    fn_end = fn_start + fn_len
    filename_bytes = data[fn_start:fn_end]
    extra = data[fn_end:fn_end+extra_len]
    data_start = fn_end + extra_len
    data_end = data_start + csize
    file_data = data[data_start:data_end]
    
    print(f"\n=== Entry {entry_idx} at offset {pos} (0x{pos:x}) ===")
    print(f"Filename raw: {filename_bytes}")
    try:
        print(f"Filename utf-8: {filename_bytes.decode('utf-8')}")
    except:
        pass
    try:
        print(f"Filename cp437: {filename_bytes.decode('cp437')}")
    except:
        pass
    print(f"ver={ver}, flag=0x{flag:04x}, method={method}, crc=0x{crc:08x}, csize={csize}, usize={usize}, fn_len={fn_len}, extra_len={extra_len}")
    
    if method == 0:
        content = file_data
    elif method == 8:
        try:
            content = zlib.decompress(file_data, -zlib.MAX_WBITS)
        except Exception as e:
            content = f"Decompress error: {e}".encode()
    else:
        content = f"Unknown method: {method}".encode()
        
    print(f"Extracted length: {len(content)}")
    print(f"Content: {repr(content)}")
    
    pos = data_end

print(f"\nFinished at offset {pos} / {len(data)}")

import struct
import zlib
import zipfile
import io

with open('Not to give, not to take.zip', 'rb') as f:
    raw_data = f.read()

# Let's inspect all valid local entries
entries = []
pos = 0
while pos < len(raw_data):
    if raw_data.startswith(b'PK\x03\x04', pos):
        hdr_offset = pos
        header = raw_data[pos:pos+30]
        magic, ver, flag, method, mtime, mdate, crc, csize, usize, fn_len, extra_len = struct.unpack('<4sHHHHHIIIHH', header)
        fn_start = pos + 30
        fn_end = fn_start + fn_len
        filename = raw_data[fn_start:fn_end]
        extra = raw_data[fn_end:fn_end+extra_len]
        data_start = fn_end + extra_len
        
        has_dd = (flag & 0x08) != 0
        if has_dd and csize == 0:
            dd_idx = raw_data.find(b'PK\x07\x08', data_start)
            csize = dd_idx - data_start
            crc, _, usize = struct.unpack('<III', raw_data[dd_idx+4:dd_idx+16])
            next_pos = dd_idx + 16
        else:
            next_pos = data_start + csize
            
        file_bytes = raw_data[data_start:data_start+csize]
        entries.append({
            'offset': hdr_offset,
            'ver': ver,
            'flag': flag,
            'method': method,
            'mtime': mtime,
            'mdate': mdate,
            'crc': crc,
            'csize': csize,
            'usize': usize,
            'filename': filename,
            'extra': extra,
            'data': file_bytes
        })
        pos = next_pos
    else:
        break

print(f"Parsed {len(entries)} entries successfully.")

# Build repaired zip file with proper Central Directory and EOCD
cd_bytes = bytearray()
for e in entries:
    cd_header = struct.pack(
        '<4sHHHHHHIIIHHHHHII',
        b'PK\x01\x02',
        e['ver'],          # ver made by
        e['ver'],          # ver needed
        e['flag'],
        e['method'],
        e['mtime'],
        e['mdate'],
        e['crc'],
        e['csize'],
        e['usize'],
        len(e['filename']),
        0,                 # extra len
        0,                 # comment len
        0,                 # disk num start
        0,                 # internal file attr
        0,                 # external file attr
        e['offset']        # relative offset of local header
    )
    cd_bytes.extend(cd_header)
    cd_bytes.extend(e['filename'])

cd_offset = len(raw_data)
cd_size = len(cd_bytes)

eocd = struct.pack(
    '<4sHHHHIIH',
    b'PK\x05\x06',
    0,                     # number of this disk
    0,                     # disk where central directory starts
    len(entries),          # number of central directory records on this disk
    len(entries),          # total number of central directory records
    cd_size,               # size of central directory
    cd_offset,             # offset of start of central directory
    0                      # zipfile comment length
)

repaired_zip_data = raw_data + cd_bytes + eocd

with open('repaired.zip', 'wb') as f:
    f.write(repaired_zip_data)

print(f"Repaired zip created: {len(repaired_zip_data)} bytes")

# Test with standard python zipfile library
zf = zipfile.ZipFile('repaired.zip', 'r')
print("zipfile namelist:", zf.namelist())
for info in zf.infolist():
    print(f"\nFile: {info.filename}")
    try:
        content = zf.read(info)
        print(f"  Extracted ({len(content)} bytes): {content}")
    except Exception as err:
        print(f"  Extraction error: {err}")

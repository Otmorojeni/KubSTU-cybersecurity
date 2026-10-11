import zipfile
import os

zip_path = "C:\\$Recycle.Bin\\S-1-5-21-948105560-2086828028-3500341516-1001\\$R32WQ2T.zip"
if not os.path.exists(zip_path):
    print("Not found at path, searching $Recycle.Bin...")
    import glob
    for p in glob.glob("C:\\$Recycle.Bin\\**\\*.zip", recursive=True):
        print("Found zip:", p)
        zip_path = p
        break

print("Zip size:", os.path.getsize(zip_path))
with zipfile.ZipFile(zip_path, "r") as z:
    for info in z.infolist():
        print(info.filename, "CRC:", hex(info.CRC), "uncompressed:", info.file_size, "compressed:", info.compress_size, "compress_type:", info.compress_type, "comment:", info.comment)
    print("Zip comment:", z.comment)

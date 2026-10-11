import os
import inspect
import blind_watermark
from blind_watermark import WaterMark, WaterMarkCore

pkg_dir = os.path.dirname(blind_watermark.__file__)
print("Package dir:", pkg_dir)
for f in os.listdir(pkg_dir):
    print(" ", f)

# Print WaterMark.extract source
with open('wm_source.py', 'w', encoding='utf-8') as out:
    out.write("### WaterMark.__init__\n")
    out.write(inspect.getsource(WaterMark.__init__))
    out.write("\n\n### WaterMark.extract\n")
    out.write(inspect.getsource(WaterMark.extract))
    out.write("\n\n### WaterMarkCore.__init__\n")
    out.write(inspect.getsource(WaterMarkCore.__init__))
    out.write("\n\n### WaterMarkCore.extract_with_kmeans\n")
    try:
        out.write(inspect.getsource(WaterMarkCore.extract_with_kmeans))
    except Exception as e:
        out.write(str(e))
    out.write("\n\n### WaterMarkCore.extract\n")
    try:
        out.write(inspect.getsource(WaterMarkCore.extract))
    except Exception as e:
        out.write(str(e))
print("Saved to wm_source.py")

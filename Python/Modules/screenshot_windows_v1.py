import ctypes
from ctypes import wintypes
import struct
import os

SRCCOPY = 0x00CC0020

class BITMAPINFOHEADER(ctypes.Structure):
    _fields_ = [
        ('biSize', wintypes.DWORD),
        ('biWidth', wintypes.LONG),
        ('biHeight', wintypes.LONG),
        ('biPlanes', wintypes.WORD),
        ('biBitCount', wintypes.WORD),
        ('biCompression', wintypes.DWORD),
        ('biSizeImage', wintypes.DWORD),
        ('biXPelsPerMeter', wintypes.LONG),
        ('biYPelsPerMeter', wintypes.LONG),
        ('biClrUsed', wintypes.DWORD),
        ('biClrImportant', wintypes.DWORD)
    ]

class BITMAPINFO(ctypes.Structure):
    _fields_ = [
        ('bmiHeader', BITMAPINFOHEADER),
        ('bmiColors', wintypes.DWORD * 3)
    ]

user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32

screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)

desktop_dc = user32.GetDC(0)
memory_dc = gdi32.CreateCompatibleDC(desktop_dc)
bitmap = gdi32.CreateCompatibleBitmap(desktop_dc, screen_width, screen_height)

if not bitmap:
    raise Exception("Could not create compatible bitmap.")

gdi32.SelectObject(memory_dc, bitmap)

success = gdi32.BitBlt(
    memory_dc, 0, 0, screen_width, screen_height,
    desktop_dc, 0, 0, SRCCOPY
)

if not success:
    raise Exception("BitBlt failed.")

bmp_header = struct.pack('<2sL2HL', b'BM', 14 + 40 + screen_width * screen_height * 3, 0, 0, 14 + 40)
dib_header = BITMAPINFO()
dib_header.bmiHeader.biSize = ctypes.sizeof(BITMAPINFOHEADER)
dib_header.bmiHeader.biWidth = screen_width
dib_header.bmiHeader.biHeight = screen_height
dib_header.bmiHeader.biPlanes = 1
dib_header.bmiHeader.biBitCount = 24
dib_header.bmiHeader.biCompression = 0  
dib_header.bmiHeader.biSizeImage = screen_width * screen_height * 3
file_path = os.path.join(os.getcwd(), 'screenshot.bmp')

buffer_size = screen_width * screen_height * 3
buffer = ctypes.create_string_buffer(buffer_size)

gdi32.GetDIBits(
    memory_dc, bitmap, 0, screen_height, buffer,
    ctypes.byref(dib_header), 0
)

with open(file_path, 'wb') as f:
    f.write(bmp_header)
    f.write(ctypes.string_at(ctypes.byref(dib_header), ctypes.sizeof(dib_header)))
    f.write(buffer)

gdi32.DeleteObject(bitmap)
gdi32.DeleteDC(memory_dc)
user32.ReleaseDC(0, desktop_dc)

print(f'Screenshot saved as {file_path}')

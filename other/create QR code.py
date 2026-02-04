import os

try:
    import pyqrcode
except:
    os.system('pip install pyqrcode')
    os.system('pip install pypng')
    import pyqrcode
    
data = "https://chat.whatsapp.com/Bbr8XRSlaQsF9fcPEyo9ZX"

qr=pyqrcode.create(data)
file_name="last"

if '.png' not in file_name:
	file_name+='.png'
qr.png(file_name,scale=8)

print('QR code created....')
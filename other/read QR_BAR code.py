import os
try:
    from pyzbar.pyzbar import decode
except:
    os.system('pip install pyzbar')
    from pyzbar.pyzbar import decode


from PIL import Image

file= input('Give QR/BAR code name you want to read :- ')

if '.png' not in file:
	file+='.png'

d= decode(Image.open(file))

print('The data in QR code is :- ',end='')
print(d[0].data.decode('ascii'))
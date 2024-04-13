from PIL import Image

img = Image.open("clouds.jpg")
print(img.size)
img.crop((178, 40, 172, 85))
img.show()
# img.save("cloud.png")

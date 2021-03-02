import PIL.Image
import requests

asciiChars = ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.']

def ResizeImage(image):
    width, height = image.size
    largestValue = max(width, height)
    ratio = 100/largestValue
    newWidth = int(ratio*width)
    newHeight = int(ratio*height)
    resizedImage = image.resize((newWidth, newHeight))
    resizedImage.save("testPic.jpg")
    return(resizedImage, newWidth)

def ResizeImageLarge(image):
    width, height = image.size
    largestValue = max(width, height)
    ratio = 1000/largestValue
    newWidth = int(ratio*width)
    newHeight = int(ratio*height)
    resizedImage = image.resize((newWidth, newHeight))
    resizedImage.save("testPic.jpg")
    return(resizedImage, newWidth)

def grayScale(image):
    grayscaleImage = image.convert('L')
    return(grayscaleImage)

def pixelToASCII(image):
    pixels = image.getdata()
    characters = ''.join([asciiChars[pixel//25] for pixel in pixels])
    return(characters)

def convert(imagePath):
    image = PIL.Image.open(requests.get(imagePath, stream=True).raw)
    if(image.mode == "RGBA"):
        image = image.convert('RGB')
    resizedImage, newWidth = ResizeImage(image)
    newImageData = pixelToASCII(grayScale(resizedImage))
    pixelCount = len(newImageData)
    asciiImage = '\n'.join(newImageData[i:(i+newWidth)] for i in range(0, pixelCount, newWidth))
    with open("AsciiArt.txt", 'w') as file:
        file.write(asciiImage)
        return file


def convertLarge(imagePath):
    image = PIL.Image.open(requests.get(imagePath, stream=True).raw)
    if(image.mode == "RGBA"):
        image = image.convert('RGB')
    resizedImage, newWidth = ResizeImageLarge(image)
    newImageData = pixelToASCII(grayScale(resizedImage))
    pixelCount = len(newImageData)
    asciiImage = '\n'.join(newImageData[i:(i+newWidth)] for i in range(0, pixelCount, newWidth))
    with open("AsciiArtLarge.txt", 'w') as file:
        file.write(asciiImage)
        return file
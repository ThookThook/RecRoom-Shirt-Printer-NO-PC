from PIL import Image, ImageFilter; # ImageOps, ImageEnhance;
import typing;

def main(symbols, imgPath):
  print("\nColor Compiler 5.2");
  selection = str(input("Do you want to compile? (y/n):\n "))
  if (selection in ("y", "Y", "yes", "Yes", "YES", "yes.", "Yes.", "YES.")):
      print("  Select image file to compile")
  else:
      return
  try: #File error detection
      try:
          img = Image.open(imgPath)
      except(ReferenceError): # guess that will do
          print("")
          print("Invalid image type - only use PNG, JPEG, or JFIF")
          print("")
          quit()
  except AttributeError:
      print("Error - file window closed")
      print("")
      quit()
  
  img = img.convert('RGB')
  imgPath = str(imgPath)
  imgPath = imgPath.split('/')
  imgPath = imgPath[len(imgPath)-1]
  try:
      imgPath = imgPath.replace('.png','')
  except:
      try:
          imgPath = imgPath.replace('.jpg','')
      except:
          try:
              imgPath = imgPath.replace('.jfif','')
          except:
              try:
                  imgPath = imgPath.replace('.jpeg','')
              except:
                  pass
  
  print("  1 marker is minmum 113 is maximum")
  img.load()
  coloramount = int(input("Enter amount of colors: "))
  if (coloramount < 1):
      print("")
      print("Color amount too small - 1 is minmum amount")
      print("")
      quit()
  elif (coloramount > 113):
      print("")
      print("Color amount too large - 113 is maximum amount")
      print("")
      quit()
  else:
      pass
  print("   0 = Median Cut - Has best color detection")
  print("   1 = Maximum Coverage - Use for special circumstances")
  print("   2 = Fast Octree - Use this method it works the best")
  colortype = int(input("Enter type of quantization: "))
  try:
      quant = img.quantize(colors=coloramount,method=colortype)
  except ValueError:
      print("")
      print("Quantization method not recognized - enter valid integer")
      print("")
      quit()
  
  count = coloramount*3
  palette = (quant.getpalette()[:count])
  maximum = int(len(palette)-2)
  hexcolors = []
  rgbcolors = []
  i = 0
  if (coloramount > 0 and coloramount <= 113):
      for i in (range(maximum)):
          if (i%3 == 0):
              rgb = palette[i],palette[i+1],palette[i+2]
              hexcolor = str(rgbToHex(rgb))
              rgbcolors.append(str(rgb) + ': "' + str(symbols[i]) + '",')
              hexcolors.append(hexcolor)
              i += 1
          else:
              i += 1
  else:
      for i in (range(maximum)):
          if (i%3 == 0):
              rgb = palette[i],palette[i+1],palette[i+2]
              hexcolor = str(rgbToHex(rgb))
              rgbcolors.append(str(rgb))
              hexcolors.append(hexcolor)
              i += 1
          else:
              i += 1
  print(str(coloramount) + " colors compiled")
  print("")
  heximgPath = "Hex Colors.txt"
  with open(heximgPath, 'w') as file1:
      file1.write('\n'.join(hexcolors))
  print("Text file written & colors set")
  dict = {}
  for elem in rgbcolors:
    dict[eval(elem[0:elem.index(":")])] = elem[elem.index(":")+3]
  return dict



def rgbToHex(rgb): return('#%02x%02x%02x' % rgb)

def hexToRGB(hex):
  hex = str(hex)
  hex = hex.replace('#','')
  return(tuple(int(hex[i:i+2], 16) for i in (0, 2, 4)))

def printBreak(number):
  for i in range(number):
      print("")


def dilate(cycles, image):
  for i in range(cycles):
      image = image.filter(ImageFilter.MaxFilter(3))
      return image

def erode(cycles, image):
  for i in range(cycles):
      image = image.filter(ImageFilter.MinFilter(3))
      return image

import time
from math import sqrt
from pathlib import Path
from typing import Tuple, List
from PIL import Image, ImageFilter  # PIL is the only required import


# Varibles:
NAME = "Color Compiler + Mcren's String Importer"
VERSION = "1.00"
IMAGE_PATH = "Image.png"

# Color Compiler's symbols
SYMBOLS = ['!','','','#','','','$','','','%','','','&','','','(','','',')','','','*','','','+','','',',','','','.','','','/','','',':','','',';','','','<','','','=','','','>','','','?','','','@','','','[','','','Ñ','','',']','','','^','','','_','','','{','','','|','','','}','','','~','','','¢','','','£','','','¤','','','¥','','','¦','','','§','','','¨','','','©','','','ª','','','«','','','¬','','','Ö','','','®','','','¯','','','°','','','±','','','²','','','³','','','´','','','µ','','','¶','','','·','','','¸','','','¹','','','º','','','»','','','¼','','','½','','','¾','','','¿','','','À','','','È','','','ß','','','Ä','','','ê','','','ö','','','Ø','','','Ð','','','Ý','','','ä','','','î','','','Œ','','','Ç','','','Ž','','','ÿ','','','Ú','','','É','','','Ê','','','Æ','','','Ë','','','Ù','','','Ü','','','a','','','ƒ','','','ñ','','','å','','','Å','','','ë','','','Ï','','','ï','','','ù','','','ý','','','Ã','','','Â','','','ž','','','Á','','','Ò','','','Ì','','','Í','','','Ó','','','Ô','','','Õ','','','€','','','Š','','','†','','','‡','','','™','','','š','','','œ','','','Ÿ','','','Û','','','ã','','','â','','','ð','','','õ','','']

# Actual symbols list without spaces.
SYMBOLS_LIST = ["!","#","$","%","&","(",")","*","+",",",".","/",";",":","<","=",">","?","@","[","Ñ","]","^","_","{","|","}","~","¢","£","¤","¥","¦","§","¨","©","ª","«","¬","Ö","®","¯","°","±","²","³","´","µ","¶","·","¸","¹","º","»","¼","½","¾","¿","À","È","ß","Ä","ê","ö","Ø","Ð","Ý","ä","î","Œ","Ç","Ž","ÿ","Ú","É","Ê","Æ","Ë","Ù","Ü","a","ƒ","ñ","å","Å","ë","Ï","ï","ù","ý","Ã","Â","ž","Á","Ò","Ì","Í","Ó","Ô","Õ","€","Š","†","‡","™","š","œ","Ÿ","Û","ã","â","ð","õ"]

# Mcren's String encoder colors/symbols: 
# All of RecRoom color in order + tan marker + eraser
rrPalette = {
  (228, 80, 80): "!",
  (211, 23, 24): "#",
  (117, 7, 6): "$",
  (123, 47, 47): "%",
  (239, 127, 79): "&",
  (245, 92, 25): "(",
  (193, 55, 9): ")",
  (127, 66, 47): "*",
  (247, 215, 106): "+",
  (244, 197, 31): ",",
  (181, 99, 0): ".",
  (130, 97, 56): "/",
  (137, 177, 81): ":",
  (105, 161, 24): ";",
  (47, 76, 9): "<",
  (66, 82, 43): "=",
  (103, 190, 122): ">",
  (16, 101, 34): "?",
  (6, 59, 17): "@",
  (51, 76, 55): "[",
  (103, 218, 205): "Ñ",
  (0, 155, 137): "]",
  (0, 80, 71): "^",
  (51, 86, 82): "_",
  (101, 199, 236): "{",
  (2, 172, 234): "|",
  (6, 87, 117): "}",
  (49, 91, 105): "~",
  (100, 161, 244): "¢",
  (23, 107, 221): "£",
  (7, 57, 128): "¤",
  (50, 79, 121): "¥",
  (165, 133, 242): "¦",
  (80, 24, 221): "§",
  (46, 18, 120): "¨",
  (86, 72, 121): "©",
  (225, 148, 242): "ª",
  (121, 66, 131): "«",
  (66, 24, 74): "¬",
  (88, 61, 92): "Ö",
  (238, 120, 178): "®",
  (234, 46, 79): "¯",
  (130, 9, 63): "°",
  (104, 56, 78): "±",
  (126, 64, 25): "²",
  (69, 40, 22): "³",
  (61, 29, 14): "´",
  (36, 16, 5): "µ",
  (197, 132, 92): "¶",
  (143, 99, 72): "·",
  (90, 62, 48): "¸",
  (37, 28, 21): "¹",
  (246, 239, 233): "º",
  (192, 188, 185): "»",
  (153, 149, 146): "¼",
  (124, 120, 119): "½",
  (99, 100, 102): "¾",
  (73, 74, 78): "¿",
  (45, 46, 50): "À",
  (25, 23, 24): "È",
}

MaxStringLength: int = 512  # Maximum length string


# Typing alias for color
PixelColor = Tuple[int, int, int]



# the color comipler
def colorCompiler(symbols):
  print("")
  print(str(NAME) + " " + str(VERSION))
  selection = str(input("Do you want to compile? (y/n):\n "))
  if (selection in ["y", "Y", "yes", "Yes", "YES", "yes.", "Yes.", "YES."]):
      print("  Select image file to compile")
  else:
      return

  imgPath = IMAGE_PATH
  try: #File error detection
      try:
          img = Image.open(imgPath)
      except:
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


# color compiler functions:
def rgbToHex(rgb):
  return('#%02x%02x%02x' % rgb)

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







# Function to write compiled strings to a text file
        # Function to write compiled strings to a text file
def write_strings_to_file(strings, max_length=512):
  with open("Image Data.txt", "w", encoding="UTF-8") as file:
      for i in range(0, len(strings), max_length):
          file.write(("\n".join(strings[i:i + max_length]) + "\n").strip())
  with open("Image Data 2.txt", "w", encoding="UTF-8") as file:
    for i in range(0, len(strings), max_length):
        file.write(("\n\n".join(strings[i:i + max_length]) + "\n\n").strip())



def closest_color(pixel_color: PixelColor) -> PixelColor:
  """
  Take an RGB value and find the closest color in `RR_PALETTE`

  It is recommended you use external programs to convert and dither images.
  2 ACO (swatch) files are included if you're using Photoshop

  :param pixel_color: The color of the pixel of the image
  :return: The color from `RR_PALETTE` that is closest to `pixel_color`
  """
  r, g, b = pixel_color
  color_diffs: List[tuple[float, PixelColor]] = []
  for key in rrPalette:
      cr, cg, cb = key
      color_diff = sqrt((r - cr) ** 2 + (g - cg) ** 2 + (b - cb) ** 2)
      color_diffs.append((color_diff, key))
  return min(color_diffs)[1]

# Rest of your functions here...
def progress_update(y: int, img: Image, prefix='Progress', suffix='', length=50) -> None:
    """
    Display a progress bar in the console
    :param y: The `y` value of the image
    :param img: The image
    :param prefix: Optional: Text in-front of the progress bar
    :param suffix: Optional: Text behind the progress bar
    :param length: Optional: The length of the progress bar
    """
    completed = int(length * y // img.height)
    empty = length - completed
    bar = "#" * completed + " " * empty
    percent = f"{100 * (y / float(img.height)):.2f}"
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end="\r")

    # Print New Line on Complete
    if y == img.height:
        print(" " * (length + 30), end="\r")

def quantize(img, ask_for_dither: bool = True, dither: int = 0, open_image: bool = True) -> Image:
    img = img.convert("RGB")

    if ask_for_dither:
        dither = 0 if "n" in input("Dither the image? [y/n] ").lower() else 1

    palette_image = Image.new("P", img.size)
    palette_image.putpalette(ALL_COLORS)
    new_image = img.quantize(palette=palette_image, dither=dither).convert("RGB")

    if open_image:
        print("Opening the final image...")
        new_image.show()

    new_image.save("Preview Image.png", format="PNG")
    return new_image

def encode(img: Image, vertical_print: bool = False, dither_: bool = True):
    """
    Take an image and encode it into a list of {`MaxStringLength`}-char strings.
    ...[number of pixels][color]...

    :param img: The image to be encoded.
    :param vertical_print: Encode the image vertically (for Ashers printer)
    :param dither_: Should the image be dithered
    :return: List of {`MaxStringLength`} char long strings
    """
    pixel_color: List[str] = []
    full_image = Image.new("RGB", img.size)
    dither = False

    # Just so pycharm doesn't complain
    x, y = 0, 0

    if dither_:
        img = quantize(img)

    # `vertical_print` just changes the orientation of the encoding process.
    for y in range(img.height):
        for x in range(img.width):
            p = img.getpixel((y, x) if vertical_print else (x, y))  # Gets the color of the pixel at `x, y`
            if len(p) == 4:  # If the value is RGBA, the last `int` is removed
                p = p[:3]
            try:
                # Check if the image has already been dithered, else find the closest color
                p = rrPalette[p]
            except KeyError:
                dither = True
                p = closest_color(p)
                full_image.putpixel((y, x) if vertical_print else (x, y), p)
                p = rrPalette[p]
                # closest_color(p)
            pixel_color.append(p)
        # Print the progress
        progress_update(y + 1, img, "Encoding")

    if dither and dither_:
        full_image.show()

    colors: List[Tuple[int, str]] = []
    count: int = 0
    current_color: str = pixel_color[0]
    # `count` is the amount of `current_color` in a row

    for c in pixel_color:
        if c != current_color:
            colors.append((count, current_color))
            count = 0
            current_color = c
        count += 1
    colors.append((count, current_color))

    print(f"Compressed {len(pixel_color)} chars into {len(colors)} chars")

    s: str = ""
    img_data: List[str] = []
    for amount, color in colors:
        if amount > 1:
            ns = f"{amount}{color}"
        else:
            ns = color

        if len(s + ns) > MaxStringLength:  # 512
            img_data.append(s)
            s = ""
        s += ns

    img_data.append(s)
    return img_data

def stringEncoder(list_size: int):
    """
    Function to tie together all others.
    Prompt for image, encode and output

    :param list_size: The max list size; 50 for `Variable` importing, 64 for `List Create` importing
    :param output_strings: Print the encoded image strings into the console
    :param wait_for_input: Wait for the user to continue. Useful when running this file directly so that it stays open
    """

    if not img:
        exit()

    img_data = encode(img)

    print("Copying strings\n_______________\n")
    time.sleep(2)
    # Print amount of {`MaxStringLength`} char long strings, image dimensions and total `List Create`s needed.
    print(f"\nGenerated {len(img_data)} strings for image WxH {img.width}x{img.height}")
    print(f"Space needed: {len(img_data) // list_size} Lists (+ {len(img_data) % list_size})")
  
    return img_data
# end

#colorCompiler(SYMBOLS)

option = int(input("""Select color option:
1.Aquire them from image.
2.Input colors manually.
3.Use default colors from the Rec Room color pallete.\n\nanswer: """));

# Using the color compiler
if option == 1:
  rrPalette = colorCompiler(SYMBOLS);

#inputing colors manually
elif option == 2:
  count: int = len(SYMBOLS_LIST);
  rgbString: str = "";
  print("Please enter colors in the format of \"(R,G,B)\",\npress enter to stop\n there currently is a max of 113 colors availible.");
  rrPalette = {};
  for i in SYMBOLS_LIST:
    #try:
    print(f"{count} colors available...")
    color = input("Enter a color: ");
    if(color == ""): break
    rgbString += str(rgbToHex(eval(color))) + "\n";
    rrPalette[eval(color)] = i;
    --count; # count-- doesn't work for some reason???
    with open("Hex Colors.txt", "w", encoding="UTF-8") as file:
        file.write(rgbString);
    except:
        print("Error!! Please try restart the program and input the color values correctly, thank you.");
        time.sleep(4);
        exit();

# use default colors.
else: pass;

# All the RecRoom colors in one list. [R, G, B, R, G, B,...]
ALL_COLORS = [num for tup in rrPalette.keys() for num in tup];
importMethod = int(input("1. Variable Import\n2. List Create Import\n> "))
# set list size.
list_size = 50
if(importMethod == 2): list_size = 64;
# Load the image
img = Image.open(IMAGE_PATH);
# Write the compiled strings to the text file
write_strings_to_file(stringEncoder(list_size))

print("Image data saved")

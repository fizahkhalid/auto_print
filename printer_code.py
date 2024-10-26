import win32ui
import win32con
import win32print
from PIL import Image, ImageWin

def initialize_printer():
    printer_name = win32print.GetDefaultPrinter()
    hDC = win32ui.CreateDC()
    hDC.CreatePrinterDC(printer_name)
    printable_area = (hDC.GetDeviceCaps(win32con.HORZRES), hDC.GetDeviceCaps(win32con.VERTRES))
    printer_size = (hDC.GetDeviceCaps(win32con.PHYSICALWIDTH), hDC.GetDeviceCaps(win32con.PHYSICALHEIGHT))
    printer_margins = (hDC.GetDeviceCaps(win32con.PHYSICALOFFSETX), hDC.GetDeviceCaps(win32con.PHYSICALOFFSETY))
    return hDC, printable_area, printer_size, printer_margins

def calculate_scale(image, printable_area):
    ratios = [1.0 * printable_area[0] / image.size[0], 0.5 * printable_area[1] / image.size[1]]
    return min(ratios)

def print_image(hDC, image, printer_size, printer_margins, scale, start_height):
    dib = ImageWin.Dib(image)
    scaled_width, scaled_height = [int(scale * i) for i in image.size]
    x1 = int((printer_size[0] - scaled_width) / 2)
    y1 = start_height
    x2 = x1 + scaled_width
    y2 = y1 + scaled_height
    dib.draw(hDC.GetHandleOutput(), (x1, y1, x2, y2))
    return y2

def print_two_images(image1_path, image2_path):
    image1 = Image.open(image1_path).convert('L') 
    image2 = Image.open(image2_path).convert('L') 
    
    hDC, printable_area, printer_size, printer_margins = initialize_printer()
    
    scale1 = calculate_scale(image1, printable_area)
    scale2 = calculate_scale(image2, printable_area)
    
    hDC.StartDoc("auto printing two images")
    hDC.StartPage()
    
    # Print the first image at the top of the page
    y_end_first_image = print_image(hDC, image1, printer_size, printer_margins, scale1, printer_margins[1])
    
    # Print the second image right below the first image
    print_image(hDC, image2, printer_size, printer_margins, scale2, y_end_first_image)
    
    hDC.EndPage()
    hDC.EndDoc()
    hDC.DeleteDC()
from email.mime import image
import sys, os, cv2, numba
import time as tm
from numba import jit
# from python_color2grey import python_color2grey
# from numpy_color2grey import numpy_color2grey
from . import python_color2grey
from . import numpy_color2grey

@jit(nopython=True)
def greyscale_filter(image):
    """
    Takes image as input of extention with '.jpg', '.png', '.jpeg', '.bmp', returns grey_scale version. Weighted sum of RGB values are 0.07, 0.72 and 0.21 respectively.
    Channel orders are 0(B), 1(G) and 2(R).
    
    Args:
        image (ndarry): 3D NumPy array of the image stored with dementions as [rows, columns, channels]. 
    Returns:
        image (ndarray): the grey_scaled image with item values of the set weighted values as unit8 type.
    """
    image = image[:, :, 0]*0.07 + image[:, :, 1]*0.72 + image[:, :, 2]*0.21
    return image


def numba_color2grey(filename):
    """
    Takes the given image file, process it and save it to grey scale.
    Args:
        The image file to be processed.
    """
    ext = os.path.splitext(filename)[-1].lower()
    picext = ['.jpg', '.png', '.jpeg', '.bmp']
    try:
        if ext in picext:
            with open(filename, 'r') as f:
                pass
    except Exception as InvalidExt:
        print(f'The file must be of image type: {InvalidExt}!')

    image = cv2.imread(filename)
    global demension
    demension = image.shape
    pythonname = sys.argv[0].strip('.\\').split('.')
    greyed_image = greyscale_filter(image)
    cv2.imwrite(f"{pythonname[0]}_greyscale{ext}", greyed_image)

def report(filename):
    """
    Record the time and its average of greyscale_filter() for 3 runs.
    The time and avg_time is then write to python report color2grey.txt
    Args:
        The image file to be processed.
    """
    python0=tm.perf_counter()
    for i in range(3):
        python_color2grey(filename)
    python1=tm.perf_counter()
    pythont=(python1 - python0)/3
    
    numpy0=tm.perf_counter()
    for i in range(3):
        numpy_color2grey(filename)
    numpy1=tm.perf_counter()
    numpyt=(numpy1 - numpy0)/3
    
    numba0=tm.perf_counter()
    for i in range(3):
        numba_color2grey(filename)
    numba1=tm.perf_counter()
    numbat=(numba1 - numba0)/3
    
    with open(f"numba_report_color2grey.txt", "w") as f:
        f.write("Timing : python_color2grey\n")
        f.write(f"Image demension: {demension}\n")
        f.write(f"Average runtime running python_color2grey after 3 runs : {numbat} s\n")
        f.write(f"Average runtime of numba_color2grey is {pythont/numbat:.3f} times faster than python_color2grey\n")
        f.write(f"Average runtime of numba_color2grey is {numpyt/numbat:.3f} times slower than numpy_color2grey\n")
        f.write("Timing performed using: time.perf_counter()\n")


if __name__ == "__main__":
    report('rain.jpg')
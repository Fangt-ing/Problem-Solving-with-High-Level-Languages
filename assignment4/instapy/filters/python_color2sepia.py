import os, sys, cv2
import time as tm


def sepia_filter(image):
    """
    Takes image as input of extention with '.jpg', '.png', '.jpeg', '.bmp', returns sepia_scale version. Weighted sum of RGB values are 0.07, 0.72 and 0.21 respectively.
    Channel orders are 0(B), 1(G) and 2(R).
    
    Args:
        image (ndarry): 3D NumPy array of the image stored with dementions as [rows, columns, channels]. 
    Returns:
        image (ndarray): the sepia_scaled image with item values of the set weighted values as unit8 type.
    """
    # multiply each color value in the corresponding channel of a pixel 
    # with the RGB ordered matrix given here
    sepia = [[0.393, 0.769, 0.189], [0.349, 0.686, 0.168], [0.272, 0.534, 0.131]]
    for rw in range(len(image)):  # rows
        for cl in range(len(image[rw])):  # columns
            image[rw, cl, 2] = sum(image[rw, cl, ch] * sepia[0][ch] for ch in range(3))
            image[rw, cl, 1] = sum(image[rw, cl, ch] * sepia[1][ch] for ch in range(3))
            image[rw, cl, 0] = sum(image[rw, cl, ch] * sepia[2][ch] for ch in range(3))
    return image


def python_color2sepia(filename):
    """
    Takes the given image file, process it and save it to sepia scale.
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
    # image = cv2.resize(image, (0, 0), fx=0.5, fy=0.5)
    global demension
    demension = image.shape
    pythonname = sys.argv[0].strip('.\\').split('.')
    sepia_image = sepia_filter(image.astype('uint16'))
    cv2.imwrite(f"{pythonname[0]}{ext}", sepia_image)


def report(filename):
    """
    Record the time and its average of sepia_filter() for 3 runs.
    The time and avg_time is then write to python report color2sepia.txt
    Args:
        The image file to be processed.
    """

    ts = tm.perf_counter()  # ts = time start
    for i in range(3):
        python_color2sepia(filename)
    te = tm.perf_counter()  # te = time end
    avg_time = (te - ts) / 3

    with open(f"python_report_color2sepia.txt", "w") as f:
        f.write("Timing : python_color2sepia\n")
        f.write(f"Image demension: {demension}\n")
        f.write(
            f"Average runtime running python_color2sepia after 3 runs : {avg_time:f} s\n"
        )
        f.write("Timing performed using: time.perf_counter()\n")


if __name__ == "__main__":
    report('rain.jpg')
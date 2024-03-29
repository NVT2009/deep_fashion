import cv2
import numpy as np

# face, hair,
upper_colour_label = [(255,0,0), (0,0,255)]
# LeftLeg, RightLeg, LeftShoe, RightShoe
#lower_colour_label = [(170,255,85), (85,255,170),(0,255,255),(0,170,255)]
lower_colour_label = [(0,255,255),(0,170,255)]


def check_background_color(dir_image, parsing_img):
    origin_image = cv2.imread(dir_image)
    pil_image = parsing_img.convert('RGB')
    open_cv_image = np.array(pil_image)
    # Convert RGB to BGR
    parsing_img = open_cv_image[:, :, ::-1].copy()

    temp = cv2.inRange(parsing_img, (0,0,0), (0,0,0))
    seg_binary = np.where((temp > 0),1,0).astype(dtype='uint8')
    re_image = seg_binary[:,:, np.newaxis] * origin_image
    num_range = np.mean(re_image)
    if num_range > 160:
        return True


def check_full_body(parsing_img):
    upper =[]
    lower = []
    pil_image = parsing_img.convert('RGB')
    open_cv_image = np.array(pil_image)
    # Convert RGB to BGR
    parsing_img = open_cv_image[:, :, ::-1].copy()
    for colour in upper_colour_label:
        temp = cv2.inRange(parsing_img, colour, colour)
        if np.sum(temp) != 0:
            upper.append(temp)

    if len(upper) > 0:
        for colour in lower_colour_label:
            temp = cv2.inRange(parsing_img, colour, colour)
            if np.sum(temp) != 0:
                lower.append(temp)

        if len(lower) > 0:
            return True
        else:
            return False
    else:
        return False

import os

import math
from PIL import Image


def overlay_image(RES_R,
                  over_img,
                  base_img,
                  x_offset=0,
                  y_offset=0):
    x1, x2 = x_offset * RES_R, x_offset * RES_R + over_img.shape[1]
    y1, y2 = y_offset * RES_R, y_offset * RES_R + over_img.shape[0]
    alpha_s = over_img[:, :, 3] / 255.0
    alpha_l = 1.0 - alpha_s

    for c in range(0, 3):
        base_img[y1:y2, x1:x2, c] = (alpha_s * over_img[:, :, c] + alpha_l * base_img[y1:y2, x1:x2, c])
    base_img[y1:y2, x1:x2, 3] = over_img[:, :, 3]
    return base_img


def cut_image(RES_R,
              img,
              y1, y2,
              x1, x2):
    return img[y1 * RES_R:y2 * RES_R, x1 * RES_R:x2 * RES_R, :]


def detect_resolution(block_path,
                      item_path):
    """
    Tries to detect the resolution of the pack

    :param block_path:
    :param item_path:
    :return:
    """
    if os.path.exists(block_path):
        searchfold = block_path
    elif os.path.exists(item_path):
        searchfold = item_path
    else:
        return False

    selected = list(file for file in os.listdir(searchfold)
                    if file.endswith('.png'))[0]

    tex = Image.open(f"{searchfold}/{selected}")
    # print(tex.size)

    ro = 1
    while math.pow(2, ro) < (tex.size[0] / 16):
        ro += 1

    # print('resolution: ' + str(tex.size[0]) + '  ro: ' + str(ro))

    if ro < 0:
        ro = 0

    return ro

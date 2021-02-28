import numpy as np
from PIL import Image
from loguru import logger

from src.util.image_util import overlay_image, cut_image


def reposition_horse_texture(RES_R,
                             dir,
                             file):
    """
    Repositions the elements in the horse textures

    :param RES_R:
    :param dir:
    :param file:
    :return:
    """
    logger.info(f"Repositioning {file}...")

    try:
        path = dir + file
        h_img = Image.open(path).convert("RGBA")
        h_img = h_img.resize((128 * RES_R, 128 * RES_R), Image.NEAREST)
        h_arr = np.array(h_img)

        n_h_arr = np.zeros((64 * RES_R, 64 * RES_R, 4), dtype=np.uint8)

        # head
        n_h_arr = overlay_image(RES_R, cut_image(RES_R, h_arr, 0, 12, 0, 24), n_h_arr, 0, 13)
        n_h_arr = overlay_image(RES_R, cut_image(RES_R, h_arr, 0, 12, 9, 24), n_h_arr, 10, 13)
        n_h_arr = overlay_image(RES_R, cut_image(RES_R, h_arr, 0, 7, 14, 17), n_h_arr, 16, 13)
        n_h_arr = overlay_image(RES_R, cut_image(RES_R, h_arr, 7, 12, 21, 24), n_h_arr, 23, 20)

        # ear
        n_h_arr = overlay_image(RES_R, cut_image(RES_R, h_arr, 12, 20, 0, 6), n_h_arr, 0, 12)
        n_h_arr = overlay_image(RES_R, cut_image(RES_R, h_arr, 0, 4, 0, 6), n_h_arr, 19, 16)

        # morth
        n_h_arr = overlay_image(RES_R, cut_image(RES_R, h_arr, 19, 27, 25, 43), n_h_arr, 0, 25)
        n_h_arr = overlay_image(RES_R, cut_image(RES_R, h_arr, 32, 34, 24, 42), n_h_arr, 0, 33)
        n_h_arr = overlay_image(RES_R, cut_image(RES_R, h_arr, 27, 32, 33, 37), n_h_arr, 9, 25)

        # neck
        n_h_arr = overlay_image(RES_R, cut_image(RES_R, h_arr, 21, 33, 0, 7), n_h_arr, 0, 42)
        n_h_arr = overlay_image(RES_R, cut_image(RES_R, h_arr, 21, 33, 8, 12), n_h_arr, 7, 42)
        n_h_arr = overlay_image(RES_R, cut_image(RES_R, h_arr, 21, 33, 13, 20), n_h_arr, 11, 42)
        n_h_arr = overlay_image(RES_R, cut_image(RES_R, h_arr, 21, 33, 20, 24), n_h_arr, 18, 42)

        n_h_arr = overlay_image(RES_R, cut_image(RES_R, h_arr, 12, 19, 8, 16), n_h_arr, 7, 35)

        # horsehair
        n_h_arr = overlay_image(RES_R, cut_image(RES_R, h_arr, 4, 20, 58, 60), n_h_arr, 56, 38)
        n_h_arr = overlay_image(RES_R, cut_image(RES_R, h_arr, 4, 20, 62, 64), n_h_arr, 58, 38)
        n_h_arr = overlay_image(RES_R, cut_image(RES_R, h_arr, 4, 20, 65, 67), n_h_arr, 60, 38)
        n_h_arr = overlay_image(RES_R, cut_image(RES_R, h_arr, 4, 20, 67, 69), n_h_arr, 62, 38)

        n_h_arr = overlay_image(RES_R, cut_image(RES_R, h_arr, 2, 4, 62, 66), n_h_arr, 58, 36)

        # body
        n_h_arr = overlay_image(RES_R, cut_image(RES_R, h_arr, 58, 68, 0, 22), n_h_arr, 0, 54)
        n_h_arr = overlay_image(RES_R, cut_image(RES_R, h_arr, 58, 68, 13, 24), n_h_arr, 11, 54)

        n_h_arr = overlay_image(RES_R, cut_image(RES_R, h_arr, 58, 68, 24, 34), n_h_arr, 22, 54)

        n_h_arr = overlay_image(RES_R, cut_image(RES_R, h_arr, 58, 68, 34, 56), n_h_arr, 32, 54)
        n_h_arr = overlay_image(RES_R, cut_image(RES_R, h_arr, 58, 68, 47, 57), n_h_arr, 43, 54)

        n_h_arr = overlay_image(RES_R, cut_image(RES_R, h_arr, 58, 68, 58, 68), n_h_arr, 54, 54)
        n_h_arr = overlay_image(RES_R, cut_image(RES_R, h_arr, 34, 56, 24, 44), n_h_arr, 22, 32)
        n_h_arr = overlay_image(RES_R, cut_image(RES_R, h_arr, 49, 58, 24, 44), n_h_arr, 22, 45)

        # chest
        n_h_arr = overlay_image(RES_R, cut_image(RES_R, h_arr, 34, 45, 0, 11), n_h_arr, 26, 21)
        n_h_arr = overlay_image(RES_R, cut_image(RES_R, h_arr, 47, 58, 11, 22), n_h_arr, 37, 21)

        # foot
        n_h_arr = overlay_image(RES_R, cut_image(RES_R, h_arr, 35, 41, 97, 113), n_h_arr, 48, 25)
        n_h_arr = overlay_image(RES_R, cut_image(RES_R, h_arr, 49, 51, 96, 104), n_h_arr, 48, 31)
        n_h_arr = overlay_image(RES_R, cut_image(RES_R, h_arr, 49, 51, 96, 104), n_h_arr, 56, 31)
        n_h_arr = overlay_image(RES_R, cut_image(RES_R, h_arr, 55, 58, 96, 112), n_h_arr, 48, 33)
        n_h_arr = overlay_image(RES_R, cut_image(RES_R, h_arr, 29, 33, 101, 105), n_h_arr, 52, 21)
        n_h_arr = overlay_image(RES_R, cut_image(RES_R, h_arr, 51, 55, 104, 108), n_h_arr, 56, 21)

        # rein
        n_h_arr = overlay_image(RES_R, cut_image(RES_R, h_arr, 0, 4, 74, 80), n_h_arr, 29, 5)
        # n_h_arr = overlayImg(cutImg(h_arr,24,29, 81,83), n_h_arr,1,7)
        # n_h_arr = overlayImg(cutImg(h_arr,24,29, 81,83), n_h_arr,25,2)
        # n_h_arr = overlayImg(cutImg(h_arr,24,29, 86,88), n_h_arr,17,7)
        # n_h_arr = overlayImg(cutImg(h_arr,24,29, 86,88), n_h_arr,19,2)

        # tail?
        n_h_arr = overlay_image(RES_R, np.rot90(cut_image(RES_R, h_arr, 10, 14, 34, 41), -1), n_h_arr, 42, 47)
        n_h_arr = overlay_image(RES_R, np.rot90(cut_image(RES_R, h_arr, 3, 10, 31, 37), -2), n_h_arr, 46, 47)
        n_h_arr = overlay_image(RES_R, np.rot90(cut_image(RES_R, h_arr, 10, 14, 24, 31), 1), n_h_arr, 52, 47)

        n_h_arr = overlay_image(RES_R, np.rot90(cut_image(RES_R, h_arr, 14, 18, 48, 55), -1), n_h_arr, 42, 40)
        n_h_arr = overlay_image(RES_R, np.rot90(cut_image(RES_R, h_arr, 7, 14, 45, 51), -2), n_h_arr, 46, 40)
        n_h_arr = overlay_image(RES_R, np.rot90(cut_image(RES_R, h_arr, 14, 18, 38, 45), 1), n_h_arr, 52, 40)
        n_h_arr = overlay_image(RES_R, cut_image(RES_R, h_arr, 14, 18, 45, 48), n_h_arr, 46, 36)

        # sella
        n_h_arr = overlay_image(RES_R, cut_image(RES_R, h_arr, 0, 9, 88, 98), n_h_arr, 35, 0)
        n_h_arr = overlay_image(RES_R, cut_image(RES_R, h_arr, 9, 11, 89, 98), n_h_arr, 26, 9)
        n_h_arr = overlay_image(RES_R, cut_image(RES_R, h_arr, 9, 11, 89, 98), n_h_arr, 45, 9)

        n_h_img = Image.fromarray(n_h_arr)
        n_h_img.save(path, 'PNG')
    except Exception as e:
        logger.error(f"Failed to convert {file} because {e}")

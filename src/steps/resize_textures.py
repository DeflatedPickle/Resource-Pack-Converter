import numpy as np
from PIL import Image, UnidentifiedImageError
from loguru import logger

from src.onefile import *
from src.settings import colour_space
from src.steps.reposition_textures import reposition_horse_texture
from src.util.image_util import overlay_image, cut_image


def resize_textures(
        RES_R,
        texture_path,
):
    logger.info("Resizing textures...")

    resize_particles(RES_R, texture_path)
    resize_map_icons(RES_R, texture_path)
    resize_horse(RES_R, texture_path)


def resize_particles(
        RES_R,
        texture_path
):
    file = "particles.png"
    path = f'{texture_path}/particle/{file}'

    logger.info(f"Resizing {file}...")

    if os.path.exists(path):
        try:
            p_img = Image.open(path).convert(colour_space)
            p_img = p_img.resize((128 * RES_R, 128 * RES_R), Image.NEAREST)
            p_arr = np.array(p_img)

            p_o_img = Image.open(resource_path(file)).convert(colour_space)
            p_o_img = p_o_img.resize((256 * RES_R, 256 * RES_R), Image.NEAREST)
            p_o_arr = np.array(p_o_img)

            n_p_arr = np.zeros((256 * RES_R, 256 * RES_R, 4), dtype=np.uint8)
            n_p_arr = overlay_image(RES_R, p_arr, n_p_arr)
            n_p_arr = overlay_image(RES_R, cut_image(RES_R, p_o_arr, 104, 112, 0, 8), n_p_arr, 0, 104)
            n_p_arr = overlay_image(RES_R, cut_image(RES_R, p_o_arr, 128, 152, 0, 88), n_p_arr, 0, 128)

            n_p_img = Image.fromarray(n_p_arr)
            n_p_img.save(path, 'PNG')
        except (FileNotFoundError, ValueError, TypeError, UnidentifiedImageError) as e:
            logger.error(f"Failed to convert {file} because {e}")


def resize_map_icons(
        RES_R,
        texture_path
):
    file = "map_icons.png"
    path = f'{texture_path}/map/{file}'

    logger.info(f"Resizing {file}...")

    if os.path.exists(path):
        try:
            m_img = Image.open(path).convert(colour_space)
            m_img = m_img.resize((32 * RES_R, 32 * RES_R), Image.NEAREST)
            m_arr = np.array(m_img)

            m_o_img = Image.open(resource_path(file)).convert(colour_space)
            m_o_img = m_o_img.resize((128 * RES_R, 128 * RES_R), Image.NEAREST)
            m_o_arr = np.array(m_o_img)

            n_m_arr = np.zeros((128 * RES_R, 128 * RES_R, 4), dtype=np.uint8)
            n_m_arr = overlay_image(RES_R, cut_image(RES_R, m_arr, 0, 8, 0, 32), n_m_arr, 0, 0)
            n_m_arr = overlay_image(RES_R, cut_image(RES_R, m_arr, 0, 16, 8, 32), n_m_arr, 32, 0)
            n_m_arr = overlay_image(RES_R, cut_image(RES_R, m_arr, 16, 24, 0, 16), n_m_arr, 64, 0)
            n_m_arr = overlay_image(RES_R, cut_image(RES_R, m_o_arr, 0, 8, 80, 128), n_m_arr, 80, 0)
            n_m_arr = overlay_image(RES_R, cut_image(RES_R, m_o_arr, 8, 16, 0, 128), n_m_arr, 0, 8)

            n_m_img = Image.fromarray(n_m_arr)
            n_m_img.save(path, 'PNG')
        except (FileNotFoundError, ValueError, TypeError, UnidentifiedImageError) as e:
            logger.error(f"Failed to convert {file} because {e}")


def resize_horse(
        RES_R,
        texture_path
):
    path = f'{texture_path}/entity/horse/'

    if os.path.exists(path):
        for file in os.listdir(path):
            if file.endswith('.png'):
                reposition_horse_texture(RES_R, path, file)

        path = f'{texture_path}/entity/horse/'

        if os.path.exists(path):
            for file in os.listdir(path):
                if file.endswith('.png'):
                    reposition_horse_texture(RES_R, path, file)

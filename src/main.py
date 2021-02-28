import json
import pathlib
import tempfile
import zipfile

import math
from loguru import logger

import settings
import steps
from onefile import *
from src.steps import pack_data, boxcraft, rename, zipping, tweak_models, tweak_states
from src.steps.resize_textures import resize_textures
from src.util.alter_util import alter_all_states
from src.util.image_util import detect_resolution
from src.util.json_util import modify_json

if settings.target_format == 4:
    from changes.v4 import *
elif settings.target_format == 5:
    from changes.v5 import *
else:
    raise NotImplementedError()


@logger.catch
def main(pack,
         destination,
         resolution,
         new_name,
         name_suffix,
         description,
         shaders,
         tex):
    is113 = False

    tmp_dir = tempfile.mkdtemp()

    # Packs can also be folders
    if zipfile.is_zipfile(pack):
        zipping.unzip_pack(pack, tmp_dir)

    # if not path.exists(f"{tmp_dir}/pack.mcmeta"):
    #     list_subfolders_with_paths = [
    #         f.path for f in os.scandir(pack) if f.is_dir()]
    #     PACK = list_subfolders_with_paths[0]

    MAIN_PATH = f'{tmp_dir}/assets/minecraft'
    TEX_PATH = f'{MAIN_PATH}/textures'
    block_path = f'{TEX_PATH}/blocks'
    item_path = f'{TEX_PATH}/items'
    entity_path = f'{TEX_PATH}/entity'
    model_path = f"{MAIN_PATH}/models"
    state_path = f"{MAIN_PATH}/blockstates"

    with open(f'{tmp_dir}/pack.mcmeta', "r", encoding="utf-8") as f:
        pack_mcmeta = json.load(f)
        if pack_mcmeta["pack"]["pack_format"] >= 4:
            is113 = True

    if is113:
        logger.success("This pack is already of 1.13 format")
        return -1

    if not resolution:
        res_r = detect_resolution(
            block_path,
            item_path
        )
        if not res_r:
            logger.warning("Failed to detect the pack's resolution")
            return 0
    else:
        res_r = resolution

    conversion(
        tmp_dir,
        destination,
        MAIN_PATH,
        TEX_PATH,
        block_path,
        item_path,
        entity_path,
        model_path,
        state_path,
        res_r,
        pathlib.Path(pack).stem,
        new_name,
        name_suffix,
        description,
        shaders,
        tex
    )
    logger.success("Finished converting the pack")
    del tmp_dir


def conversion(pack_path,
               destination,
               main_path,
               texture_path,
               block_path,
               item_path,
               entity_path,
               model_path,
               state_path,
               res_r,
               old_name,
               new_name,
               name_suffix,
               description,
               shaders,
               tex):
    if res_r == 0:
        res_r = 1
    RES_R = int(math.pow(2, res_r))

    steps.make_missing_directories(main_path)
    rename.change_file_names(
        block_path,
        item_path,
        entity_path,
        model_path,
        state_path,
        shaders
    )
    rename.change_folder_name(
        {
            entity_path: entity_directory_list,
            texture_path: texture_directory_list
        }
    )
    tweak_models.change_models(
        model_path
    )
    tweak_states.change_states(
        state_path
    )
    resize_textures(
        RES_R,
        texture_path
    )
    pack_data.change_info(
        pack_path,
        pack_format,
        description
    )
    if tex:
        boxcraft.blockstate_fix_normal_variants(
            texture_path,
            model_path,
            state_path
        )
    zipping.zip_pack(
        pack_path,
        destination,
        old_name,
        new_name,
        name_suffix
    )

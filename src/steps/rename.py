import os

from loguru import logger

from src.changes.common import blockList, itemList, entityList, modelList, stateList, blockListNormal, blockListSpecular


def change_file_names(
        block_path,
        item_path,
        entity_path,
        model_path,
        state_path,
        shaders
):
    logger.info("Changing file names...")

    change_texture_names([
        [block_path, blockList],
        [item_path, itemList],
        [entity_path, entityList]
    ])
    if shaders:
        change_texture_names([
            [block_path, blockListNormal],
            [block_path, blockListSpecular]
        ])
    change_model_names(model_path)
    change_state_names(state_path)


def change_texture_names(asset_matrix):
    logger.info("Changing texture names...")

    ext_list = ["png", "png.mcmeta"]

    for ext in ext_list:
        for pair in asset_matrix:
            texture_path = pair[0]
            texture_list = pair[1]

            for name in texture_list:
                old = name[0]
                new = name[1]

                try:
                    os.rename(f"{texture_path}/{old}.{ext}",
                              f"{texture_path}/{new}.{ext}")
                    logger.debug(f"{old} was renamed to {new}")
                except IOError as e:
                    # Not all textures should have meta files, ignore errors from ones that don't
                    if ext != ext_list[1]:
                        logger.error(f"Failed to read {old}.{ext} because {e}")


def change_model_names(model_path):
    logger.info("Changing model names...")

    asset_type_to_model_list = {"block": modelList,
                                "item": stateList}

    for model_type, asset_list in asset_type_to_model_list.items():
        for name in asset_list:
            old = name[0]
            new = name[1]

            try:
                os.rename(f'{model_path}/{model_type}/{old}.json',
                          f'{model_path}/{model_type}/{new}.json')
                logger.debug(f"{old} was renamed to {new}")
            except IOError as e:
                logger.error(f"Failed to read {new}.json because {e}")


def change_state_names(state_path):
    logger.info("Changing blockstate names...")

    for name in stateList:
        old = name[0]
        new = name[1]

        try:
            os.rename(f'{state_path}/{old}.json',
                      f'{state_path}/{new}.json')
            logger.debug(f"{old} was renamed to {new}")
        except IOError as e:
            logger.error(f"Failed to read {old}.json because {e}")


def change_folder_name(lead_to_directories):
    logger.info("Changing folder names...")

    for lead, changes in lead_to_directories.items():
        for name in changes:
            old = name[0]
            new = name[1]

            try:
                os.rename(f"{lead}/{old}", f"{lead}/{new}")
                logger.debug(f"{old} was renamed to {new}")
            except IOError as e:
                logger.error(f"Failed to rename {old} to {new} because {e}")

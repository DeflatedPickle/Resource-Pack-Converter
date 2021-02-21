import json

from loguru import logger

from src.util.json_util import modify_json


def change_info(pack_path,
                pack_format,
                description):
    """
    Replace the pack format

    :param pack_path:
    :param pack_format:
    :param description:
    :return:
    """
    logger.info("Changing pack format")

    # Read the current data in
    # Then replace the format and description
    with open(f'{pack_path}/pack.mcmeta', 'r') as f:
        pack_info = json.loads("\n".join(modify_json(f)))

        pack_info['pack']['pack_format'] = pack_format

        if description != "":
            pack_info['pack']['description'] = description

    # Write the new data
    with open(f'{pack_path}/pack.mcmeta', 'w') as f:
        json.dump(pack_info, f, ensure_ascii=False, indent=4)

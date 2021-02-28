from pathlib import Path

from loguru import logger


def alter(f,
          old_str,
          new_str):
    file_data = ""

    for line in f:
        line = line.replace(old_str, new_str)
        file_data += line

    return file_data


def alter_all_models(f,
                     block_list,
                     item_list,
                     model_list):
    logger.info(f"Altering the {Path(f.name).name} block/item models...")

    file_data = ""

    # TODO: Replace these using the json library
    for line in f:
        line = line.replace("\"blocks/", "\"block/")
        line = line.replace("\"items/", "\"item/")

        for path, list_ in {
            "block": block_list,
            "item": item_list,
            "\"parent\": \"block": model_list
        }.items():
            for name in list_:
                line = line.replace(
                    f"\"{path}/{name[0]}\"",
                    f"\"{path}/{name[1]}\""
                )

        file_data += line

    return file_data


def alter_all_states(f,
                     model_list):
    logger.info(f"Replacing all old block states in {Path(f.name).name}...")

    file_data = ""

    # TODO: Replace these using the json library
    for line in f:
        line = line.replace("\"model\": \"", "\"model\": \"block/")

        for name in model_list:
            line = line.replace(
                f"\"model\": \"block/{name[0]}\"",
                f"\"model\": \"block/{name[1]}\""
            )

        file_data += line

    return file_data

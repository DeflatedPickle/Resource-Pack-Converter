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
    file_data = ""

    # TODO: Replace these using the json library
    for line in f:
        line = line.replace("\"blocks/", "\"block/")
        line = line.replace("\"items/", "\"item/")

        for name in block_list:
            line = line.replace(
                f"\"block/{name[0]}\"",
                f"\"block/{name[1]}\""
            )

        for name in item_list:
            line = line.replace(
                f"\"item/{name[0]}\"",
                f'\"item/{name[1]}\"'
            )

        for name in model_list:
            line = line.replace(
                f"\"parent\": \"block/{name[0]}\"",
                f"\"parent\": \"block/{name[1]}\""
            )

        file_data += line

    return file_data


def alter_all_states(f,
                     model_list):
    file_data = ""

    # TODO: Replace these using the json library
    for line in f:
        line = line.replace("\"model\": \"", "\"model\": \"block/")

        for name in model_list:
            logger.info(f"Replacing {name[0]} with {name[1]} for {f}")
            line = line.replace(
                f"\"model\": \"block/{name[0]}\"",
                f"\"model\": \"block/{name[1]}\""
            )

        file_data += line

    return file_data

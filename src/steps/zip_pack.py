import zipfile
import os
from loguru import logger


def unzip_pack(
        old,
        new
):
    """
    Unzips a pack

    :param old:
    :param new:
    :return:
    """
    logger.info("Unzipping pack...")

    azip = zipfile.ZipFile(old)

    try:
        azip.extractall(new)
    except OSError as e:
        logger.error(e)


def zipup_pack(pack,
               destination,
               old_name,
               new_name,
               name_suffix):
    """
    Zips a pack up, optionally adding a suffix to the name

    :param pack:
    :param destination:
    :param old_name:
    :param new_name:
    :param name_suffix:
    :return:
    """
    logger.info("Zipping up pack...")

    if new_name is None:
        pack_name = old_name
    else:
        pack_name = new_name

    if name_suffix != "":
        name_suffix = f"-{name_suffix}"

    azip = zipfile.ZipFile(f"{destination}/{pack_name}{name_suffix}.zip", 'w')

    for root, dirs, files in os.walk(pack):
        for name in files:
            azip.write(os.path.join(root, name), os.path.join(root, name)[len(pack) + 1:])
            print(os.path.join(root, name)[len(pack) + 1:])

    azip.close()

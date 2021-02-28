import json
import os

from loguru import logger

from src.util.json_util import modify_json


# noinspection SpellCheckingInspection
def blockstate_fix_normal_variants(texture_path,
                                   model_path,
                                   state_path):
    """
    In 1.8, blockstates have a "normal" variant. This was changed to "" in newer packs

    :param texture_path:
    :param model_path:
    :param state_path:
    :return:
    """
    logger.info("Replacing blockstate normal variants")

    natural_texture_blocks = [
        "bedrock",
        "dirt",
        "grass_path",
        "netherrack",
        "red_sand",
        "sand",
        "stone"
    ]

    for n in natural_texture_blocks:
        path = f'{state_path}/{n}.json'

        try:
            with open(path, 'r') as f:
                nblockdict = json.loads("\n".join(modify_json(f)))

            variants = nblockdict["variants"]
            newvar = variants["normal"]
            del variants["normal"]
            variants[""] = newvar

            with open(path, 'w') as dump_f:
                json.dump({'variants': variants}, dump_f)
            logger.debug(f"Converted {n}.json")
        except (IOError, KeyError) as e:
            logger.error(f"Failed because of {e}")

    os.remove(f"{state_path}/furnace.json")
    os.remove(f"{model_path}/block/item_frame.json")

    # TODO: Convert to a dictionary
    animated_blocks = [
        ["furnace_front_on", 10],
        ["sea_lantern", 5]
    ]

    for block in animated_blocks:
        try:
            with open(f"{texture_path}/block/{block[0]}.png.mcmeta", 'w+') as dump_f:
                json.dump(
                    {
                        "animation": {
                            "interpolate": True,
                            "frametime": block[1]
                        }
                    },
                    dump_f
                )
            logger.debug(f"Converted {block[0]}.png.mcmeta")
        except (IOError, KeyError) as e:
            logger.error(f"Failed because of {e}")

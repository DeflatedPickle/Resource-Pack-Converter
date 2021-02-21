import json
import os

from loguru import logger

from src.util.json_util import modify_json


# noinspection SpellCheckingInspection
def blockstate_fix_normal_variants(main_path,
                                   texture_path):
    """
    In 1.8, blockstates have a "normal" variant. This was changed to "" in newer packs

    :param main_path:
    :param texture_path:
    :return:
    """
    logger.info("Replacing blockstate normal variants")

    natural_texture_blocks = [
        "bedrock.json",
        "dirt.json",
        "grass_path.json",
        "netherrack.json",
        "red_sand.json",
        "sand.json",
        "stone.json"
    ]

    for n in natural_texture_blocks:
        path = f'{main_path}/blockstates/{n}'

        try:
            with open(path, 'r') as f:
                nblockdict = json.loads("\n".join(modify_json(f)))

            variants = nblockdict["variants"]
            newvar = variants["normal"]
            del variants["normal"]
            variants[""] = newvar

            with open(path, 'w') as dump_f:
                json.dump({'variants': variants}, dump_f)
            print("Converted blockstates/" + n)
        except IOError:
            print("Error: fail to splite anvil state")
        except KeyError:
            print("Error: Block has no variant of 'normal'")

    os.remove(f"{main_path}/blockstates/furnace.json")
    os.remove(f"{main_path}/models/block/item_frame.json")

    # TODO: Convert to a dictionary
    animated_blocks = [
        ["furnace_front_on", 10],
        ["sea_lantern", 5]
    ]

    for block in animated_blocks:
        try:
            animation = {"interpolate": True, "frametime": block[1]}
            with open(f"{texture_path}/block/{block[0]}.png.mcmeta", 'w+') as dump_f:
                json.dump({"animation": animation}, dump_f)
            print("Converted " + block[0] + ".png.mcmeta")
        except IOError:
            print("Error: fail to splite anvil state")
        except KeyError:
            print("Error: Key error in block " + block)

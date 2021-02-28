import json
import os

from loguru import logger

from src.changes.common import blockList, itemList, modelList
from src.util.alter_util import alter_all_models
from src.util.json_util import modify_json


def change_models(
        model_path
):
    logger.info("Converting models...")

    convert_block_item_models(model_path)
    merge_grass_block_models(model_path)
    replace_anvil_textures(model_path)


def convert_block_item_models(model_path):
    logger.info("Converting block and item models...")

    asset_list = ["block", "item"]

    for asset in asset_list:
        asset_directory = f'{model_path}/{asset}/'
        
        if os.path.exists(asset_directory):
            for model in os.listdir(asset_directory):
                if model.endswith('.json'):
                    logger.debug(f"Converting the model for {model}...")

                    # change all textures & models' name in model file
                    with open(f'{model_path}/{asset}/{model}', "r", encoding="utf-8") as f:
                        file_data = alter_all_models(f, blockList, itemList, modelList)

                    with open(f'{model_path}/{asset}/{model}', "w", encoding="utf-8") as f:
                        f.write(file_data)


def merge_grass_block_models(model_path):
    logger.info(f"Merging the grass_block and grass_normal models...")

    grass_block = f'{model_path}/block/grass_block.json'
    grass_normal = f'{model_path}/block/grass_normal.json'
    
    if os.path.exists(grass_block):
        with open(grass_block, 'r') as f:
            grass_block_json = json.loads("\n".join(f))

        # TODO: Move this to a specific files in a resource path
        if 'elements' not in grass_block_json:
            grass_block_json['elements'] = [
                {"from": [0, 0, 0],
                 "to": [16, 16, 16],
                 "faces": {
                     "down": {"uv": [0, 0, 16, 16], "texture": "#bottom", "cullface": "down"},
                     "up": {"uv": [0, 0, 16, 16], "texture": "#top", "cullface": "up", "tintindex": 0},
                     "north": {"uv": [0, 0, 16, 16], "texture": "#side", "cullface": "north"},
                     "south": {"uv": [0, 0, 16, 16], "texture": "#side", "cullface": "south"},
                     "west": {"uv": [0, 0, 16, 16], "texture": "#side", "cullface": "west"},
                     "east": {"uv": [0, 0, 16, 16], "texture": "#side", "cullface": "east"}
                 }
                 },
                {"from": [0, 0, 0],
                 "to": [16, 16, 16],
                 "faces": {
                     "north": {"uv": [0, 0, 16, 16], "texture": "#overlay", "tintindex": 0, "cullface": "north"},
                     "south": {"uv": [0, 0, 16, 16], "texture": "#overlay", "tintindex": 0, "cullface": "south"},
                     "west": {"uv": [0, 0, 16, 16], "texture": "#overlay", "tintindex": 0, "cullface": "west"},
                     "east": {"uv": [0, 0, 16, 16], "texture": "#overlay", "tintindex": 0, "cullface": "east"}
                 }
                 }
            ]

        if os.path.exists(grass_normal):
            with open(grass_normal, 'r') as f:
                grass_normal_json = json.loads("\n".join(modify_json(f)))

            if "textures" in grass_block_json:
                grass_block_tex = grass_normal_json["textures"]
            else:
                grass_block_tex = grass_block_json["textures"]
        else:
            grass_block_tex = grass_block_json["textures"]

        # Replace textures
        if "particle" not in grass_block_tex:
            grass_block_tex["particle"] = "block/dirt"
        if "bottom" not in grass_block_tex:
            grass_block_tex["bottom"] = "block/dirt"
        if "top" not in grass_block_tex:
            grass_block_tex["top"] = "block/grass_block_top"
        if "side" not in grass_block_tex:
            grass_block_tex["side"] = "block/grass_block_side"
        if "overlay" not in grass_block_tex:
            grass_block_tex["overlay"] = "block/grass_block_side_overlay"

        grass_block_json["textures"] = grass_block_tex
        grass_block_json["parent"] = "block/block"

        with open(grass_block, 'w') as dump_f:
            json.dump(grass_block_json, dump_f)


def replace_anvil_textures(model_path):
    logger.info(f"Replacing the anvil textures...")

    anvil = f'{model_path}/block/anvil.json'
    anvil_undamaged = f'{model_path}/block/anvil_undamaged.json'

    if os.path.exists(anvil):
        with open(anvil, 'r') as f:
            anvil_json = json.loads("\n".join(modify_json(f)))

    if os.path.exists(anvil_undamaged):
        with open(anvil_undamaged, 'r') as f:
            anvil_tex = json.loads("\n".join(modify_json(f)))['textures']
    else:
        anvil_tex = {
            "particle": "block/anvil",
            "body": "block/anvil",
            "top": "block/anvil_top"
        }

    anvil_json['textures'] = anvil_tex
    with open(anvil, 'w') as dump_f:
        json.dump(anvil_json, dump_f)

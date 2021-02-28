import json
import os

from loguru import logger

from src.changes.common import modelList, torch_list
from src.util.alter_util import alter_all_states
from src.util.json_util import modify_json


def change_states(state_path):
    altar_states(state_path)

    for torch in torch_list:
        split_torch_states(state_path, torch)

    split_anvil_state(state_path)
    replace_lever_variants(state_path)


def altar_states(state_path):
    if os.path.exists(state_path):
        for state in os.listdir(state_path):
            if state.endswith(".json"):
                with open(f'{state_path}/{state}', "r", encoding="utf-8") as f:
                    fileData = alter_all_states(f, modelList)

                with open(f'{state_path}/{state}', "w", encoding="utf-8") as f:
                    f.write(fileData)


def split_anvil_state(state_path):
    logger.info("Splitting the anvil states...")

    try:
        with open(f'{state_path}/anvil.json', 'r') as f:
            anvil_dict = json.loads("\n".join(modify_json(f)))

        if 'damage=0,facing=south' in anvil_dict['variants']:
            anvil_json = {
                'variants': {
                    "facing=south": anvil_dict['variants']["damage=0,facing=south"],
                    "facing=west": anvil_dict['variants']["damage=0,facing=west"],
                    "facing=north": anvil_dict['variants']["damage=0,facing=north"],
                    "facing=east": anvil_dict['variants']["damage=0,facing=east"]
                }
            }

            with open(f'{state_path}/anvil.json', 'w') as dump_f:
                json.dump(anvil_json, dump_f)

        if 'damage=1,facing=south' in anvil_dict['variants']:
            chipped_anvil_json = {
                'variants': {
                    "facing=south": anvil_dict['variants']["damage=1,facing=south"],
                    "facing=west": anvil_dict['variants']["damage=1,facing=west"],
                    "facing=north": anvil_dict['variants']["damage=1,facing=north"],
                    "facing=east": anvil_dict['variants']["damage=1,facing=east"]
                }
            }

            with open(f'{state_path}/chipped_anvil.json', 'w') as dump_f:
                json.dump(chipped_anvil_json, dump_f)

        if 'damage=2,facing=south' in anvil_dict['variants']:
            damaged_anvil_json = {
                'variants': {
                    "facing=south": anvil_dict['variants']["damage=2,facing=south"],
                    "facing=west": anvil_dict['variants']["damage=2,facing=west"],
                    "facing=north": anvil_dict['variants']["damage=2,facing=north"],
                    "facing=east": anvil_dict['variants']["damage=2,facing=east"]
                }
            }

            with open(f'{state_path}/damaged_anvil.json', 'w') as dump_f:
                json.dump(damaged_anvil_json, dump_f)

    except IOError as e:
        logger.error(f"Failed to split anvil state because {e}")


def replace_lever_variants(state_path):
    logger.info("Replacing lever variants...")

    try:
        with open(f'{state_path}/lever.json', 'r') as f:
            lever_dict = json.loads("\n".join(modify_json(f)))

        variants = {}
        variants = change_lever_variants(variants, lever_dict, 'false')
        variants = change_lever_variants(variants, lever_dict, 'true')

        with open(f'{state_path}/lever.json', 'w') as dump_f:
            json.dump({'variants': variants}, dump_f)

    except IOError as e:
        logger.error(f"Failed to replace lever variants because {e}")


def split_torch_states(state_path, prefix):
    logger.info(f"Splitting {prefix}torch states...")

    try:
        with open(f'{state_path}/{prefix}torch.json', 'r', encoding="utf-8") as f:
            torch_dict = json.loads("\n".join(modify_json(f)))

        if 'facing=up' in torch_dict['variants']:
            torch_json = {
                'variants': {
                    "": torch_dict['variants']["facing=up"]
                }
            }
            # print(torch_json)
            with open(f'{state_path}/{prefix}torch.json', 'w') as dump_f:
                json.dump(torch_json, dump_f)

        if 'facing=east' in torch_dict['variants']:
            if 'facing=up' in torch_dict['variants']:
                del torch_dict['variants']["facing=up"]
            wall_torch_json = torch_dict
            # print(wall_torch_json)

            with open(f'{state_path}/{prefix}wall_torch.json', 'w') as dump_f:
                json.dump(wall_torch_json, dump_f)
    except IOError as e:
        logger.error(f"Failed to split {prefix}torch states because {e}")


def change_lever_variants(variants, lever_dict, toggled):
    logger.info(f"Changing {'powered' if toggled else ''} lever variants...")

    if 'facing=east,powered=' + toggled in lever_dict['variants']:
        model = lever_dict['variants']["facing=east,powered=" + toggled]["model"]
        variants = {
            **variants,
            "face=wall,facing=north,powered=" + toggled: {"model": model, "x": 90},
            "face=wall,facing=east,powered=" + toggled: {"model": model, "x": 90, "y": 90},
            "face=wall,facing=south,powered=" + toggled: {"model": model, "x": 90, "y": 180},
            "face=wall,facing=west,powered=" + toggled: {"model": model, "x": 90, "y": 270},
        }

    if 'facing=down_z,powered=' + toggled in lever_dict['variants']:
        model = lever_dict['variants']["facing=down_z,powered=" + toggled]["model"]
        variants = {
            **variants,
            "face=ceiling,facing=north,powered=" + toggled: {"model": model, "x": 180, "y": 180},
            "face=ceiling,facing=east,powered=" + toggled: {"model": model, "x": 180, "y": 270},
            "face=ceiling,facing=south,powered=" + toggled: {"model": model, "x": 180},
            "face=ceiling,facing=west,powered=" + toggled: {"model": model, "x": 180, "y": 90},
        }

    if 'facing=up_z,powered=' + toggled in lever_dict['variants']:
        model = lever_dict['variants']["facing=up_z,powered=" + toggled]["model"]
        variants = {
            **variants,
            "face=floor,facing=north,powered=" + toggled: {"model": model},
            "face=floor,facing=east,powered=" + toggled: {"model": model, "y": 90},
            "face=floor,facing=south,powered=" + toggled: {"model": model, "y": 180},
            "face=floor,facing=west,powered=" + toggled: {"model": model, "y": 270},
        }

    return variants

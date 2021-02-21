import json
import pathlib
import tempfile
import zipfile

import math
from loguru import logger

import settings
import steps
from onefile import *
from src.steps import pack_data, boxcraft
from src.util.alter_util import alter_all_models, alter_all_states
from src.steps.resize_textures import resize_textures
from src.steps.zip_pack import zipup_pack, unzip_pack
from src.util.image_util import detect_resolution
from src.util.json_util import modify_json

if settings.target_format == 4:
    from changes.v4 import *
elif settings.target_format == 5:
    from changes.v5 import *
else:
    raise NotImplementedError()

'''
                            static textures' name
---------------------------------------------------------------------------
'''
def changeFileName(
        main_path,
        block_path,
        item_path,
        entity_path
):
    print ("changing texs'name...")

    ext_list = ["png", "png.mcmeta"]
    path_to_asset_matrix = {block_path: blockList,
                            item_path: itemList,
                            entity_path: entityList}

    for ext in ext_list:
        for tex_path, asset_list in path_to_asset_matrix.items():
            for name in asset_list:
                try:
                    #change file name
                    os.rename(f"{tex_path}/{name[0]}.{ext}",
                              f"{tex_path}/{name[1]}.{ext}")
                    print (name[0] + " changed to " + name[1])
                except IOError:
                    print (f"Error: fail to read {name[0]}.{ext}")

    '''
                                models' name
    ---------------------------------------------------------------------------
    '''
    asset_type_to_model_list = {"block": modelList,
                                "item": stateList}
    for model_type, asset_list in asset_type_to_model_list.items():
        for name in asset_list:
            try:
                os.rename(
                    f'{main_path}/models/{model_type}/{name[0]}.json',
                    f'{main_path}/models/{model_type}/{name[1]}.json'
                    )
            except IOError:
                print ("Error: fail to read" + name[0] + '.json')
    '''
                                bloackstates' name
    ---------------------------------------------------------------------------
    '''
    for name in stateList:
        try:
            os.rename(
                f'{main_path}/blockstates/{name[0]}.json',
                f'{main_path}/blockstates/{name[1]}.json',
                )
        except IOError:
            print ("Error: fail to read " + name[0] + '.json')

'''
---------------------------------------------------------------------------
                            change folders'name
---------------------------------------------------------------------------
'''
def changeFolderName(
        entity_path,
        texture_path
):
    print ("changing folders'name...")
    try:
        os.rename(entity_path + 'endercrystal', entity_path + 'end_crystal')
        #os.rename(entity_path + 'horse', entity_path + '.horse')

        os.rename(f'{texture_path}/blocks', f'{texture_path}/block')
        os.rename(f'{texture_path}/items', f'{texture_path}/item')
        #os.rename(TEX_PATH + 'particle', TEX_PATH + '.particle')

    except IOError as e:
        logger.error(e)

'''
---------------------------------------------------------------------------
                     change state/model files'content
---------------------------------------------------------------------------
'''
def changeModel(
        main_path
):
    print ("converting models...")
    '''
                                models' content
    ---------------------------------------------------------------------------
    '''
    asset_list = ["block", "item"]

    for asset in asset_list:
        if os.path.exists(f'{main_path}/models/{asset}/'):
            model_list = (file for file in os.listdir(f'{main_path}/models/{asset}/')
                     if file.endswith('.json'))
            logger.info("Altering all the block/item models...")
            for model in model_list:
                #change all textures & models' name in model file
                with open(f'{main_path}/models/{asset}/{model}', "r", encoding="utf-8") as f:
                    fileData = alter_all_models(f, blockList, itemList, modelList)

                with open(f'{main_path}/models/{asset}/{model}', "w", encoding="utf-8") as f:
                    f.write(fileData)

                print(model + ' is OK')

    #merge grasss_block and grass_normal
    if os.path.exists(f'{main_path}/models/block/grass_block.json'):
        with open(f'{main_path}/models/block/grass_block.json', 'r') as f:
            grass_block_json = json.loads("\n".join(f))

        if 'elements' not in grass_block_json:
            grass_block_json['elements'] = [
                {   "from": [ 0, 0, 0 ],
                    "to": [ 16, 16, 16 ],
                    "faces": {
                        "down":  { "uv": [ 0, 0, 16, 16 ], "texture": "#bottom", "cullface": "down" },
                        "up":    { "uv": [ 0, 0, 16, 16 ], "texture": "#top",    "cullface": "up", "tintindex": 0 },
                        "north": { "uv": [ 0, 0, 16, 16 ], "texture": "#side",   "cullface": "north" },
                        "south": { "uv": [ 0, 0, 16, 16 ], "texture": "#side",   "cullface": "south" },
                        "west":  { "uv": [ 0, 0, 16, 16 ], "texture": "#side",   "cullface": "west" },
                        "east":  { "uv": [ 0, 0, 16, 16 ], "texture": "#side",   "cullface": "east" }
                    }
                },
                {   "from": [ 0, 0, 0 ],
                    "to": [ 16, 16, 16 ],
                    "faces": {
                        "north": { "uv": [ 0, 0, 16, 16 ], "texture": "#overlay", "tintindex": 0, "cullface": "north" },
                        "south": { "uv": [ 0, 0, 16, 16 ], "texture": "#overlay", "tintindex": 0, "cullface": "south" },
                        "west":  { "uv": [ 0, 0, 16, 16 ], "texture": "#overlay", "tintindex": 0, "cullface": "west" },
                        "east":  { "uv": [ 0, 0, 16, 16 ], "texture": "#overlay", "tintindex": 0, "cullface": "east" }
                    }
                }
            ]

        if os.path.exists(f'{main_path}/models/block/grass_normal.json'):
            with open(f'{main_path}/models/block/grass_normal.json','r') as f:
                grass_normal_json = json.loads("\n".join(modify_json(f)))
            if "textures" in grass_block_json:
                grass_block_tex = grass_normal_json["textures"]
            else:
                grass_block_tex = grass_block_json["textures"]
        else:
            grass_block_tex = grass_block_json["textures"]

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

        with open(f'{main_path}/models/block/grass_block.json','w') as dump_f:
            json.dump(grass_block_json,dump_f)

    if os.path.exists(f'{main_path}/models/block/anvil.json'):
        with open(f'{main_path}/models/block/anvil.json','r') as f:
            anvil_json = json.loads("\n".join(modify_json(f)))

        if os.path.exists(f'{main_path}/models/block/anvil_undamaged.json'):
            with open(f'{main_path}/models/block/anvil_undamaged.json','r') as f:
                anvil_tex = json.loads("\n".join(modify_json(f)))['textures']
        else:
            anvil_tex = {
                "particle": "block/anvil",
                "body": "block/anvil",
                "top": "block/anvil_top"
            }

        anvil_json['textures'] = anvil_tex
        with open(f'{main_path}/models/block/anvil.json','w') as dump_f:
            json.dump(anvil_json,dump_f)

    '''
                               blockstates' content
    ---------------------------------------------------------------------------
    '''
    if os.path.exists(f'{main_path}/blockstates/'):
        blockstateList = (file for file in os.listdir(f'{main_path}/blockstates/')
                 if file.endswith('.json'))
        logger.info("Altering all the block states...")
        for state in blockstateList:
            #change all models' name in blockstate file
            with open(f'{main_path}/blockstates/{state}', "r", encoding="utf-8") as f:
                fileData = alter_all_states(f, modelList)

            with open(f'{main_path}/blockstates/{state}', "w", encoding="utf-8") as f:
                f.write(fileData)

            print(state + ' is OK')

    changeTorchState(main_path, '')
    changeTorchState(main_path, 'redstone_')
    changeTorchState(main_path, 'unlit_redstone_')

    #splite anvi bloackstates
    try:
        with open(f'{main_path}/blockstates/anvil.json','r') as f:
            anvil_dict = json.loads("\n".join(modify_json(f)))
        if 'damage=0,facing=south' in anvil_dict['variants']:
            anvil_json = {
                'variants' : {
                    "facing=south": anvil_dict['variants']["damage=0,facing=south"],
                    "facing=west": anvil_dict['variants']["damage=0,facing=west"],
                    "facing=north": anvil_dict['variants']["damage=0,facing=north"],
                    "facing=east": anvil_dict['variants']["damage=0,facing=east"]
                    }
            }

            with open(f'{main_path}/blockstates/anvil.json','w') as dump_f:
                json.dump(anvil_json,dump_f)

        if 'damage=1,facing=south' in anvil_dict['variants']:
            chipped_anvil_json = {
                'variants' : {
                    "facing=south": anvil_dict['variants']["damage=1,facing=south"],
                    "facing=west": anvil_dict['variants']["damage=1,facing=west"],
                    "facing=north": anvil_dict['variants']["damage=1,facing=north"],
                    "facing=east": anvil_dict['variants']["damage=1,facing=east"]
                    }
            }

            with open(f'{main_path}/blockstates/chipped_anvil.json','w') as dump_f:
                json.dump(chipped_anvil_json,dump_f)

        if 'damage=2,facing=south' in anvil_dict['variants']:
            damaged_anvil_json = {
                'variants' : {
                    "facing=south": anvil_dict['variants']["damage=2,facing=south"],
                    "facing=west": anvil_dict['variants']["damage=2,facing=west"],
                    "facing=north": anvil_dict['variants']["damage=2,facing=north"],
                    "facing=east": anvil_dict['variants']["damage=2,facing=east"]
                    }
            }

            with open(f'{main_path}/blockstates/damaged_anvil.json','w') as dump_f:
                json.dump(damaged_anvil_json,dump_f)

    except IOError:
        print ("Error: fail to splite anvil state")

    try:
        with open(f'{main_path}/blockstates/lever.json','r') as f:
            lever_dict = json.loads("\n".join(modify_json(f)))

        variants = {}
        variants = changeLeverState(variants, lever_dict, 'false')
        variants = changeLeverState(variants, lever_dict, 'true')

        with open(f'{main_path}/blockstates/lever.json','w') as dump_f:
            json.dump({'variants':variants},dump_f)

    except IOError:
        print ("Error: fail to splite anvil state")


#splite torch bloackstates
def changeTorchState(main_path, _str):
    try:
        with open(f'{main_path}/blockstates/{_str}torch.json','r', encoding="utf-8") as f:
            torch_dict = json.loads("\n".join(modify_json(f)))

        if 'facing=up' in torch_dict['variants']:
            torch_json = {
                'variants' : {
                    "": torch_dict['variants']["facing=up"]
                }
            }
            #print(torch_json)
            with open(f'{main_path}/blockstates/{_str}torch.json','w') as dump_f:
                json.dump(torch_json,dump_f)

        if 'facing=east' in torch_dict['variants']:
            if 'facing=up' in torch_dict['variants']:
                del torch_dict['variants']["facing=up"]
            wall_torch_json = torch_dict
            #print(wall_torch_json)

            with open(f'{main_path}/blockstates/{_str}wall_torch.json','w') as dump_f:
                json.dump(wall_torch_json,dump_f)
    except IOError:
        print ("Error: fail to splite " + _str + "torch state")

#change lever bloackstates
def changeLeverState(variants, lever_dict,  _str):
    if 'facing=east,powered=' + _str in lever_dict['variants']:
        model = lever_dict['variants']["facing=east,powered=" + _str]["model"]
        variants = {
            **variants,
            "face=wall,facing=north,powered=" + _str: { "model": model, "x": 90},
            "face=wall,facing=east,powered=" + _str: { "model": model, "x": 90, "y": 90 },
            "face=wall,facing=south,powered=" + _str: { "model": model, "x": 90, "y": 180 },
            "face=wall,facing=west,powered=" + _str: { "model": model, "x": 90, "y": 270 },
        }

    if 'facing=down_z,powered=' + _str in lever_dict['variants']:
        model = lever_dict['variants']["facing=down_z,powered=" + _str]["model"]
        variants = {
            **variants,
            "face=ceiling,facing=north,powered=" + _str: { "model": model, "x": 180, "y": 180 },
            "face=ceiling,facing=east,powered=" + _str: { "model": model, "x": 180, "y": 270 },
            "face=ceiling,facing=south,powered=" + _str: { "model": model, "x": 180},
            "face=ceiling,facing=west,powered=" + _str: { "model": model, "x": 180, "y": 90 },
        }

    if 'facing=up_z,powered=' + _str in lever_dict['variants']:
        model = lever_dict['variants']["facing=up_z,powered=" + _str]["model"]
        variants = {
            **variants,
            "face=floor,facing=north,powered=" + _str: { "model": model},
            "face=floor,facing=east,powered=" + _str: { "model": model,  "y": 90 },
            "face=floor,facing=south,powered=" + _str: { "model": model, "y": 180},
            "face=floor,facing=west,powered=" + _str: { "model": model, "y": 270 },
        }
    return variants

'''
---------------------------------------------------------------------------
                           resize change tex
---------------------------------------------------------------------------
'''



@logger.catch
def main(pack,
         destination,
         resolution,
         new_name,
         name_suffix,
         description,
         tex=False):
    is113 = False

    tmp_dir = tempfile.mkdtemp()

    # Packs can also be folders
    if zipfile.is_zipfile(pack):
        unzip_pack(pack, tmp_dir)

    # if not path.exists(f"{tmp_dir}/pack.mcmeta"):
    #     list_subfolders_with_paths = [
    #         f.path for f in os.scandir(pack) if f.is_dir()]
    #     PACK = list_subfolders_with_paths[0]

    MAIN_PATH = f'{tmp_dir}/assets/minecraft'
    TEX_PATH = f'{MAIN_PATH}/textures'
    block_path = f'{TEX_PATH}/blocks'
    item_path = f'{TEX_PATH}/items'
    entity_path = f'{TEX_PATH}/entity'

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
        res_r,
        pathlib.Path(pack).stem,
        new_name,
        name_suffix,
        description,
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
               res_r,
               old_name,
               new_name,
               name_suffix,
               description,
               tex=False):
    if res_r == 0:
        res_r = 1
    RES_R = int(math.pow(2, res_r))

    steps.make_missing_directories(main_path)
    changeFileName(
        main_path,
        block_path,
        item_path,
        entity_path,
    )
    changeFolderName(
        entity_path,
        texture_path
    )
    changeModel(
        main_path
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
            main_path,
            texture_path
        )
    zipup_pack(
        pack_path,
        destination,
        old_name,
        new_name,
        name_suffix
    )

from .common import *

pack_format = 5

newDirectories = [
    'textures/entity/signs'
]

entityList = [
    ["sign", "signs/oak"],
    ["snowman", "snow_golem"],
    ['cow/mooshroom', 'cow/red_mooshroom'],
    ['shulker/endergolem', 'shulker/shulker']
]

for _str in colorList:
    if _str != "light_gray":
        blockList.append(['wool_colored_' + _str, _str + '_wool'])
        blockList.append(['glass_' + _str, _str + '_stained_glass'])
        blockList.append(['glass_pane_top_' + _str, _str + '_stained_glass_pane_top'])
        blockList.append(['hardened_clay_stained_' + _str, _str + '_terracotta'])
        blockList.append(['concrete_powder_' + _str, _str + '_concrete_powder'])
        blockList.append(['concrete_' + _str, _str + '_concrete'])
        blockList.append(['glazed_terracotta_' + _str, _str + '_glazed_terracotta'])
        blockList.append(['shulker_top_' + _str, _str + '_shulker_box_top'])
    else:
        blockList.append(['wool_colored_silver', _str + '_wool'])
        blockList.append(['glass_silver', _str + '_stained_glass'])
        blockList.append(['glass_pane_top_silver', _str + '_stained_glass_pane_top'])
        blockList.append(['hardened_clay_stained_silver', _str + '_terracotta'])
        blockList.append(['concrete_powder_silver', _str + '_concrete_powder'])
        blockList.append(['concrete_silver', _str + '_concrete'])
        blockList.append(['glazed_terracotta_silver', _str + '_glazed_terracotta'])
        blockList.append(['shulker_top_silver', _str + '_shulker_box_top'])

for _str in woodenList:
    modelList.append([ _str + '_bark', _str + '_wood'])

#ITEMLIST： Dyes
for _str in colorList:
    if _str != "silver":
        itemList.append(['dye_powder_' + _str, _str + '_dye'])
    else:
        itemList.append(['dye_powder_' + _str, 'light_gray_dye'])

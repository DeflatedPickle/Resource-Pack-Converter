from .common import *

for _str in colorList:
    blockList.append(['wool_colored_' + _str, _str + '_wool'])
    blockList.append(['glass_' + _str, _str + '_stained_glass'])
    blockList.append(['glass_pane_top_' + _str, _str + '_stained_glass_pane_top'])
    blockList.append(['hardened_clay_stained_' + _str, _str + '_terracotta'])
    blockList.append(['concrete_powder_' + _str, _str + '_concrete_powder'])
    blockList.append(['concrete_' + _str, _str + '_concrete'])
    blockList.append(['glazed_terracotta_' + _str, _str + '_glazed_terracotta'])
    blockList.append(['shulker_top_' + _str, _str + '_shulker_box_top'])

#ITEMLIST： Dyes
for _str in colorList:
    itemList.append(['dye_powder_' + _str, _str + '_dye'])

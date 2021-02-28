# phantom
A tool for converting minecraft's resource pack from 1.8-1.12 to 1.13 or 1.15

## Usage
```
usage: phantom [-h] [-n [NAME]] [-s [SUFFIX]] [-d [DESTINATION]]
               [-f {1.13,1.15}] [--boxcraft]
               pack

a tool to convert Minecraft resource packs from 1.8-1.12 to 1.13 or 1.15

positional arguments:
  pack                  the pack location

optional arguments:
  -h, --help            show this help message and exit
  -n [NAME], --name [NAME]
                        the file name of the converted pack (default: None)
  -s [SUFFIX], --suffix [SUFFIX]
                        an extra string to add to the end of the converted
                        pack name (default: None)
  -d [DESTINATION], --destination [DESTINATION]
                        the directory the converted pack will be placed in
                        (default: None)
  -f {1.13,1.15}, --format {1.13,1.15}
                        the game version to convert to (default: 1.15)
  --boxcraft            toggles the BoxCraft texture fix (default: False)
```
### Example:
```
phantom oldpack.zip -s converted
```

## License
```
MIT License

Copyright (c) 2018 icrdr
Copyright (c) 2019 MamiyaOtaru
Copyright (c) 2020 trevorwarnerOIT
Copyright (c) 2021 DeflatedPickle
```

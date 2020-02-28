# CHANGELOG
All notable changes to this project will be documented in this file. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


		Resource-Pack-Converter - v1.2.0
		Created by: icrdr
        Fork by: Trevor W.

		Github Fork: https://github.com/trevor34/Resource-Pack-Converter

## Types of changes
    [Added] for new features.
    [Changed] for changes in existing functionality.
    [Deprecated] for soon-to-be removed features.
    [Removed] for now removed features.
    [Fixed] for any bug fixes.
    [Security] in case of vulnerabilities.

# [1.2.0] 2020-02-28
I'm updating this project to work along side a texture pack I'm updating, as well as update all packs to 1.15
# Added
- This changelog
- New button in convert_tool to convert Boxcraft
- There is some specific code to allow for the clean conversion of Boxcraft Reloaded.
    - Functionality to this code:
        - Removes 'natural' textures that minecraft adds to certain blocks
        - Removes furnace blockstate file that has issues with animation
        - Removes item frame model file to properly display items
        - Changes the animation properties of two blocks
    - These are all within the new main.FixTextures
- Added some additional files to convert
    - entity sign to sign/Oak
    - entity snowman to snow_golem
    - entity cow/mooshroom to cow/red_mooshroom
    - entity shulker/endergolem to shulker/shulker
    - model `woodtype`\_bark to `woodtype`\_wood
- Added the ability to create new directories
# Fixed
- Boat entities not properly added to entity list

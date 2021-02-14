#!/usr/bin/env just --justfile

alias h := usage
alias help := usage
alias i := readme
alias info := readme
alias l := license
alias b := build

export PYTHONOPTIMIZE := "1"

name := 'phantom'
version := '1.4.0'

icon_sizes := '16 32 64 128 256 512'
icon_temp_name := 'Phantom_JE1.png'
icon_url := 'https://static.wikia.nocookie.net/minecraft_gamepedia/images/a/a6/' + icon_temp_name + '/revision/latest'
icon_name := 'favicon'

download := './downloads/icon'

dist := './dist'
build := './build'
spec := './'

split := if os() == "windows" { ';' } else { ':' }

default:
	@just --list --unsorted

_requirements:
	pip install -r requirements.txt

# shows how to use phantom
usage:
	@src/cli.py -h

# shows the readme file
readme:
	@cat README.md

# shows the license file
license:
	@cat LICENSE

# count non-empty lines of code
sloc:
	@cat src/*.py | sed '/^\s*$/d' | wc -l

# makes the temporary directory
_make_temp_dir:
	-mkdir -p {{ build }}/icon
	-mkdir -p {{ dist }}/icon
	-mkdir -p {{ download }}/icon

# downloads the icon then runs _gen_icons
_download_icon: _make_temp_dir
	wget {{ icon_url }} -O "{{ download }}/icon/{{ icon_temp_name }}"

# resizes a given image
_resize_icon size:
	convert "{{ download }}/icon/{{ icon_temp_name }}" \
			-resize "{{ size }}x{{ size }}" \
			-background none \
			-gravity center \
			-extent "{{ size }}x{{ size }}" \
			"{{ build }}/icon/{{ size }}.png"

# generates scaled versions of the icon
_gen_icons: _download_icon
	for size in {{ icon_sizes }}; do just _resize_icon $size; done

# makes a windows icon file out of the icon images
_make_ico: _gen_icons
	#!/usr/bin/env bash
	set -euo pipefail
	convert $(ls {{ build }}/icon/*.png) {{ dist }}/icon/{{ icon_name }}.ico

_make_icns: _gen_icons
	#!/usr/bin/env bash
	set -euo pipefail
	png2icns {{ dist }}/icon/{{ icon_name }}.icns $(ls {{ build }}/icon/*.png | awk '$0 !~ "/64"')

# runs the pyinstaller build
build label=(name + '-' + version) type='file' level='INFO' debug='' upx='true': # _requirements _make_ico _make_icns
	#!/usr/bin/env bash
	set -euxo pipefail
	echo "Starting build for {{ os() }}"
	pyinstaller \
		`# general options` \
		--distpath {{ dist }} \
		--workpath {{ build }} \
		--clean \
		--log-level {{ level }} \
		`# what to generate` \
		{{ if type == 'dir' { '-D' } else { '-F' } }} \
		--specpath {{ spec }} \
		--name {{ label }} \
		`# what to bundle` \
		{{ if os() == "windows" { "--add-data {{ dist }}/icon/{{ icon_name }}.ico;." } else { '' } }} \
		{{ if os() == "macos" { "--add-data {{ dist }}/icon/{{ icon_name }}.icns:." } else { '' } }} \
		--add-data src/*.png{{ split }}. \
		`# how to generate` \
		{{ if debug != '' { "--debug {{ debug }}" } else { '' } }} \
		{{ if os() != "windows" { '--strip' } else { '' } }} \
		{{ if upx != 'true' { '--noupx' } else { '' } }} \
		--console \
		{{ if os() == "windows" { "--icon {{ dist }}/{{ icon_name }}.ico" } else { '' } }} \
		{{ if os() == "macos" { "--icon {{ dist }}/{{ icon_name }}.icns" } else { '' } }} \
		`# script to run` \
		./src/cli.py
	echo 'Finished building'
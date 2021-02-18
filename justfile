#!/usr/bin/env just --justfile

alias h := usage
alias help := usage
alias i := readme
alias info := readme
alias l := license
alias b := build

export PYTHONOPTIMIZE := "1"

download := './downloads'

dist := './dist'
build := './build'
spec := './'

name := 'phantom'
version := '1.4.0'

icon_sizes := '16 32 64 128 256 512'
icon_temp_name := 'Phantom_JE1.png'
icon_url := 'https://static.wikia.nocookie.net/minecraft_gamepedia/images/a/a6/' + icon_temp_name + '/revision/latest'
icon_name := 'favicon'
icon_destination := download + "/icon/" + icon_temp_name
icon_final := dist + "/icon/"+ icon_name

split := if os() == "windows" { ';' } else { ':' }

# shows the command list
default:
	@just --list --unsorted

# installs required python libraries
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
	curl {{ icon_url }} -o {{ icon_destination }}

# resizes a given image
_resize_icon size="256":
	#!/usr/bin/env bash
	set -euo pipefail

	# This is installed on Windows and Linux, but MacOS doesn't have it by default :^)
	if [ {{ os() }} = "macos" ]; then
		brew install imagemagick
	fi

	convert "{{ icon_destination }}" \
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
	convert "$(ls {{ build }}/icon/*.png)" "{{ dist }}/icon/{{ icon_name }}.ico"

_make_icns: _gen_icons
	#!/usr/bin/env bash
	set -euo pipefail

	# This package is also available on Linux but we'll never use this script on it
	if [ {{ os() }} = "macos" ]; then
		brew install libicns
	fi

	png2icns {{ dist }}/icon/{{ icon_name }}.icns $(ls {{ build }}/icon/*.png | awk '$0 !~ "/64"')

# runs the pyinstaller build
build label=(name + '-' + version) type='file' level='INFO' debug='all' upx='true': _requirements
	#!/usr/bin/env bash
	set -euo pipefail
	echo "Starting build for {{ os() }} ({{ arch() }})"

	# Make the icons for the OS we're on
	if [ {{ os() }} = "windows" ]; then
		just _make_ico;
	elif [ {{ os() }} = "macos" ]; then
		just _make_icns;
	fi

	if [ {{ os() }} = "windows" ]; then
		data="--add-data {{ icon_final }}.ico;."
		strip="--strip"
		icon="--icon {{ icon_final }}.ico"
	elif [ {{ os() }} = "macos" ]; then
		data="--add-data {{ icon_final }}.icns:."
		strip=""
		icon="--icon {{ icon_final }}.icns"
	else
		data=""
		strip=""
		icon=""
	fi

	if [ {{ debug }} != "" ]; then debug="--debug {{ debug }}"; else debug=""; fi

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
		$data \
		--add-data src/*.png{{ split }}. \
		`# how to generate` \
		$debug \
		$strip \
		{{ if upx != 'true' { '--noupx' } else { '' } }} \
		--console \
		$icon \
		`# script to run` \
		./src/cli.py
	echo 'Finished building'
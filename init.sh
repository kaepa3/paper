#!/bin/sh
git submodule update --init
touch .git/modules/pico/info/sparse-checkout
echo /MicroPython/network/ > .git/modules/pico/info/sparse-checkout

git -C pico config core.sparsecheckout true
git -C pico read-tree -mu HEAD



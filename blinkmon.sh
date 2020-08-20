#! /usr/bin/env bash

dir=$(dirname "$(realpath $0)")

. $dir/venv/bin/activate
python $dir/main.py

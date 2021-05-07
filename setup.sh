#!/usr/bin/env bash

curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3
mkdir -p "$HOME"/.bash_completion.d
poetry completions bash > "$HOME"/.bash_completion.d/poetry.bash-completion
echo 'source $HOME/.bash_completion.d/poetry.bash-completion' >> ~/.profile
poetry install

# pyformat-nvim

Based on [averms/black-nvim] but also runs isort and autoflake.

Features:

- It runs asynchronously, so it won't block scrolling while formatting the buffer.
- Checks if filetype is "python" before formatting.
- Uses the configured textwidth as black/isort line length by default.
- More robust error handling and better error messages.
- Only vital features (Upgrading the black package is left to the user).
- Don't have to clone the entire source repo just to get the plugin.
- Zero lines of Vimscript.

Todo:
- Find pyproject.toml and apply its configuration along with the Nvim configuration. 
- Add option to disable string normalization.

[averms/black-nvim]: https://github.com/averms/black-nvim

## Installation

The 'master' branch is stable.

| Plugin manager | How to install                                                     |
|----------------|--------------------------------------------------------------------|
| minpac         | `call minpac#add('maxdjohnson/pyformat-nvim')`                     |
| dein.vim       | `call dein#add('maxdjohnson/pyformat-nvim')`                       |
| vim-plug       | `Plug 'maxdjohnson/pyformat-nvim', {'do': ':UpdateRemotePlugins'}` |

If you don't already have a system for managing python environments on your computer
I would recommend the following:

- Make sure you have at least version 3.6.
- Set up a virtual environment for use with neovim.
  ```sh
  mkdir -p ~/.local/venv && cd ~/.local/venv
  python3 -m venv nvim
  cd nvim
  . ./bin/activate
  pip install pynvim black isort autoflake
  ```
- Tell neovim about that environment like so:
  ```vim
  let g:python3_host_prog = $HOME . '/.local/venv/nvim/bin/python'
  ```
- Run `:checkhealth`. The python3 provider section should be not-red.

## Documentation

See [blackisort.md](doc/blackisort.md) or type `:h blackisort.txt`.

## License

pyformat-nvim is distributed under the MIT/Expat license.
See LICENSE file for details.

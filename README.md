# black-isort-nvim

Based on [averms/black-nvim] but also runs isort

Features:

- It runs asynchronously, so it won't block scrolling while formatting the buffer.
- Checks if filetype is "python" before formatting.
- More robust error handling and better error messages.
- Only vital features (Upgrading the black package is left to the user).
- Don't have to clone the entire source repo just to get the plugin.
- Zero lines of Vimscript.

Todo:
- Find pyproject.toml and apply its configuration along with the Nvim configuration. 
- Add option to disable string normalization.

[averms/black-nvim]: https://github.com/averms/black-nvim

## Installation

The 'master' branch is stable. You can see what is coming up by looking at 'devel' but
I wouldn't recommend using it.

| Plugin manager | How to install                                             |
|----------------|------------------------------------------------------------|
| minpac         | `call minpac#add('maxdjohnson/black-isort-nvim')`                     |
| dein.vim       | `call dein#add('maxdjohnson/black-isort-nvim')`                       |
| vim-plug       | `Plug 'maxdjohnson/black-isort-nvim', {'do': ':UpdateRemotePlugins'}` |

If you don't already have a system for managing python environments on your computer
I would recommend the following:

- Make sure you have at least version 3.6.
- Set up a virtual environment for use with neovim.
  ```sh
  mkdir -p ~/.local/venv && cd ~/.local/venv
  python3 -m venv nvim
  cd nvim
  . ./bin/activate
  pip install pynvim black isort
  ```
- Tell neovim about that environment like so:
  ```vim
  let g:python3_host_prog = $HOME . '/.local/venv/nvim/bin/python'
  ```
- Run `:checkhealth`. The python3 provider section should be not-red.

## Documentation

See [blackisort.md](doc/blackisort.md) or type `:h blackisort.txt`.

## License

black-isort-nvim is distributed under the MIT/Expat license.
See LICENSE file for details.

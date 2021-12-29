## Introduction

pyformat-nvim formats your Python buffer asynchronously using one or more formatter tools. It
currently supports [autoflake], [black], and [isort]. Its interface is simple: it defines a
function, |PyFormat()|, that formats the entire buffer.

[autoflake]: https://github.com/myint/autoflake
[black]: https://github.com/psf/black
[isort]: https://github.com/psf/isort

## Usage

You can set `PyFormat()` to a command, key mapping, or just call it directly.

You can also use `PyFormatSync()` to format your buffer synchronously. This can be used in the
|BufWritePre| autocmd to format your buffer on save.

For example, you can put the following commands in after/ftplugin/python.vim to map `gO` to organize
imports with autoflake and isort and format with black and isort automatically on save:

```vim
" map gO to "organize imports" using autoflake to remove unused and isort to sort
let g:autoflake#settings = { 'remove_all_unused_imports': 1 }
autocmd FileType python map <buffer> gO :call PyFormat('autoflake', 'isort')<CR>

" format with black and isort on save
autocmd BufWritePre *.py execute ':call PyFormatSync("black", "isort")'
```

## Black Configuration

Use `g:black#settings`
For example:

```vim
let g:black#settings = {
    \ 'fast': 1,
    \ 'line_length': 100
\}
```

- `fast` (default: 0)
  Set to a non-zero number to skip the AST check. This makes formatting a lot faster.
- `line_length` (default: 88)
  Set to an integer to tell Black where to wrap lines.

## Isort Configuration

Use `g:isort#settings`
For example:

```vim
let g:isort#settings = {
    \ 'profile': 'black',
\}
```

## Autoflake Configuration

Use `g:autoflake#settings`
For example:

```vim
let g:autoflake#settings = {
    \ 'remove_all_unused_imports': 1,
\}
```

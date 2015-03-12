# Renaming Files in Vim
Most of the time, I have multiple buffers up in vim. They get opened lots of different ways:

- Starting vim with a glob (`vim path/to/files/*.py`)
- Editing a file from an existing vim session (`:e ../../somefile.rst`)
- Using [ctrlp][] or [ag][] within to find a file and create a new buffer (`C-p, *pattern*, <Enter>`)

... then I start editing the file and realize the name should be changed. There are a couple ways to do this:

1. Save all buffers and exit vim with `wqa`, then rename the file in the shell. This is the most obvious, and what I did
   for years. It's extremely inefficient, and all the methods below are much better. :)
2. Save the buffer with `:w[rite] <filename>` or `:saveas <filename>` and remove the old file with `!rm <filename>`.
3. We could write a vim-script to do above, but [Tim Pope][] has already done this for us. The [vim-eunuch][] package
   provides a `:Rename` command for just this purpose.
4. Bonus: If it's a git repository, we can use [vim-fugitive][]'s `:GMove` command to rename the file, delete the old file, and
   update the *git repository* at the same time.

Both [vim-eunuch][] and [vim-fugitive][] respect the buffers path, even with multiple buffers open. So if we open files
with ` vim file1.py dir/file2.py` and with the *file2.py* buffer active run `:Rename ../file3.py`, this will move
*dir/file2.py* to *file3.py*, just as we'd like. Similarly, with *file1.py* active, `:Rename dir/file1.py` will move the
*file1.py* to *dir/file1.py*.


<!-- References -->
[ctrlp]:        https://github.com/kien/ctrlp.vim
[ag]:           https://github.com/ggreer/the_silver_searcher
[Tim Pope]:     https://github.com/tpope
[vim-eunuch]:   https://github.com/tpope/vim-eunuch
[vim-fugitive]: https://github.com/tpope/vim-fugitive

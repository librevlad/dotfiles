"-----------------------------------------------------------
"--[ Basic setup] ------------------------------------------
"----------------------------------------------------------

syntax enable                     " Turn on syntax highlighting.
syntax on
filetype plugin indent on         " Turn on file type detection.

set showcmd                       " Display incomplete commands.
set showmode                      " Display the mode you're in.
set backspace=indent,eol,start    " Intuitive backspacing.
set hidden                        " Handle multiple buffers better.
set wildmenu                      " Enhanced command line completion.
set wildmode=list:longest         " Complete files like a shell.
set ignorecase                    " Case-insensitive searching.
set smartcase                     " But case-sensitive if expression contains a capital letter.
set number                        " Show line numbers.
set ruler                         " Show cursor position.
set incsearch                     " Highlight matches as you type.
set hlsearch                      " Highlight matches.
set wrap                          " Turn on line wrapping.
set scrolloff=3                   " Show 3 lines of context around the cursor.
set title                         " Set the terminal's title
set visualbell                    " No beeping.
set nobackup                      " Don't make a backup before overwriting a file.
set nowritebackup                 " And again.
set noswapfile                    " Don't use swap files, they are annoying!
set tabstop=2                     " Global tab width.
set softtabstop=2
set shiftwidth=2                  " And again, related.
set expandtab                     " Use spaces instead of tabs
set modelines=0
set encoding=utf-8
set autoindent
set cursorline
set ttyfast
set gdefault
set showmatch
set textwidth=79
set formatoptions=qrn1
set linebreak
set nolist

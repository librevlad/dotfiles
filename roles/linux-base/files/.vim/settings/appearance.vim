"Invisible character colors
highlight NonText guifg=#A9A9A9
highlight SpecialKey guifg=#A9A9A9


" Theme
"
" set background=light
set guifont=Fira\ Code\ 15
"set guifont=Input\ Mono\ 13
set guioptions-=m  "remove menu bar
set guioptions-=T " Removes top toolbar
set guioptions-=r " Removes right hand scroll bar
set go-=L " Removes left hand scroll bar
set go-=F " Removes footer?
set go-=l " Removes left hand scroll bar
set go-=r " Removes left hand scroll bar
set go-=R " Removes left hand scroll bar
set go-=e " tabs



set linespace=10
"
" Force the right number of colours, if the terminal supports it, but
" vim doesn't realise
if $TERM == "xterm-256color" || $TERM == "screen-256color" || $COLORTERM == "gnome-terminal"
  set t_Co=256
endif

colorscheme atom-dark-256
if has('gui_running')
  colorscheme atom-dark
endif
hi StatusLine ctermfg=7 ctermbg=0 guibg=bg
hi StatusLineNC ctermfg=7 ctermbg=0 guibg=bg

highlight Pmenu ctermfg=251 ctermbg=234 guifg=#ebebeb guibg=#232323 
highlight PmenuSel ctermfg=12 ctermbg=0 guifg=#ffffff guibg=#994444 
highlight vertsplit guifg=bg guibg=bg
hi LineNr guibg=bg

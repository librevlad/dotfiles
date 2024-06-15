
" Fast saves
nmap <leader>w :w!<cr>
nmap <leader>fmt mpgg=G`p


" --------------------------------------------------------
" --[ Navigation ]----------------------------------------
" --------------------------------------------------------

nnoremap <leader>cd :cd %:p:h<CR>

" For skipping between buffers

nmap ]b :bnext<CR>
nmap [b :bprev<CR>

" Tabs
nnoremap ]t :tabnext<CR>
nnoremap [t :tabprevious<CR>


"easier window navigation

nmap <C-h> <C-w>h
nmap <C-j> <C-w>j
nmap <C-k> <C-w>k
nmap <C-l> <C-w>l

nmap <leader>q :q<cr>

nnoremap j gj
nnoremap k gk

" unnmap arrows

"noremap <Right> <nop>
"noremap <Left> <nop>
"noremap <Up> <nop>
"noremap <Down> <nop>


"Resize vsplit
nmap <C-v> :vertical resize +5<cr>
nmap 25 :vertical resize 30<cr>
nmap 50 <c-w>=
nmap 75 :vertical resize 100<cr>
" no highlight
nnoremap <leader><space> :noh<cr>


" source current file
nnoremap sop :source %<CR>

" To fold tags (for html)
nnoremap <leader>ft Vatzf

imap jj <Esc>


" Set wrapping
nmap \w :setlocal wrap!<CR>:setlocal wrap?<CR>


" handy way of editing .vimrc
nnoremap <leader>rc :e ~/.vim/vimrc<CR>
nnoremap <leader>rcc :e ~/.vim/vimrc<CR>
nnoremap <leader>rcm :e ~/.vim/settings/mappings.vim<CR>
nnoremap <leader>rcp :e ~/.vim/settings/plugins.vim<CR>
nnoremap <leader>rcb :e ~/.vim/settings/basic.vim<CR>
nnoremap <leader>rca :e ~/.vim/settings/appearance.vim<CR>

" make Ctrl-Z work
map <C-z> <Esc>
nnoremap <C-z> <Esc>u
imap <C-z> <Esc>ui


" normal copy/paste
:set clipboard=unnamedplus
:smap <Del> <C-g>"_d
:smap <C-c> <C-g>y
:smap <C-x> <C-g>x
:imap <C-v> <Esc>pi
:smap <C-v> <C-g>p

" make normal tab?
:smap <Tab> <C-g>1>
:smap <S-Tab> <C-g>1<


" For when you forget to sudo.. Really Write the file.
cmap w!! w !sudo tee % >/dev/null

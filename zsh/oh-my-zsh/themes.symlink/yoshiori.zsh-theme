# Here are the colours from Textmate's Monokai theme:
# 
# Black: 0, 0, 0
# Red: 229, 34, 34
# Green: 166, 227, 45
# Yellow: 252, 149, 30
# Blue: 196, 141, 255
# Magenta: 250, 37, 115
# Cyan: 103, 217, 240
# White: 242, 242, 242

# https://github.com/olivierverdier/zsh-git-prompt
# source $ZSH/../.oh-my-zsh-git-prompt/zshrc.sh
# source ~/.oh-my-zsh-git-prompt/zshrc.sh
source ~/github.SSeleznyov/zsh-git-prompt/zshrc_singleCommand.sh

# The prompt
PROMPT='%{$fg[magenta]%}┌[%{$fg[green]%}%~%{$fg[magenta]%}]
└> %{$reset_color%}$(git_super_status)%{$reset_color%}'

# └> %{$reset_color%}$(git_prompt_info)%{$reset_color%}'

# The right-hand prompt
# RPROMPT='$(git_prompt_status) %{$reset_color%}$(git_prompt_stash_count)$(git_prompt_modified_count)%{$reset_color%} ${time}'
# RPROMPT='$(git_prompt_status) %{$reset_color%}$(git_prompt_stash_count)%{$reset_color%} ${time}'
RPROMPT='%{$reset_color%}$(git_prompt_stash_count)%{$reset_color%} ${time}'

# local time, color coded by last return code
time_enabled="%(?.%{$fg[green]%}.%{$fg[red]%})%*%{$reset_color%}"
time_disabled="%{$fg[green]%}%*%{$reset_color%}"
time=$time_enabled

ZSH_THEME_GIT_PROMPT_PREFIX="%{$fg[magenta]%}[on %{$fg[red]%}"
ZSH_THEME_GIT_PROMPT_SUFFIX="%{$fg[magenta]%}] %{$reset_color%}"
ZSH_THEME_GIT_PROMPT_DIRTY="%{$fg[yellow]%} ☂" # Ⓓ
# ZSH_THEME_GIT_PROMPT_UNTRACKED="%{$fg[cyan]%} ✭" # ⓣ
# ZSH_THEME_GIT_PROMPT_CLEAN="%{$fg[green]%} ☀" # Ⓞ

ZSH_THEME_GIT_PROMPT_ADDED="%{$fg[cyan]%} ✚" # ⓐ ⑃
ZSH_THEME_GIT_PROMPT_MODIFIED="%{$fg[yellow]%} ⚡"  # ⓜ ⑁
ZSH_THEME_GIT_PROMPT_DELETED="%{$fg[red]%} ✖" # ⓧ ⑂
ZSH_THEME_GIT_PROMPT_RENAMED="%{$fg[blue]%} ➜" # ⓡ ⑄
ZSH_THEME_GIT_PROMPT_UNMERGED="%{$fg[magenta]%} ♒" # ⓤ ⑊

ZSH_THEME_GIT_PROMPT_STASH_COUNT_BEFORE="%{$fg[yellow]%} 【%{$fg[green]%}⚒ "
ZSH_THEME_GIT_PROMPT_STASH_COUNT_AFTER="%{$fg[yellow]%}】"

ZSH_THEME_GIT_PROMPT_MODIFIED_COUNT_BEFORE="%{$fg[yellow]%} 【%{$fg[green]%}⬆ "
ZSH_THEME_GIT_PROMPT_MODIFIED_COUNT_AFTER="%{$fg[yellow]%}】"

# More symbols to choose from:
# ☀ ✹ ☄ ♆ ♀ ♁ ♐ ♇ ♈ ♉ ♚ ♛ ♜ ♝ ♞ ♟ ♠ ♣ ⚢ ⚲ ⚳ ⚴ ⚥ ⚤ ⚦ ⚒ ⚑ ⚐ ♺ ♻ ♼ ☰ ☱ ☲ ☳ ☴ ☵ ☶ ☷
# ✡ ✔ ✖ ✚ ✱ ✤ ✦ ❤ ➜ ➟ ➼ ✂ ✎ ✐ ⨀ ⨁ ⨂ ⨍ ⨎ ⨏ ⨷ ⩚ ⩛ ⩡ ⩱ ⩲ ⩵  ⩶ ⨠ 
# ⬅ ⬆ ⬇ ⬈ ⬉ ⬊ ⬋ ⬒ ⬓ ⬔ ⬕ ⬖ ⬗ ⬘ ⬙ ⬟  ⬤ 〒 ǀ ǁ ǂ ĭ Ť Ŧ

# git stash count
function git_prompt_stash_count(){
  COUNT=$(git stash list 2>/dev/null | wc -l | tr -d ' ')
  if [ "$COUNT" -gt 0 ]; then
    echo "$ZSH_THEME_GIT_PROMPT_STASH_COUNT_BEFORE$COUNT$ZSH_THEME_GIT_PROMPT_STASH_COUNT_AFTER"
  fi
}

function git_prompt_modified_count(){
  # git diff --cached --numstat | wc -l
  COUNT=$(git diff --numstat 2>/dev/null | wc -l | tr -d ' ')
  if [ "$COUNT" -gt 0 ]; then
    echo "$ZSH_THEME_GIT_PROMPT_MODIFIED_COUNT_BEFORE$COUNT$ZSH_THEME_GIT_PROMPT_MODIFIED_COUNT_AFTER"
  fi
}
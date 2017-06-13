# Based on:
# https://github.com/olivierverdier/zsh-git-prompt

# To install source this file from your .zshrc file

# see documentation at http://linux.die.net/man/1/zshexpn
# A: finds the absolute path, even if this is symlinked
# h: equivalent to dirname
export __GIT_PROMPT_DIR=${0:A:h}

# Initialize colors.
autoload -U colors
colors

# Allow for functions in the prompt.
setopt PROMPT_SUBST

autoload -U add-zsh-hook

add-zsh-hook chpwd chpwd_update_git_vars
add-zsh-hook preexec preexec_update_git_vars
add-zsh-hook precmd precmd_update_git_vars

## Function definitions
function preexec_update_git_vars() {
    case "$2" in
        git*|hub*|gh*|stg*)
        __EXECUTED_GIT_COMMAND=1
        ;;
    esac
}

function precmd_update_git_vars() {
    if [ -n "$__EXECUTED_GIT_COMMAND" ] || [ ! -n "$ZSH_THEME_GIT_PROMPT_CACHE" ]; then
        update_current_git_vars
        unset __EXECUTED_GIT_COMMAND
    fi
}

function chpwd_update_git_vars() {
    update_current_git_vars
}

function update_current_git_vars() {
    unset __CURRENT_GIT_STATUS

    _GIT_STATUS=`git status --porcelain --branch &> /dev/null | $__GIT_PROMPT_DIR/git-status-prompt.py`

    __CURRENT_GIT_STATUS=("${(@s: :)_GIT_STATUS}")
     
    GIT_BRANCH_LOCAL=$__CURRENT_GIT_STATUS[1]
    GIT_BRANCH_REMOTE=$__CURRENT_GIT_STATUS[2]
    GIT_AHEAD=$__CURRENT_GIT_STATUS[3]
    GIT_BEHIND=$__CURRENT_GIT_STATUS[4]

    GIT_STAGED_DELETED=$__CURRENT_GIT_STATUS[5]
    GIT_STAGED_ADDED=$__CURRENT_GIT_STATUS[6]
    GIT_STAGED_MODIFIED=$__CURRENT_GIT_STATUS[7]

    GIT_UNSTAGED_DELETED=$__CURRENT_GIT_STATUS[8]
    GIT_UNSTAGED_ADDED=$__CURRENT_GIT_STATUS[9]
    GIT_UNSTAGED_MODIFIED=$__CURRENT_GIT_STATUS[10]

    GIT_CONFLICTS=$__CURRENT_GIT_STATUS[11]

    GIT_CLEAN=$__CURRENT_GIT_STATUS[12]
    GIT_CHANGED=$__CURRENT_GIT_STATUS[13]
}


git_status_prompt() {
  precmd_update_git_vars
    if [ -n "$__CURRENT_GIT_STATUS" ]; then
        STATUS="$ZSH_THEME_GIT_PROMPT_PREFIX$ZSH_THEME_GIT_PROMPT_BRANCH_LOCAL$GIT_BRANCH_LOCAL%{${reset_color}%}"
      
        if [ -n "$GIT_BRANCH_REMOTE" ]; then
            STATUS="$STATUS$ZSH_THEME_GIT_PROMPT_BRANCH_REMOTE$GIT_BRANCH_REMOTE%{${reset_color}%}"
        fi

        if [ "$GIT_BEHIND" -ne "0" ]; then
            STATUS="$STATUS$ZSH_THEME_GIT_PROMPT_BEHIND$GIT_BEHIND%{${reset_color}%}"
        fi
        if [ "$GIT_AHEAD" -ne "0" ]; then
            STATUS="$STATUS$ZSH_THEME_GIT_PROMPT_AHEAD$GIT_AHEAD%{${reset_color}%}"
        fi

        if [ "$GIT_CHANGED" = "True" ]; then
            STATUS="$STATUS$ZSH_THEME_GIT_PROMPT_SEPARATOR"
        fi

        if [ "$GIT_STAGED_ADDED" -ne "0" ]; then
            STATUS="$STATUS$ZSH_THEME_GIT_PROMPT_STAGED_ADDED$GIT_STAGED_ADDED%{${reset_color}%}"
        fi
        if [ "$GIT_STAGED_MODIFIED" -ne "0" ]; then
            STATUS="$STATUS$ZSH_THEME_GIT_PROMPT_STAGED_MODIFIED$GIT_STAGED_MODIFIED%{${reset_color}%}"
        fi
        if [ "$GIT_STAGED_DELETED" -ne "0" ]; then
            STATUS="$STATUS$ZSH_THEME_GIT_PROMPT_STAGED_DELETED$GIT_STAGED_DELETED%{${reset_color}%}"
        fi

        if [ "$GIT_UNSTAGED_ADDED" -ne "0" ]; then
            STATUS="$STATUS$ZSH_THEME_GIT_PROMPT_UNSTAGED_ADDED$GIT_UNSTAGED_ADDED%{${reset_color}%}"
        fi
        if [ "$GIT_UNSTAGED_MODIFIED" -ne "0" ]; then
            STATUS="$STATUS$ZSH_THEME_GIT_PROMPT_UNSTAGED_MODIFIED$GIT_UNSTAGED_MODIFIED%{${reset_color}%}"
        fi
        if [ "$GIT_UNSTAGED_DELETED" -ne "0" ]; then
            STATUS="$STATUS$ZSH_THEME_GIT_PROMPT_UNSTAGED_DELETED$GIT_UNSTAGED_DELETED%{${reset_color}%}"
        fi

        if [ "$GIT_CONFLICTS" -ne "0" ]; then
            STATUS="$STATUS$ZSH_THEME_GIT_PROMPT_CONFLICTS$GIT_CONFLICTS%{${reset_color}%}"
        fi

        if [ "$GIT_CLEAN" = "True" ]; then
            STATUS="$STATUS$ZSH_THEME_GIT_PROMPT_CLEAN"
        fi

        STATUS="$STATUS%{${reset_color}%}$ZSH_THEME_GIT_PROMPT_SUFFIX"
        echo "$STATUS"

    fi
}

# Default values for the appearance of the prompt. Configure at will.
ZSH_THEME_GIT_PROMPT_PREFIX="("
ZSH_THEME_GIT_PROMPT_SUFFIX=")"
ZSH_THEME_GIT_PROMPT_SEPARATOR=" | "
ZSH_THEME_GIT_PROMPT_BRANCH_LOCAL="%{$fg[green]%}"
ZSH_THEME_GIT_PROMPT_BRANCH_REMOTE="%{$fg[blue]%}➟"

ZSH_THEME_GIT_PROMPT_AHEAD="%{↑%G%}"
ZSH_THEME_GIT_PROMPT_BEHIND="%{↓%G%}"

ZSH_THEME_GIT_PROMPT_STAGED_DELETED="%{$fg[green]%}%{-%G%}"
ZSH_THEME_GIT_PROMPT_STAGED_ADDED="%{$fg[green]%}%{+%G%}"
ZSH_THEME_GIT_PROMPT_STAGED_MODIFIED="%{$fg[green]%}%{~%G%}"

ZSH_THEME_GIT_PROMPT_UNSTAGED_DELETED="%{$fg[red]%}%{-%G%}"
ZSH_THEME_GIT_PROMPT_UNSTAGED_ADDED="%{$fg[red]%}%{+%G%}"
ZSH_THEME_GIT_PROMPT_UNSTAGED_MODIFIED="%{$fg[red]%}%{~%G%}"

ZSH_THEME_GIT_PROMPT_CONFLICTS="%{$fg[yellow]%}%{✖%G%}"

ZSH_THEME_GIT_PROMPT_CLEAN="%{$fg[green]%}%{✔%G%}"
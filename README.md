# Dotfiles
@SergeySeleznyov's dotfiles

## oh-my-zsh screenshots

![screenshot1](/zsh/Screenshot1.png)
![screenshot2](/zsh/Screenshot2.png)

### Prompt

Left-side prompt (from left to right):

  1. Local branch name
  2. '->' Remote branch name
  3. Behind commits count
  4. Ahead commits count
  5. '|' separator if needed
  6. '+' added to index (in green)
  7. '~' updated in index (in green)
  8. '-' deleted in index (in green)
  9. '+' untracked (in red)
  10. '~' updated not in index (in red)
  11. '-' deleted not in index (in red)
  12. 'x' conflict count
  
Right-side prompt (from left to right):

  1. stash count
  2. prompt time

## Requirements

* oh-my-zsh

* python

## Install

1. Clone it into your home derectory, like follow:

```bash
git clone git://github.com/SergeySeleznyov/dotfiles.git ~/.dotfiles
```

or, if you have several authors dotfiles:

```bash
git clone git://github.com/SergeySeleznyov/dotfiles.git ~/.dotfiles/SergeySeleznyov
```

2. Run the [setup.sh](setup.sh) script

it will create the symlinks

## Thanks

Thanks to the dotfiles authors who inspired me:

* [holman](https://github.com/holman/dotfiles)

* [thoughtbot](https://github.com/thoughtbot/dotfiles)

* [mattstauffer](https://github.com/mattstauffer/ohmyzsh-dotfiles)

Thanks to the [yoshiori](https://github.com/yoshiori/oh-my-zsh-yoshiori) the author of the _oh-my-zsh_'s theme which is used as the default.

Thanks to the [olivierverdier](https://github.com/olivierverdier/zsh-git-prompt) the _oh-my-zsh_'s git status prompt author, who has inspired for deeply customizing it.

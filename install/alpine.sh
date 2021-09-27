#/bin/bash

apk update
apk add --no-cache git bash curl wget stow vim

# install zsh
apk add --no-cache zsh zsh-vcs

# install zplug
apk --no-cache add ncurses # tput
curl -sL --proto-redir -all,https https://raw.githubusercontent.com/zplug/installer/master/installer.zsh | zsh

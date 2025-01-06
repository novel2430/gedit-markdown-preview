#!/bin/sh

version=$(gedit --version | awk '{print $4}' | cut -d'.' -f1)
compare_version=47

if [ -z "$HOME" ]; then
  echo 'Where is ur $HOME ?'
else
  # Do install
  if [ "$version" -ge "$compare_version" ]; then
    install_dir=$HOME/.local/share/gedit/plugins
    mkdir -p "$install_dir"
    echo "Installing plugin files in $install_dir"
    cp md_preview.plugin "$install_dir"/md_preview.plugin
    cp -r md_preview "$install_dir"/
    echo "Done!"
  else
    echo "gedit version must > 47.0"
  fi
fi

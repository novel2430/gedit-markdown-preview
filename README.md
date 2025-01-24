# Gedit Markdown Preview Plugin

This plugin adds Markdown preview functionality to Gedit, providing a convenient way to render and interact with Markdown files directly within the editor.

> This plugin was developed because the code changes a lot in Gedit after upgrading to `Gedit 47` caused the previous Markdown preview plugin to no longer function properly. 

## Features

- 👀 **Real-Time Rendering**: Automatically render Markdown in a side panel as you edit.
- 👇 **Cursor Synchronization**: Keep the preview and editor synchronized as you navigate through your Markdown file.
- 🌙 **Dark Mode Support**: Switch the rendered markdown to dark mode at any time.
- 🚀 **Copy Code Blocks**: Easily copy code blocks from the preview.
- 📄 **Export to PDF**: Generate a PDF file from your Markdown content with a single click.
- 🌐 **Embedded HTML Support**: Support proper display of embedded HTML text within markdown. 
- ⚙️ **Customize the Font and CSS style**: Just head to the settings to tweak the font and CSS for the markdown preview.

## Screenshots
![img](https://github.com/novel2430/gedit-markdown-preview/blob/main/res/light.png?raw=true)
![img](https://github.com/novel2430/gedit-markdown-preview/blob/main/res/dark.png?raw=true)
### Cursor Synchronization
<video src="https://github.com/novel2430/gedit-markdown-preview/raw/refs/heads/main/res/cursor.mp4" width="90%" controls></video>
[tt](https://github.com/novel2430/gedit-markdown-preview/raw/refs/heads/main/res/cursor.mp4)
### Dark Mode
<video src="https://github.com/novel2430/gedit-markdown-preview/raw/refs/heads/main/res/dark.mp4" width="90%" controls></video>
### Custom Fonts
<video src="https://github.com/novel2430/gedit-markdown-preview/raw/refs/heads/main/res/font.mp4" width="90%" controls></video>
### Custom CSS Theme
<video src="https://github.com/novel2430/gedit-markdown-preview/raw/refs/heads/main/res/css.mp4" width="90%" controls></video>

## Requirements
### Dependencies
- [Gedit](https://gedit-text-editor.org/) 47.0 or later.
- [Python 3](https://www.python.org/)
- webkit2gtk [Arch](https://archlinux.org/packages/extra/x86_64/webkit2gtk/) / [Nix](https://github.com/NixOS/nixpkgs/blob/nixos-24.11/pkgs/development/libraries/webkitgtk/default.nix#L280)
- python-gobject [Arch](https://archlinux.org/packages/extra/x86_64/python-gobject/) / [Nix](https://github.com/NixOS/nixpkgs/blob/nixos-24.11/pkgs/development/python-modules/pygobject/3.nix#L73)
- (Option) For playing media in markdown preview
    - gstreamer [Arch](https://archlinux.org/packages/extra/x86_64/gstreamer/) / [Nix](https://github.com/NixOS/nixpkgs/blob/nixos-24.11/pkgs/development/libraries/gstreamer/core/default.nix#L137)    
    - gst-plugins-base [Arch](https://archlinux.org/packages/extra/x86_64/gst-plugins-base/) / [Nix](https://github.com/NixOS/nixpkgs/blob/nixos-24.11/pkgs/development/libraries/gstreamer/base/default.nix#L172)
    - gst-plugins-good [Arch](https://archlinux.org/packages/extra/x86_64/gst-plugins-good/) / [Nix](https://github.com/NixOS/nixpkgs/blob/nixos-24.11/pkgs/development/libraries/gstreamer/good/default.nix#L211)
    - gst-plugins-bad [Arch](https://archlinux.org/packages/extra/x86_64/gst-plugins-bad/) / [Nix](https://github.com/NixOS/nixpkgs/blob/nixos-24.11/pkgs/development/libraries/gstreamer/bad/default.nix#L368)
- (Option) For fetching URL in markdown preview
    - glib-networking [Arch](https://archlinux.org/packages/extra/x86_64/glib-networking/) / [Nix](https://github.com/NixOS/nixpkgs/blob/nixos-24.11/pkgs/by-name/gl/glib-networking/package.nix#L97)
### Install (All Dependencies)
- Arch
    ```sh
    sudo pacman -S gedit \
        webkit2gtk \
        gstreamer \
        gst-plugins-base \
        gst-plugins-good \
        gst-plugins-bad 
    ```
- Nix  
    On NixOS, the system differs significantly from others; the following command line primarily serves to display the names of the dependency packages.
    ```sh
    nix-shell -p gedit \
        python312Packages.pygobject3 \
        webkitgtk_4_0 \
        gst_all_1.gstreamer \
        gst_all_1.gst-plugins-base \
        gst_all_1.gst-plugins-good \
        gst_all_1.gst-plugins-bad \
        glib-networking
    ```
    I haven't figured out the most suitable packaging approach for this plugin on Nix yet, so I wrote a [custom package](https://github.com/novel2430/MyNUR/blob/master/pkgs/gedit/default.nix) and published it on NUR. The downside is that it also **bundles the gedit core**, which makes it less modular.
## Installation

1. **Download the Plugin**:  
   Clone or download this repository to your local machine.

   ```bash
   git clone https://github.com/novel2430/gedit-markdown-preview.git
   ```

2. **Copy the Plugin Files**:  
   - Manual Way  
   Move the plugin files to Gedit's plugin directory:
   ```bash
   cd gedit-markdown-preview
   mkdir -p ~/.local/share/gedit/plugins
   cp -r md_preview ~/.local/share/gedit/plugins/
   cp md_preview.plugin ~/.local/share/gedit/plugins/
   ```
   - Using Script  
   ```bash
   cd gedit-markdown-preview
   sh install.sh
   ```

3. **Enable the Plugin**:
   - Open Gedit.
   - Go to `Preferences` > `Plugins`.
   - Find `Markdown-Preview` in the list and enable it.

## Manual Customization

The config file is located at `~/.config/gedit-markdown-preview/settings.json`, where you can customize settings for `css`, `font`, and `is-dark`. 
```json
# ~/.config/gedit-markdown-preview/settings.json
{
    "css": "<ur .css path>",
    "font": "<ur font path>",
    "is-dark": false
}
```

## Contributing

Contributions are welcome! If you encounter bugs or have feature requests, feel 
free to open an issue or submit a pull request.


## Acknowledgments

Special thanks to the open-source community for providing inspiration and resources for this plugin.   

- **[markdown-it](https://github.com/markdown-it/markdown-it)**  
> md_preview/deps/markdown-it.min.js

For its incredible markdown-to-HTML conversion features. It's packed with options and backed by clear, well-written documentation.  
License: **MIT**
- **[highlight.js](https://highlightjs.org/)**  
> md_preview/deps/highlight.min.js  
> md_preview/deps/github.min.css  
> md_preview/deps/github-dark.min.css

For providing beautiful CSS styles for syntax highlighting, making code snippets pop!  
License: **BSD 3-Clause**
- **[github-markdown-css](https://github.com/sindresorhus/github-markdown-css)**  
> md_preview/deps/github-markdown-dark.css  
> md_preview/deps/github-markdown-light.css

For offering clean, GitHub-style markdown preview CSS that makes everything look polished.  
License: **MIT** 
- **[Noto Sans](https://fonts.google.com/noto)**  
> md_preview/fonts/NotoSans.ttf  
> md_preview/fonts/NotoSansSC.ttf  
> md_preview/fonts/NotoSansTC.ttf

For significantly improving the readability of Chinese text with its elegant font design.  
License: **SIL Open Font License (OFL) 1.1**

---

Happy Markdown editing! ☕


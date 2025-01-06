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

## Installation

1. **Download the Plugin**:
   Clone or download this repository to your local machine.

   ```bash
   git clone https://github.com/novel2430/gedit-markdown-preview.git
   ```

2. **Copy the Plugin Files**:
   Move the plugin files to Gedit's plugin directory:

   ```bash
   cd gedit-markdown-preview
   mkdir -p ~/.local/share/gedit/plugins
   cp -r md_preview ~/.local/share/gedit/plugins/
   cp md_preview.plugin ~/.local/share/gedit/plugins/
   ```

3. **Enable the Plugin**:
   - Open Gedit.
   - Go to `Preferences` > `Plugins`.
   - Find `Markdown-Preview` in the list and enable it.

## Screenshots

## Requirements

- Gedit 3.37 or later.
- Python 3.
- Required dependencies:
  - `markdown`
  - `pygtk` or `gi` for GTK integration

Install dependencies using pip:

```bash
pip install markdown
```

## Customization

- **Theme Matching**: The plugin detects Gedit's theme and adjusts the preview accordingly.
- **Keyboard Shortcuts**: Customize shortcuts for toggling the preview and exporting to PDF via Gedit's preferences.

## Contributing

Contributions are welcome! If you encounter bugs or have feature requests, feel 
free to open an issue or submit a pull request.

## License

## Acknowledgments

Special thanks to the open-source community for providing inspiration and resources for this plugin.

---

Happy Markdown editing!


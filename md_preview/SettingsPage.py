import os
from gi.repository import Gtk

class SettingsPage(Gtk.Window):
    def __init__(self, parent, func) -> None:
        super().__init__(title="Settings Page")
        # Window Setup
        self.set_default_size(600, 400)
        self.set_border_width(10)
        self.set_transient_for(parent)
        self.set_modal(True)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(vbox)
        # CSS chooser
        self.css_chooser_box, self.css_chooser_entry = self._get_chooser_box(name="CSS", func=self._on_css_file_select)
        vbox.pack_start(self.css_chooser_box, False, False, 0)
        # Font chooser
        self.font_chooser_box, self.font_chooser_entry = self._get_chooser_box(name="Font", func=self._on_font_file_select)
        vbox.pack_start(self.font_chooser_box, False, False, 0)
        # Deafult CheckBox
        self.defualt_css_check = Gtk.CheckButton(label="Reset to default CSS")
        vbox.pack_start(self.defualt_css_check, False, False, 0)
        self.defualt_font_check = Gtk.CheckButton(label="Reset to default Font")
        vbox.pack_start(self.defualt_font_check, False, False, 0)
        # Bottom Area
        action_box = Gtk.Box(spacing=10, orientation=Gtk.Orientation.HORIZONTAL)
        ok_button = Gtk.Button(label="Ok")
        ok_button.connect("clicked", lambda b: [ func(self.css_chooser_entry.get_text(), self.font_chooser_entry.get_text(), self.defualt_css_check.get_active(), self.defualt_font_check.get_active()), self.destroy() ])
        action_box.pack_end(ok_button, False, False, 0)
        vbox.pack_end(action_box, False, False, 0)
        self.connect("destroy", Gtk.main_quit)

    def _get_chooser_box(self, name:str, func):
        result = Gtk.Box(spacing=10)
        label = Gtk.Label(label="{}:".format(name))
        entry = Gtk.Entry()
        button = Gtk.Button(label="open")
        button.connect("clicked", func, entry)
        result.pack_start(label, False, False, 0)
        result.pack_start(entry, True, True, 0)
        result.pack_start(button, False, False, 0)
        return result, entry

    def _dialog_run(self, name, entry, filter):
        dialog = Gtk.FileChooserDialog(
            title=name, parent=None, action=Gtk.FileChooserAction.OPEN
        )
        dialog.set_transient_for(self)
        dialog.set_modal(True)
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN, Gtk.ResponseType.OK
        )
        dialog.add_filter(filter)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            file_path = dialog.get_filename()
            entry.set_text(file_path)
        dialog.destroy()

    def _on_css_file_select(self, button, entry):
        filter = Gtk.FileFilter()
        filter.set_name("(*.css)")
        filter.add_pattern("*.css")
        self._dialog_run(name="Choose CSS file", entry=entry, filter=filter)

    def _on_font_file_select(self, button, entry):
        filter = Gtk.FileFilter()
        filter.set_name("(*.ttf,*.otf,*.woff,*.woff2)")
        filter.add_pattern("*.ttf")
        filter.add_pattern("*.otf")
        filter.add_pattern("*.woff")
        filter.add_pattern("*.woff2")
        self._dialog_run(name="Choose Font file", entry=entry, filter=filter)

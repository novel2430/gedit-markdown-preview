from gi.repository import GObject, Gtk, Gedit, WebKit2, Tepl

import json
import hashlib

from .html import html

class MarkdownPanel(Gtk.Box):
    __gtype_name__ = "MarkdownPanel"

    def __init__(self, webview):
        # Webview
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.pack_start(webview, True, True, 0)
        # Toolbar
        toolbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5, halign=Gtk.Align.END)
        self.pack_start(toolbar, expand=False, fill=True, padding=2)
        # Dark mode Btn
        self.dark_mode_button = Gtk.Button(label="Mode 🌕")
        toolbar.pack_start(self.dark_mode_button, expand=False, fill=False, padding=0)
        # output pdf
        self.export_pdf_button = Gtk.Button(label="To PDF 📄")
        toolbar.pack_start(self.export_pdf_button, expand=False, fill=False, padding=0)

        self.show_all()


class MarkdownPanelUtils():
    def __init__(self):
        self.webview = WebKit2.WebView()
        setting = self.webview.get_settings()
        self.webview.get_settings().set_enable_developer_extras(True)
        self.initialize_html()
        self.panel = MarkdownPanel(self.webview)
        # Handler
        self._dark_mode_handler = None
        self._to_pdf_handler = None

    def add_dark_mode_button_func(self, func):
        self._dark_mode_handler = self.panel.dark_mode_button.connect("clicked", func)

    def add_to_pdf_button_func(self, func):
        self._to_pdf_handler = self.panel.export_pdf_button.connect("clicked", func)

    def disconnect_btns_signal(self):
        self.panel.dark_mode_button.disconnect(self._dark_mode_handler)
        self.panel.export_pdf_button.disconnect(self._to_pdf_handler)

    def initialize_html(self):
        self.webview.load_html(html, "file:///")

    def update_webview(self, content):
        if content:
            safe_markdown = json.dumps(content)
            script = f"""
                console.log("Update Markdown")
                window.updateContent({safe_markdown})
            """
            self.webview.evaluate_javascript(script, -1, None, None, None, None, None)

    def run_js(self, script):
        self.webview.evaluate_javascript(script, -1, None, None, None, None, None)



class MarkdownPreview(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = "MarkdownPreview"
    window = GObject.Property(type=Gedit.Window)

    def __init__(self):
        super().__init__()
        self._panel = None
        self._markdown_panel_util = None
        self._current_hash = None
        self._is_dark = False
        # Handler
        self._active_tab_handler = None
        self._cursor_move_handler_map = {}
        self._doc_loaded_map = {}

    def do_activate(self):
        self._add_side_panel()
        self._connect_signals()
        self._markdown_to_view()

    def do_deactivate(self):
        self._remove_side_panel()
        self._disconnect_signals()
        self._panel = None


    def _connect_signals(self):
        self._active_tab_handler = self.window.connect("active-tab-changed", self._on_tab_changed)
        self._add_doc_signals()
        self._add_btn_signal()


    def _disconnect_signals(self):
        # Deactive active tab handler
        if self._active_tab_handler:
            self.window.disconnect(self._active_tab_handler)
        # Deactive cursor move handler
        for doc in self._cursor_move_handler_map.keys():
            if self._cursor_move_handler_map.get(doc):
                doc.disconnect(self._cursor_move_handler_map.get(doc))
        # Deactive doc loaded signal
        for doc in self._doc_loaded_map.keys():
            if self._doc_loaded_map.get(doc):
                doc.disconnect(self._doc_loaded_map.get(doc))
        if self._markdown_panel_util :
            self._markdown_panel_util.disconnect_btns_signal()
            
    def _add_side_panel(self):
        side_panel = self.window.get_side_panel()
        self._markdown_panel_util = MarkdownPanelUtils()
        self._panel = Tepl.PanelItem.new(self._markdown_panel_util.panel, "MarkdownPreview", _("Markdown Preview"), None, 0)
        Tepl.Panel.add(side_panel, self._panel)

    def _remove_side_panel(self):
        if self._panel:
            Tepl.Panel.remove(self.window.get_side_panel(), self._panel)

    def _add_cursor_connet_to_doc(self, document):
        handler = document.connect('tepl-cursor-moved', self._on_cursor_change)
        self._cursor_move_handler_map.update({document: handler})

    def _add_doc_loaded_to_doc(self, document):
        handler = document.connect('loaded', self._on_doc_loaded)
        self._doc_loaded_map.update({document: handler})

    def _add_doc_signals(self):
        document = self.window.get_active_document()
        if document:
            if self._cursor_move_handler_map.get(document) == None:
                self._add_cursor_connet_to_doc(document)
                self._add_doc_loaded_to_doc(document)

    def _add_btn_signal(self):
        if self._markdown_panel_util:
            self._markdown_panel_util.add_dark_mode_button_func(self.toggle_dark_mode)
            self._markdown_panel_util.add_to_pdf_button_func(self.export_to_pdf)


    def _get_doc_type(self):
        document = self.window.get_active_document()
        if document:
            if document.get_content_type() == "text/markdown":
                return 1
            if document.get_content_type() == "text/html":
                return 2
        return 0

    def _get_current_text(self):
        document = self.window.get_active_document()
        if not document:
            return None
        start_iter = document.get_start_iter()
        end_iter = document.get_end_iter()
        return document.get_text(start_iter, end_iter, True)

    def _get_current_hash(self):
        doc_text = self._get_current_text()
        if doc_text:
            return hashlib.sha256(doc_text.encode()).hexdigest()
        return None

    def _sync_scroll(self, cursor):
        line_number = cursor.get_line()
        js_scroll = f"""
            window.synCursor({line_number})
        """
        self._markdown_panel_util.run_js(js_scroll)

    def toggle_dark_mode(self, button):
        js = """
            window.toggleDark()
        """
        self._markdown_panel_util.run_js(js)
        if self._is_dark:
            button.set_label("Mode 🌕")
            self._is_dark = False
        else:
            button.set_label("Mode 🌑")
            self._is_dark = True

    def export_to_pdf(self, button):
        webkit_print_op = WebKit2.PrintOperation.new(self._markdown_panel_util.webview)
        webkit_print_op.run_dialog()

    def _is_buffer_change(self):
        cur_cash = self._get_current_hash()
        if cur_cash == self._current_hash:
            return False
        else:
            self._current_hash = cur_cash
            return True

    def _on_cursor_change(self, buffer):
        current_type = self._get_doc_type()
        document = self.window.get_active_document()
        cursor = document.get_iter_at_mark(document.get_insert())
        if current_type == 0:
            return
        if current_type == 1:
            # Markdown
            if self._is_buffer_change():
                self._markdown_to_view()  
            self._sync_scroll(cursor)
        elif current_type == 2:
            # HTML
            pass

    def _on_tab_changed(self, *_):
        self._add_doc_signals()
        self._current_hash = self._get_current_hash()
        self._markdown_to_view()

    def _on_doc_loaded(self, doc):
        self._current_hash = self._get_current_hash()
        self._markdown_to_view()

    def _markdown_to_view(self):
        text = self._get_current_text()
        current_type = self._get_doc_type()
        if current_type == 1 and text:
            self._markdown_panel_util.update_webview(text)

# Plugin metadata required for Gedit to load the plugin
GObject.type_register(MarkdownPreview)


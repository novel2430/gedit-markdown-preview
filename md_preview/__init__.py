from gi.repository import GObject, Gtk, Gedit, WebKit2, Tepl

import json
import hashlib
import os

from .HtmlCreator import HtmlCreator
from .SettingsPage import SettingsPage
from .Configuration import Configuration

current_file_path = os.path.abspath(__file__)
current_directory = os.path.dirname(current_file_path)

light_mode_label = "Mode 🌕"
dark_mode_label = "Mode 🌑"

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
        self.dark_mode_button = Gtk.Button(label=light_mode_label)
        toolbar.pack_start(self.dark_mode_button, expand=False, fill=False, padding=0)
        # output pdf
        self.export_pdf_button = Gtk.Button(label="To PDF 📄")
        toolbar.pack_start(self.export_pdf_button, expand=False, fill=False, padding=0)
        # Settings
        self.settings_button = Gtk.Button(label="Settings ⚙️")
        toolbar.pack_start(self.settings_button, expand=False, fill=False, padding=0)

        self.show_all()


class MarkdownPanelUtils():
    def __init__(self):
        settings = WebKit2.Settings()
        settings.set_enable_developer_extras(True)  # Development
        self.webview = WebKit2.WebView()
        self.webview.set_settings(settings)
        self.panel = MarkdownPanel(self.webview)
        # Handler
        self._dark_mode_handler = None
        self._to_pdf_handler = None
        self._settings_handler = None
        self._webview_load_change_handler = None

    def _add_click_func_to_btn(self, btn, func):
        return btn.connect("clicked", func)
    
    def _remove_click_func_from_btn(self, btn, handler):
        btn.disconnect(handler)

    def add_dark_mode_button_func(self, func):
        self._dark_mode_handler = self._add_click_func_to_btn(self.panel.dark_mode_button, func)

    def add_to_pdf_button_func(self, func):
        self._to_pdf_handler =  self._add_click_func_to_btn(self.panel.export_pdf_button, func)

    def add_to_settings_button_func(self, func):
        self._settings_handler =  self._add_click_func_to_btn(self.panel.settings_button, func)

    def add_to_webview_load_change_func(self, func):
        self._webview_load_change_handler = self.webview.connect("load-changed", func)

    def disconnect_btns_signal(self):
        self._remove_click_func_from_btn(self.panel.dark_mode_button, self._dark_mode_handler)
        self._remove_click_func_from_btn(self.panel.export_pdf_button, self._to_pdf_handler)
        self._remove_click_func_from_btn(self.panel.settings_button, self._settings_handler)
        self.webview.disconnect(self._webview_load_change_handler)

    def initialize_html(self, html_page):
        self.webview.load_html(html_page, "file:///")

    def update_webview(self, content):
        if content:
            safe_markdown = json.dumps(content)
            script = f"""
                window.updateContent({safe_markdown})
            """
            self.webview.evaluate_javascript(script, -1, None, None, None, None, None)

    def run_js(self, script):
        self.webview.evaluate_javascript(script, -1, None, None, None, None, None)

    def init_dark_mode_label(self, name):
        self.panel.dark_mode_button.set_label(name)



class MarkdownPreview(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = "MarkdownPreview"
    window = GObject.Property(type=Gedit.Window)

    def __init__(self):
        super().__init__()
        self._panel = None
        self._markdown_panel_util = None
        self._current_hash = None
        self._is_dark = False
        self._is_startup = True
        self._configuration = Configuration()
        self._html_creator = HtmlCreator()
        # Handler
        self._active_tab_handler = None
        self._cursor_move_handler_map = {}
        self._doc_loaded_map = {}

    def do_activate(self):
        self._add_side_panel()
        self._connect_signals()
        self._init_webview_page()

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

    def _init_webview_page(self):
        font_path = None
        font_type = None
        css_path = None
        if self._configuration.load_state:
            if self._configuration.is_dark:
                self._markdown_panel_util.panel.dark_mode_button.set_label(dark_mode_label)
                self._is_dark = True
            if self._configuration.font_path and self._configuration.font_path != "default":
                font_path = json.dumps(self._configuration.font_path)
                font_type = json.dumps(self._get_font_format(self._configuration.font_path))
            if self._configuration.css_path and self._configuration.css_path != "default":
                css_path = json.dumps(self._configuration.css_path)

        html_page = self._html_creator.build_html(font_path=font_path, font_type=font_type, css_path=css_path, is_dark=self._is_dark)
        self._markdown_panel_util.initialize_html(html_page=html_page)

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
            self._markdown_panel_util.add_to_settings_button_func(self.open_settings_page)
            self._markdown_panel_util.add_to_webview_load_change_func(self.webview_load_chage)


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

    def _get_font_format(self, font_path):
        font_ext = os.path.splitext(font_path)[1].lower()
        if font_ext == '.ttf':
            return 'truetype'
        elif font_ext == '.otf':
            return 'opentype'
        elif font_ext == '.woff':
            return 'woff'
        elif font_ext == '.woff2':
            return 'woff2'
        else:
            return None

    def toggle_dark_mode(self, button):
        js_dark = """
            window.setDarkMode(true)
        """
        js_light = """
            window.setDarkMode(false)
        """
        if self._is_dark:
            self._markdown_panel_util.run_js(js_light)
            button.set_label(light_mode_label)
            self._is_dark = False
            self._configuration.is_dark = False
        else:
            self._markdown_panel_util.run_js(js_dark)
            button.set_label(dark_mode_label)
            self._is_dark = True
            self._configuration.is_dark = True
        self._configuration.save_to_disk()

    def export_to_pdf(self, button):
        webkit_print_op = WebKit2.PrintOperation.new(self._markdown_panel_util.webview)
        webkit_print_op.run_dialog()

    def open_settings_page(self, button):
        settingPage = SettingsPage(parent=self.window, func=self.apply_setting)
        settingPage.show_all()

    def webview_load_chage(self, webview, load_event):
        if load_event == WebKit2.LoadEvent.FINISHED and self._is_startup:
            self._markdown_to_view()
            self._is_startup = False
        
    def apply_setting(self, css_path, font_path, css_default, font_default):
        if css_default == True:
            js = f"""
                window.setCSSDefault()
            """
            self._markdown_panel_util.run_js(js)
            self._configuration.css_path = "default"

        if font_default == True:
            js = f"""
                window.setFontDefault()
            """
            self._markdown_panel_util.run_js(js)
            self._configuration.font_path = "default"

        if os.path.exists(css_path) and css_default == False:
            path = json.dumps(css_path)
            js = f"""
                window.updateCSS({path})
            """
            self._markdown_panel_util.run_js(js)
            self._configuration.css_path = css_path

        if os.path.exists(font_path) and font_default == False:
            path = json.dumps(font_path)
            font_type = json.dumps(self._get_font_format(font_path))
            js = f"""
                window.updateFont({path}, {font_type})
            """
            self._markdown_panel_util.run_js(js)
            self._configuration.font_path = font_path

        self._configuration.save_to_disk()

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


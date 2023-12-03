import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class MyWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Hypr Settings")

        self.set_border_width(10)
        self.set_default_size(800, 600)

        self.box = Gtk.Paned()
        self.add(self.box)

        self.scroll = Gtk.ScrolledWindow()
        self.scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.box.pack1(self.scroll, True, True)

        self.liststore = Gtk.ListStore(str)
        self.treeview = Gtk.TreeView(model=self.liststore)
        self.scroll.add(self.treeview)

        self.cell = Gtk.CellRendererText()
        self.column = Gtk.TreeViewColumn("", self.cell, text=0,)
        self.treeview.append_column(self.column)
        self.treeview.props.headers_visible = False
        self.treeview.set_activate_on_single_click(True)

        for filename in os.listdir(os.path.expanduser("~/.config/hypr")):
            self.liststore.append([filename])

        self.treeview.connect("row-activated", self.on_row_activated)

        self.editor = Gtk.TextView()
        self.editor.set_editable(True)
        self.editor.set_cursor_visible(True)

        self.buffer = self.editor.get_buffer()

        self.scrolledwindow = Gtk.ScrolledWindow()
        self.scrolledwindow.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.box.pack2(self.scrolledwindow, True, True)

        self.box.set_position(200)
        self.box.set_wide_handle(True)

        self.scrolledwindow.add(self.editor)

        self.save_button = Gtk.Button(label="Save")
        self.save_button.connect("clicked", self.on_save_button_clicked)

        header_bar = Gtk.HeaderBar()
        header_bar.set_show_close_button(True)
        header_bar.props.title = "Hypr Files"
        header_bar.pack_end(self.save_button)

        self.set_titlebar(header_bar)


        tree_context = self.treeview.get_style_context()
        tree_context.remove_class("view")
        tree_context.add_class("background")
        
        
    def on_row_activated(self, treeview, path, column):
        model = treeview.get_model()
        iter = model.get_iter(path)
        filename = model.get_value(iter, 0)
        filepath = os.path.expanduser("~/.config/hypr/" + filename)

        with open(filepath, "r") as f:
            text = f.read()
            self.buffer.set_text(text)

    def on_save_button_clicked(self, widget):
        editor_text = self.buffer.get_text(self.buffer.get_start_iter(), self.buffer.get_end_iter(), True)
        selected_row = self.treeview.get_selection().get_selected()
        if selected_row is not None:
            model, iter = selected_row
            filename = model.get_value(iter, 0)
            filepath = os.path.expanduser("~/.config/hypr/" + filename)
            with open(filepath, "w") as f:
                f.write(editor_text)

win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()

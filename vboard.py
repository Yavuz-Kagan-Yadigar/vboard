#!/usr/bin/env python3
import gi
from evdev import uinput, ecodes
import time
import os
import configparser
import subprocess
os.environ['GDK_BACKEND'] = 'x11'
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk, GLib

key_mapping = {
    ecodes.KEY_ESC: "Esc",
    ecodes.KEY_1: "1",
    ecodes.KEY_2: "2",
    ecodes.KEY_3: "3",
    ecodes.KEY_4: "4",
    ecodes.KEY_5: "5",
    ecodes.KEY_6: "6",
    ecodes.KEY_7: "7",
    ecodes.KEY_8: "8",
    ecodes.KEY_9: "9",
    ecodes.KEY_0: "0",
    ecodes.KEY_MINUS: "*",
    ecodes.KEY_EQUAL: "-",
    ecodes.KEY_BACKSPACE: "Backspace",
    ecodes.KEY_TAB: "Tab",
    ecodes.KEY_Q: "Q",
    ecodes.KEY_W: "W",
    ecodes.KEY_E: "E",
    ecodes.KEY_R: "R",
    ecodes.KEY_T: "T",
    ecodes.KEY_Y: "Y",
    ecodes.KEY_U: "U",
    ecodes.KEY_I: "I",
    ecodes.KEY_O: "O",
    ecodes.KEY_P: "P",
    ecodes.KEY_LEFTBRACE: "Ğ",
    ecodes.KEY_RIGHTBRACE: "Ü",
    ecodes.KEY_ENTER: "Enter",
    ecodes.KEY_LEFTCTRL: "Ctrl_L",
    ecodes.KEY_A: "A",
    ecodes.KEY_S: "S",
    ecodes.KEY_D: "D",
    ecodes.KEY_F: "F",
    ecodes.KEY_G: "G",
    ecodes.KEY_H: "H",
    ecodes.KEY_J: "J",
    ecodes.KEY_K: "K",
    ecodes.KEY_L: "L",
    ecodes.KEY_SEMICOLON: "Ş",
    ecodes.KEY_APOSTROPHE: "İ",
    ecodes.KEY_GRAVE: '"',
    ecodes.KEY_LEFTSHIFT: "Shift_L",
    ecodes.KEY_BACKSLASH: ",",
    ecodes.KEY_Z: "Z",
    ecodes.KEY_X: "X",
    ecodes.KEY_C: "C",
    ecodes.KEY_V: "V",
    ecodes.KEY_B: "B",
    ecodes.KEY_N: "N",
    ecodes.KEY_M: "M",
    ecodes.KEY_COMMA: "Ö",
    ecodes.KEY_DOT: "Ç",
    ecodes.KEY_SLASH: ".",
    ecodes.KEY_RIGHTSHIFT: "Shift_R",
    ecodes.KEY_KPENTER: "Enter",
    ecodes.KEY_LEFTALT: "Alt_L",
    ecodes.KEY_RIGHTALT: "Alt_R",
    ecodes.KEY_SPACE: "Space",
    ecodes.KEY_CAPSLOCK: "CapsLock",
    ecodes.KEY_F1: "F1",
    ecodes.KEY_F2: "F2",
    ecodes.KEY_F3: "F3",
    ecodes.KEY_F4: "F4",
    ecodes.KEY_F5: "F5",
    ecodes.KEY_F6: "F6",
    ecodes.KEY_F7: "F7",
    ecodes.KEY_F8: "F8",
    ecodes.KEY_F9: "F9",
    ecodes.KEY_F10: "F10",
    ecodes.KEY_F11: "F11",
    ecodes.KEY_F12: "F12",
    ecodes.KEY_SCROLLLOCK: "ScrollLock",
    ecodes.KEY_PAUSE: "Pause",
    ecodes.KEY_INSERT: "Insert",
    ecodes.KEY_HOME: "Home",
    ecodes.KEY_PAGEUP: "PageUp",
    ecodes.KEY_DELETE: "Delete",
    ecodes.KEY_END: "End",
    ecodes.KEY_PAGEDOWN: "PageDown",
    ecodes.KEY_RIGHT: "→",
    ecodes.KEY_LEFT: "←",
    ecodes.KEY_DOWN: "↓",
    ecodes.KEY_UP: "↑",
    ecodes.KEY_NUMLOCK: "NumLock",
    ecodes.KEY_RIGHTCTRL: "Ctrl_R",
    ecodes.KEY_LEFTMETA: "Super_L",
    ecodes.KEY_RIGHTMETA: "Super_R",
    ecodes.KEY_102ND: "<",
}

class VirtualKeyboard(Gtk.Window):
    def __init__(self):
        super().__init__(title="Virtual Keyboard", name="toplevel")
        self.set_border_width(0)
        self.set_resizable(True)
        self.set_keep_above(True)
        self.set_modal(False)
        self.set_focus_on_map(False)
        self.set_can_focus(False)
        self.set_accept_focus(False)
        self.width = 0
        self.height = 0
        self.CONFIG_DIR = os.path.expanduser("~/.config/vboard")
        self.CONFIG_FILE = os.path.join(self.CONFIG_DIR, "settings.conf")
        self.config = configparser.ConfigParser()
        self.bg_color = "0, 0, 0"
        self.opacity = "0.90"
        self.text_color = "white"
        self.read_settings()
        self.modifiers = {
            ecodes.KEY_LEFTSHIFT: False,
            ecodes.KEY_RIGHTSHIFT: False,
            ecodes.KEY_LEFTCTRL: False,
            ecodes.KEY_RIGHTCTRL: False,
            ecodes.KEY_LEFTALT: False,
            ecodes.KEY_RIGHTALT: False,
            ecodes.KEY_LEFTMETA: False,
            ecodes.KEY_RIGHTMETA: False,
            ecodes.KEY_CAPSLOCK: False
        }
        self.turkish_keys = {
            "ğ_lower": (ecodes.KEY_LEFTBRACE, 'lower'),
            "ğ_upper": (ecodes.KEY_LEFTBRACE, 'upper'),
            "ü_lower": (ecodes.KEY_RIGHTBRACE, 'lower'),
            "ü_upper": (ecodes.KEY_RIGHTBRACE, 'upper'),
            "ş_lower": (ecodes.KEY_SEMICOLON, 'lower'),
            "ş_upper": (ecodes.KEY_SEMICOLON, 'upper'),
            "i_lower": (ecodes.KEY_APOSTROPHE, 'lower'),
            "i_upper": (ecodes.KEY_APOSTROPHE, 'upper'),
            "ö_lower": (ecodes.KEY_COMMA, 'lower'),
            "ö_upper": (ecodes.KEY_COMMA, 'upper'),
            "ç_lower": (ecodes.KEY_DOT, 'lower'),
            "ç_upper": (ecodes.KEY_DOT, 'upper')
        }
        self.capslock_state = False
        self.capslock_button = None
        self.colors = [
            ("Black", "0,0,0"),
            ("Red", "255,0,0"),
            ("Pink", "255,105,183"),
            ("White", "255,255,255"),
            ("Green", "0,255,0"),
            ("Blue", "0,0,110"),
            ("Gray", "128,128,128"),
            ("Dark Gray", "64,64,64"),
            ("Orange", "255,165,0"),
            ("Yellow", "255,255,0"),
            ("Purple", "128,0,128"),
            ("Cyan", "0,255,255"),
            ("Teal", "0,128,128"),
            ("Brown", "139,69,19"),
            ("Gold", "255,215,0"),
            ("Silver", "192,192,192"),
            ("Turquoise", "64,224,208"),
            ("Magenta", "255,0,255"),
            ("Olive", "128,128,0"),
            ("Maroon", "128,0,0"),
            ("Indigo", "75,0,130"),
            ("Beige", "245,245,220"),
            ("Lavender", "230,230,250")
        ]
        if self.width != 0:
            self.set_default_size(self.width, self.height)
        self.header = Gtk.HeaderBar()
        self.header.set_show_close_button(False)
        self.buttons = []
        self.modifier_buttons = {}
        self.row_buttons = []
        self.color_combobox = Gtk.ComboBoxText()
        self.set_titlebar(self.header)
        self.set_default_icon_name("preferences-desktop-keyboard")
        self.header.set_decoration_layout(":")
        self.create_settings()
        grid = Gtk.Grid()
        grid.set_row_homogeneous(True)
        grid.set_column_homogeneous(True)
        grid.set_margin_start(3)
        grid.set_margin_end(3)
        grid.set_name("grid")
        self.add(grid)
        self.apply_css()
        self.device = uinput.UInput({ecodes.EV_KEY: list(key_mapping.keys())})
        
        # End ve Home tuşlarını değiştir: Home, End olarak sırala
        rows = [
            ["Esc", '"', "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "*", "-", "Backspace", "Delete"],
            ["Tab", "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "ğ_lower", "ü_upper", ",", "Home", "End"],  # Home, End olarak değiştirildi
            ["CapsLock", "A", "S", "D", "F", "G", "H", "J", "K", "L", "ş_lower", "i_upper", "Enter"],
            ["Shift_L", "Z", "X", "C", "V", "B", "N", "M", "ö_lower", "ç_upper", ".", "Shift_R", "↑", "<>"],
            ["Ctrl_L", "Super_L", "Alt_L", "Space", "Alt_R", "Super_R", "Ctrl_R", "@", "←", "↓", "→"]
        ]
        for row_index, keys in enumerate(rows):
            self.create_row(grid, row_index, keys)
        self.update_label(False)
        
        # HeaderBar için sürükleme desteği
        self.dragging = False
        self.drag_start_x = 0
        self.drag_start_y = 0
        
        # HeaderBar için olayları bağla
        self.header.connect("button-press-event", self.on_header_button_press)
        self.header.connect("button-release-event", self.on_header_button_release)
        self.header.connect("motion-notify-event", self.on_header_motion)
        
        # Tüm olay türlerini etkinleştir
        self.header.set_events(
            self.header.get_events() |
            Gdk.EventMask.BUTTON_PRESS_MASK |
            Gdk.EventMask.BUTTON_RELEASE_MASK |
            Gdk.EventMask.POINTER_MOTION_MASK |
            Gdk.EventMask.TOUCH_MASK
        )

    def on_header_button_press(self, widget, event):
        """HeaderBar'a tıklandığında sürüklemeyi başlat"""
        if event.type == Gdk.EventType.BUTTON_PRESS or event.type == Gdk.EventType.TOUCH_BEGIN:
            self.dragging = True
            window_x, window_y = self.get_position()
            self.drag_start_x = event.x_root - window_x
            self.drag_start_y = event.y_root - window_y
            return True
        return False

    def on_header_button_release(self, widget, event):
        """HeaderBar'dan tıklama bırakıldığında sürüklemeyi durdur"""
        if event.type == Gdk.EventType.BUTTON_RELEASE or event.type == Gdk.EventType.TOUCH_END:
            self.dragging = False
            return True
        return False

    def on_header_motion(self, widget, event):
        """HeaderBar'da hareket edildiğinde pencereyi sürükle"""
        if self.dragging:
            new_x = event.x_root - self.drag_start_x
            new_y = event.y_root - self.drag_start_y
            self.move(new_x, new_y)
            return True
        return False

    def create_settings(self):
        # Diğer butonlar (önce bunları ekleyelim)
        self.create_button("☰", self.change_visibility, callbacks=1)
        self.create_button("+", self.change_opacity, True, 2)
        self.create_button("-", self.change_opacity, False, 2)
        self.create_button(f"{self.opacity}")
        self.capslock_button = self.create_button("CAPS", self.toggle_capslock, callbacks=1)
        self.modifier_buttons[ecodes.KEY_CAPSLOCK] = self.capslock_button
        self.color_combobox.append_text("Change Background")
        self.color_combobox.set_active(0)
        self.color_combobox.connect("changed", self.change_color)
        self.color_combobox.set_name("combobox")
        self.header.add(self.color_combobox)
        for label, color in self.colors:
            self.color_combobox.append_text(label)
        
        # Minimize butonunu en sağa ekle
        minimize_btn = Gtk.Button(label="−")
        minimize_btn.set_name("headbar-button")
        minimize_btn.connect("clicked", self.minimize)
        self.header.pack_end(minimize_btn)
        self.buttons.append(minimize_btn)

    def minimize(self, widget):
        """Pencereyi simge durumuna küçült"""
        self.iconify()

    def on_resize(self, widget, event):
        self.width, self.height = self.get_size()

    def create_button(self, label_="", callback=None, callback2=None, callbacks=0):
        button = Gtk.Button(label=label_)
        button.set_name("headbar-button")
        if callbacks == 1:
            button.connect("clicked", callback)
        elif callbacks == 2:
            button.connect("clicked", callback, callback2)
        if label_ == self.opacity:
            self.opacity_btn = button
            self.opacity_btn.set_tooltip_text("opacity")
        self.header.add(button)
        self.buttons.append(button)
        return button

    def change_visibility(self, widget=None):
        for button in self.buttons:
            if button.get_label() not in ["−", "☰", "CAPS"]:
                button.set_visible(not button.get_visible())
        self.color_combobox.set_visible(not self.color_combobox.get_visible())

    def change_color(self, widget):
        label = self.color_combobox.get_active_text()
        for label_, color_ in self.colors:
            if label_ == label:
                self.bg_color = color_
                if self.bg_color in {"255,255,255", "0,255,0", "255,255,0", "245,245,220", "230,230,250", "255,215,0"}:
                    self.text_color = "#1C1C1C"
                else:
                    self.text_color = "white"
                self.apply_css()

    def change_opacity(self, widget, boolean):
        if boolean:
            self.opacity = str(round(min(1.0, float(self.opacity) + 0.01), 2))
        else:
            self.opacity = str(round(max(0.0, float(self.opacity) - 0.01), 2))
        self.opacity_btn.set_label(f"{self.opacity}")
        self.apply_css()

    def apply_css(self):
        provider = Gtk.CssProvider()
        css = f"""
        headerbar {{
            background-color: rgba({self.bg_color}, {self.opacity});
            border: 0px;
            box-shadow: none;
            min-height: 24px;
            padding: 1px;
        }}
        headerbar button {{
            min-width: 24px;
            min-height: 20px;
            padding: 1px 4px;
            border: 0px;
            margin: 0px 1px;
        }}
        headerbar .titlebutton {{
            min-width: 24px;
            min-height: 20px;
            padding: 1px;
        }}
        headerbar button label {{
            color: {self.text_color};
            font-size: 10px;
        }}
        #headbar-button, #combobox button.combo {{
            background-image: none;
        }}
        #toplevel {{
            background-color: rgba({self.bg_color}, {self.opacity});
        }}
        #grid button label {{
            color: {self.text_color};
        }}
        #grid button {{
            border: none;
            background-image: none;
            padding: 0px;
            margin: 0px;
        }}
        button {{
            background-color: transparent;
            color: {self.text_color};
        }}
        #grid button:hover {{
            border: 1px solid #00CACB;
        }}
        #grid button.pressed, #grid button.pressed:hover {{
            border: 1px solid {self.text_color};
        }}
        tooltip {{
            color: white;
            padding: 5px;
        }}
        #combobox button.combo {{
            color: {self.text_color};
            padding: 1px 4px;
            min-height: 20px;
            font-size: 10px;
        }}
        """
        try:
            provider.load_from_data(css.encode("utf-8"))
        except GLib.GError as e:
            print(f"CSS Error: {e.message}")
        Gtk.StyleContext.add_provider_for_screen(
            self.get_screen(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_USER
        )

    def create_row(self, grid, row_index, keys):
        col = 0
        for key_label in keys:
            if key_label in self.turkish_keys:
                key_event, case = self.turkish_keys[key_label]
                display_label = "Ğ" if "ğ" in key_label else "Ü" if "ü" in key_label else "Ş" if "ş" in key_label else "İ" if "i" in key_label else "Ö" if "ö" in key_label else "Ç"
                if case == 'lower':
                    display_label = display_label.lower()
            else:
                key_event = next((key for key, label in key_mapping.items() if label == key_label), None)
                display_label = key_label

            if key_event or key_label in ["<>", "@"]:
                if key_label == "Tab":
                    display_label = "Tab"
                elif key_label == "CapsLock":
                    display_label = "Caps"
                elif key_label == "Shift_L":
                    display_label = "Shift"
                elif key_label == "Shift_R":
                    display_label = "Shift"
                elif key_label == "Ctrl_L":
                    display_label = "Ctrl"
                elif key_label == "Ctrl_R":
                    display_label = "Ctrl"
                elif key_label == "Alt_L":
                    display_label = "Alt"
                elif key_label == "Alt_R":
                    display_label = "Alt"
                elif key_label == "Super_L":
                    display_label = "Super"
                elif key_label == "Super_R":
                    display_label = "Super"
                elif key_label == "Backspace":
                    display_label = "⌫"
                elif key_label == "Enter":
                    display_label = "⏎"
                elif key_label == "Space":
                    display_label = "Space"
                elif key_label == "Esc":
                    display_label = "Esc"
                elif key_label == "Home":
                    display_label = "Home"
                elif key_label == "End":
                    display_label = "End"
                elif key_label == "Delete":
                    display_label = "Del"
                elif key_label == "<>":
                    display_label = "<"
                    key_event = ecodes.KEY_102ND
                elif key_label == "@":
                    display_label = "@"
                    key_event = None  # @ işareti için özel işlem yapacağız

                button = Gtk.Button(label=display_label)
                button.connect("pressed", self.on_button_press, key_event, key_label)
                button.connect("released", self.on_button_release)
                button.connect("leave-notify-event", self.on_button_release)
                self.row_buttons.append(button)
                if key_event in self.modifiers:
                    self.modifier_buttons[key_event] = button

                # Tuş genişliklerini ayarla
                if key_label == "Space":
                    width = 12
                elif key_label == "CapsLock":
                    width = 3
                elif key_label == "Shift_R":
                    width = 4
                elif key_label == "Shift_L":
                    width = 4
                elif key_label == "Backspace":
                    width = 2  # 2br yapıldı
                elif key_label == "Delete":
                    width = 2
                elif key_label == '"':
                    width = 2
                elif key_label == ",":
                    width = 2
                elif key_label == ".":
                    width = 2
                elif key_label == "Enter":
                    width = 7  # 2br büyütüldü (5'ten 7'ye)
                elif key_label == "Tab":
                    width = 2
                elif key_label == "Esc":
                    width = 2
                elif key_label in ["Ctrl_L", "Ctrl_R", "Super_L", "Super_R", "Alt_L", "Alt_R"]:
                    width = 2
                elif key_label in ["←", "↓", "→"]:
                    width = 2
                elif key_label == "↑":
                    width = 2
                elif key_label == "Home":
                    width = 2
                elif key_label == "End":
                    width = 2
                elif key_label in ["<>", "@"]:
                    width = 2
                else:
                    width = 2
                grid.attach(button, col, row_index, width, 1)
                col += width

    def update_label(self, show_symbols=False):
        show_upper = show_symbols or self.capslock_state
        button_positions = [
            (1, '" é'),      # 1: "
            (2, '1 !'),      # 2: 1
            (3, '2 \''),     # 3: 2
            (4, '3 ^'),      # 4: 3
            (5, '4 +'),      # 5: 4
            (6, '5 %'),      # 6: 5
            (7, '6 &'),      # 7: 6
            (8, '7 /'),      # 8: 7
            (9, '8 ('),      # 9: 8
            (10, '9 )'),     # 10: 9
            (11, '0 ='),     # 11: 0
            (12, '* ?'),     # 12: *
            (13, '- _'),     # 13: -
            (22, 'y Y'),     # 22: Y (ikinci satırın 6. tuşu)
            (23, 'u U'),     # 23: U (ikinci satırın 7. tuşu)
            (24, 'ı I'),     # 24: I (ikinci satırın 8. tuşu)
            (27, 'ğ Ğ'),     # 27: ğ (ikinci satırın 11. tuşu)
            (28, 'ü Ü'),     # 28: ü (ikinci satırın 12. tuşu)
            (29, ', ;'),     # 29: , (ikinci satırın 13. tuşu)
            (33, 'a A'),     # 33: A (üçüncü satırın 1. tuşu)
            (42, 'ş Ş'),     # 42: ş (üçüncü satırın 10. tuşu)
            (43, 'i İ'),     # 43: İ (üçüncü satırın 11. tuşu)
            (53, 'ö Ö'),     # 53: ö (dördüncü satırın 8. tuşu)
            (54, 'ç Ç'),     # 54: ç (dördüncü satırın 9. tuşu)
            (55, '. :'),     # 55: . (dördüncü satırın 10. tuşu)
            (58, '< >'),     # 58: < (dördüncü satırın 13. tuşu)
        ]
        for i, button in enumerate(self.row_buttons):
            current_label = button.get_label()
            special_labels = ["Tab", "Caps", "Shift", "Ctrl", "Alt", "Super", "Space", "⌫", "⏎", "Esc", "←", "↓", "→", "↑", "Home", "End", "Del", "@"]
            if current_label in special_labels:
                continue
            found = False
            for pos, label in button_positions:
                if pos == i:
                    label_parts = label.split()
                    if len(label_parts) == 2:
                        if show_upper:
                            # Özel durum: ı/I ve i/İ
                            if label_parts[0] == 'ı':
                                button.set_label(label_parts[1])
                            elif label_parts[0] == 'i':
                                button.set_label(label_parts[1])
                            else:
                                button.set_label(label_parts[1])
                        else:
                            # Özel durum: ı/I ve i/İ
                            if label_parts[0] == 'ı':
                                button.set_label('ı')
                            elif label_parts[0] == 'i':
                                button.set_label('i')
                            else:
                                button.set_label(label_parts[0])
                    found = True
                    break
            
            if not found and current_label.isalpha() and len(current_label) == 1:
                if show_upper:
                    # Özel durum: I harfi büyük harf, i değil
                    if current_label.lower() == 'i':
                        button.set_label('I')
                    else:
                        button.set_label(current_label.upper())
                else:
                    # Özel durum: ı küçük harf, i değil
                    if current_label.lower() == 'i':
                        button.set_label('ı')
                    else:
                        button.set_label(current_label.lower())

    def update_modifier(self, key_event, value):
        self.modifiers[key_event] = value
        if key_event in self.modifier_buttons:
            button = self.modifier_buttons[key_event]
            style_context = button.get_style_context()
            if value:
                style_context.add_class('pressed')
            else:
                style_context.remove_class('pressed')

    def toggle_capslock(self, widget=None):
        self.capslock_state = not self.capslock_state
        if self.capslock_state:
            self.capslock_button.set_label("Capslock ON")
            self.capslock_button.get_style_context().add_class('pressed')
        else:
            self.capslock_button.set_label("CAPS")
            self.capslock_button.get_style_context().remove_class('pressed')
        self.update_label(self.capslock_state)
        return True

    def on_button_press(self, widget, key_event, key_label):
        if key_event == ecodes.KEY_CAPSLOCK:
            self.toggle_capslock()
            return
        if key_event in self.modifiers:
            self.update_modifier(key_event, not self.modifiers[key_event])
            if self.modifiers[ecodes.KEY_LEFTSHIFT] and self.modifiers[ecodes.KEY_RIGHTSHIFT]:
                self.update_modifier(ecodes.KEY_LEFTSHIFT, False)
                self.update_modifier(ecodes.KEY_RIGHTSHIFT, False)
            shift_active = self.modifiers[ecodes.KEY_LEFTSHIFT] or self.modifiers[ecodes.KEY_RIGHTSHIFT]
            self.update_label(shift_active)
            return
        
        # @ işareti için özel işlem
        if key_label == "@":
            self.emit_at_key()
            self.delay_source = GLib.timeout_add(400, self.start_repeat_at)
            return
            
        self.emit_key(key_event, key_label)
        self.delay_source = GLib.timeout_add(400, self.start_repeat, key_event, key_label)

    def on_button_release(self, widget, *args):
        if hasattr(self, "delay_source"):
            GLib.source_remove(self.delay_source)
            del self.delay_source
        if hasattr(self, "repeat_source"):
            GLib.source_remove(self.repeat_source)
            del self.repeat_source

    def start_repeat(self, key_event, key_label):
        self.repeat_source = GLib.timeout_add(100, self.repeat_key, key_event, key_label)
        return False
    
    def start_repeat_at(self):
        self.repeat_source = GLib.timeout_add(100, self.repeat_at)
        return False
    
    def repeat_at(self):
        self.emit_at_key()
        return True

    def repeat_key(self, key_event, key_label):
        self.emit_key(key_event, key_label)
        return True

    def emit_at_key(self):
        # @ işareti için AltGr+Q (Türkçe klavye)
        self.device.write(ecodes.EV_KEY, ecodes.KEY_RIGHTALT, 1)
        self.device.write(ecodes.EV_KEY, ecodes.KEY_Q, 1)
        self.device.syn()
        time.sleep(0.01)
        self.device.write(ecodes.EV_KEY, ecodes.KEY_Q, 0)
        self.device.write(ecodes.EV_KEY, ecodes.KEY_RIGHTALT, 0)
        self.device.syn()
    
    def emit_key(self, key_event, key_label):
        caps_lock_active = self.capslock_state
        shift_active = self.modifiers[ecodes.KEY_LEFTSHIFT] or self.modifiers[ecodes.KEY_RIGHTSHIFT]
        caps_lock_keys = [
            ecodes.KEY_A, ecodes.KEY_B, ecodes.KEY_C, ecodes.KEY_D, ecodes.KEY_E,
            ecodes.KEY_F, ecodes.KEY_G, ecodes.KEY_H, ecodes.KEY_I, ecodes.KEY_J,
            ecodes.KEY_K, ecodes.KEY_L, ecodes.KEY_M, ecodes.KEY_N, ecodes.KEY_O,
            ecodes.KEY_P, ecodes.KEY_Q, ecodes.KEY_R, ecodes.KEY_S, ecodes.KEY_T,
            ecodes.KEY_U, ecodes.KEY_V, ecodes.KEY_W, ecodes.KEY_X, ecodes.KEY_Y,
            ecodes.KEY_Z,
            ecodes.KEY_LEFTBRACE, ecodes.KEY_RIGHTBRACE, ecodes.KEY_SEMICOLON,
            ecodes.KEY_APOSTROPHE, ecodes.KEY_COMMA, ecodes.KEY_DOT
        ]
        for mod_key, active in self.modifiers.items():
            if active and mod_key not in [ecodes.KEY_LEFTSHIFT, ecodes.KEY_RIGHTSHIFT, ecodes.KEY_CAPSLOCK]:
                self.device.write(ecodes.EV_KEY, mod_key, 1)
                self.device.syn()
        
        if shift_active:
            if self.modifiers[ecodes.KEY_LEFTSHIFT]:
                self.device.write(ecodes.EV_KEY, ecodes.KEY_LEFTSHIFT, 1)
                self.device.syn()
            elif self.modifiers[ecodes.KEY_RIGHTSHIFT]:
                self.device.write(ecodes.EV_KEY, ecodes.KEY_RIGHTSHIFT, 1)
                self.device.syn()
        elif caps_lock_active and key_event in caps_lock_keys:
            self.device.write(ecodes.EV_KEY, ecodes.KEY_LEFTSHIFT, 1)
            self.device.syn()
        
        self.device.write(ecodes.EV_KEY, key_event, 1)
        self.device.syn()
        time.sleep(0.01)
        self.device.write(ecodes.EV_KEY, key_event, 0)
        self.device.syn()
        
        if shift_active:
            if self.modifiers[ecodes.KEY_LEFTSHIFT]:
                self.device.write(ecodes.EV_KEY, ecodes.KEY_LEFTSHIFT, 0)
                self.device.syn()
            elif self.modifiers[ecodes.KEY_RIGHTSHIFT]:
                self.device.write(ecodes.EV_KEY, ecodes.KEY_RIGHTSHIFT, 0)
                self.device.syn()
        elif caps_lock_active and key_event in caps_lock_keys:
            self.device.write(ecodes.EV_KEY, ecodes.KEY_LEFTSHIFT, 0)
            self.device.syn()
        
        for mod_key, active in self.modifiers.items():
            if active and mod_key not in [ecodes.KEY_LEFTSHIFT, ecodes.KEY_RIGHTSHIFT, ecodes.KEY_CAPSLOCK]:
                self.device.write(ecodes.EV_KEY, mod_key, 0)
                self.device.syn()
                self.update_modifier(mod_key, False)
        
        if shift_active:
            self.update_modifier(ecodes.KEY_LEFTSHIFT, False)
            self.update_modifier(ecodes.KEY_RIGHTSHIFT, False)
            self.update_label(False)

    def read_settings(self):
        try:
            os.makedirs(self.CONFIG_DIR, exist_ok=True)
        except PermissionError:
            print("Warning: No permission to create the config directory. Proceeding without it.")
        try:
            if os.path.exists(self.CONFIG_FILE):
                self.config.read(self.CONFIG_FILE)
                self.bg_color = self.config.get("DEFAULT", "bg_color")
                self.opacity = self.config.get("DEFAULT", "opacity")
                self.text_color = self.config.get("DEFAULT", "text_color", fallback="white")
                self.width = self.config.getint("DEFAULT", "width", fallback=0)
                self.height = self.config.getint("DEFAULT", "height", fallback=0)
                print(f"rgba: {self.bg_color}, {self.opacity}")
        except configparser.Error as e:
            print(f"Warning: Could not read config file ({e}). Using default values.")

    def save_settings(self):
        self.config["DEFAULT"] = {
            "bg_color": self.bg_color,
            "opacity": self.opacity,
            "text_color": self.text_color,
            "width": self.width,
            "height": self.height
        }
        try:
            with open(self.CONFIG_FILE, "w") as configfile:
                self.config.write(configfile)
        except (configparser.Error, IOError) as e:
            print(f"Warning: Could not write to config file ({e}). Changes will not be saved.")

if __name__ == "__main__":
    win = VirtualKeyboard()
    win.connect("destroy", Gtk.main_quit)
    win.connect("destroy", lambda w: win.save_settings())
    win.show_all()
    win.connect("configure-event", win.on_resize)
    win.change_visibility()
    Gtk.main()

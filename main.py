# FOODIE GO — Python + Kivy
# Created by Revan
# Demo aplikasi pemesanan makanan. Checkout belum terhubung ke restoran/pembayaran nyata.

from datetime import datetime
from pathlib import Path
import re

from kivy.app import App
from kivy.metrics import dp, sp
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.core.clipboard import Clipboard

# Warna aplikasi
ORANGE = get_color_from_hex("#F97316")
DARK_ORANGE = get_color_from_hex("#C2410C")
CREAM = get_color_from_hex("#FFF7ED")
PALE_ORANGE = get_color_from_hex("#FFEDD5")
WHITE = get_color_from_hex("#FFFFFF")
INK = get_color_from_hex("#1F2937")
MUTED = get_color_from_hex("#6B7280")
GREEN = get_color_from_hex("#15803D")
LIGHT_GREEN = get_color_from_hex("#DCFCE7")
RED = get_color_from_hex("#B91C1C")

FOODS = [
    {"id": 1, "name": "Nasi Goreng", "cat": "Makanan berat", "price": 15000, "emoji": "🍛", "desc": "Nasi goreng gurih dengan bumbu spesial.", "tag": "Terlaris"},
    {"id": 2, "name": "Ayam Geprek", "cat": "Makanan berat", "price": 18000, "emoji": "🍗", "desc": "Ayam crispy dengan sambal pedas mantap.", "tag": "Pedas"},
    {"id": 3, "name": "Burger Spesial", "cat": "Fast food", "price": 22000, "emoji": "🍔", "desc": "Burger juicy dengan sayur dan saus spesial.", "tag": "Favorit"},
    {"id": 4, "name": "Mie Goreng", "cat": "Makanan berat", "price": 14000, "emoji": "🍜", "desc": "Mie goreng gurih dengan topping pilihan.", "tag": "Hemat"},
    {"id": 5, "name": "Kentang Goreng", "cat": "Fast food", "price": 12000, "emoji": "🍟", "desc": "Kentang renyah untuk teman ngemil.", "tag": "Camilan"},
    {"id": 6, "name": "Pizza Mini", "cat": "Fast food", "price": 25000, "emoji": "🍕", "desc": "Pizza keju dengan topping melimpah.", "tag": "Keju"},
    {"id": 7, "name": "Es Teh Manis", "cat": "Minuman", "price": 5000, "emoji": "🧋", "desc": "Segar dan manis, pas buat teman makan.", "tag": "Hemat"},
    {"id": 8, "name": "Jus Jeruk", "cat": "Minuman", "price": 10000, "emoji": "🍹", "desc": "Jus jeruk segar dengan rasa citrus.", "tag": "Segar"},
    {"id": 9, "name": "Donat Cokelat", "cat": "Camilan", "price": 8000, "emoji": "🍩", "desc": "Donat lembut dengan topping cokelat.", "tag": "Manis"},
    {"id": 10, "name": "Pisang Keju", "cat": "Camilan", "price": 10000, "emoji": "🍌", "desc": "Pisang manis dengan taburan keju.", "tag": "Favorit"},
    {"id": 11, "name": "Sushi Roll", "cat": "Makanan berat", "price": 26000, "emoji": "🍣", "desc": "Sushi roll praktis dengan rasa gurih.", "tag": "Spesial"},
    {"id": 12, "name": "Es Krim", "cat": "Camilan", "price": 9000, "emoji": "🍨", "desc": "Dessert dingin untuk penutup makan.", "tag": "Dingin"},
    {"id": 13, "name": "Chicken Katsu", "cat": "Makanan berat", "price": 20000, "emoji": "🍱", "desc": "Ayam katsu renyah dengan saus gurih.", "tag": "Favorit"},
    {"id": 14, "name": "Hot Dog", "cat": "Fast food", "price": 17000, "emoji": "🌭", "desc": "Roti lembut dengan sosis dan saus.", "tag": "Praktis"},
    {"id": 15, "name": "Kopi Susu", "cat": "Minuman", "price": 12000, "emoji": "☕", "desc": "Kopi susu dingin untuk penyemangat.", "tag": "Kopi"},
    {"id": 16, "name": "Pancake", "cat": "Camilan", "price": 16000, "emoji": "🥞", "desc": "Pancake lembut dengan sirup manis.", "tag": "Manis"},
    {"id": 17, "name": "Dimsum", "cat": "Camilan", "price": 15000, "emoji": "🥟", "desc": "Dimsum hangat cocok untuk sharing.", "tag": "Populer"},
    {"id": 18, "name": "Salad Buah", "cat": "Camilan", "price": 13000, "emoji": "🥗", "desc": "Potongan buah segar dengan saus creamy.", "tag": "Segar"},
]
CATEGORIES = ["Semua", "Makanan berat", "Fast food", "Minuman", "Camilan"]


def rupiah(value):
    return "Rp" + f"{int(value):,}".replace(",", ".")


class RoundedPanel(BoxLayout):
    def __init__(self, bg=WHITE, radius=16, **kwargs):
        super().__init__(**kwargs)
        self.bg = bg
        self.radius = dp(radius)
        with self.canvas.before:
            self._color = Color(*self.bg)
            self._rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[self.radius])
        self.bind(pos=self._update_rect, size=self._update_rect)

    def _update_rect(self, *_):
        self._rect.pos = self.pos
        self._rect.size = self.size


class FoodieButton(Button):
    def __init__(self, bg=ORANGE, fg=WHITE, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ""
        self.background_down = ""
        self.background_color = bg
        self.color = fg
        self.bold = True
        self.font_size = sp(14)
        self.size_hint_y = None
        self.height = dp(44)


class FoodCard(RoundedPanel):
    def __init__(self, food, app, **kwargs):
        super().__init__(orientation="vertical", padding=dp(10), spacing=dp(5), bg=WHITE, radius=15, **kwargs)
        self.food = food
        self.app = app
        self.size_hint_y = None
        self.height = dp(190)

        emoji = Label(text=food["emoji"], font_size=sp(36), size_hint_y=None, height=dp(48), color=INK)
        self.add_widget(emoji)
        title = Label(text=f"[b]{food['name']}[/b]", markup=True, font_size=sp(14), color=INK,
                      size_hint_y=None, height=dp(25), halign="left", valign="middle")
        title.bind(size=lambda inst, val: setattr(inst, "text_size", val))
        self.add_widget(title)
        desc = Label(text=food["desc"], font_size=sp(10.5), color=MUTED,
                     size_hint_y=None, height=dp(31), halign="left", valign="top")
        desc.bind(size=lambda inst, val: setattr(inst, "text_size", val))
        self.add_widget(desc)
        bottom = BoxLayout(size_hint_y=None, height=dp(38), spacing=dp(5))
        price = Label(text=rupiah(food["price"]), font_size=sp(12), bold=True, color=DARK_ORANGE,
                      halign="left", valign="middle")
        price.bind(size=lambda inst, val: setattr(inst, "text_size", val))
        bottom.add_widget(price)
        add = FoodieButton(text="+ Tambah", bg=ORANGE, font_size=sp(11))
        add.size_hint_x = None
        add.width = dp(82)
        add.height = dp(34)
        add.bind(on_release=lambda *_: app.add_to_cart(food["id"]))
        bottom.add_widget(add)
        self.add_widget(bottom)


class FoodieGoApp(App):
    title = "FOODIE GO"

    def build(self):
        self.cart = {}
        self.favorites = set()
        self.history = []
        self.selected_category = "Semua"
        self.search_text = ""
        self.root_layout = BoxLayout(orientation="vertical", spacing=0)
        with self.root_layout.canvas.before:
            Color(*CREAM)
            self.bg_rect = Rectangle(pos=self.root_layout.pos, size=self.root_layout.size)
        self.root_layout.bind(pos=self._update_bg, size=self._update_bg)

        header = RoundedPanel(orientation="vertical", bg=ORANGE, radius=0,
                              padding=[dp(16), dp(13), dp(16), dp(16)], spacing=dp(4),
                              size_hint_y=None, height=dp(142))
        brand = Label(text="[b]🍊 FOODIE GO[/b]", markup=True, font_size=sp(22),
                      color=WHITE, size_hint_y=None, height=dp(34), halign="left")
        brand.bind(size=lambda inst, val: setattr(inst, "text_size", val))
        header.add_widget(brand)
        tagline = Label(text="PESAN • NIKMATI • ULANGI", font_size=sp(10), color=WHITE,
                        size_hint_y=None, height=dp(20), halign="left")
        tagline.bind(size=lambda inst, val: setattr(inst, "text_size", val))
        header.add_widget(tagline)
        hero = Label(text="[b]Lagi lapar? Gas, pesan aja![/b]\\nPilih menu favoritmu dari HP.", markup=True,
                     font_size=sp(16), color=WHITE, halign="left", valign="middle")
        hero.bind(size=lambda inst, val: setattr(inst, "text_size", val))
        header.add_widget(hero)
        self.root_layout.add_widget(header)

        # Konten utama scroll agar nyaman di layar kecil
        scroll = ScrollView(do_scroll_x=False, bar_width=dp(4))
        self.content = BoxLayout(orientation="vertical", padding=[dp(12), dp(12), dp(12), dp(16)],
                                 spacing=dp(10), size_hint_y=None)
        self.content.bind(minimum_height=self.content.setter("height"))

        search_row = BoxLayout(size_hint_y=None, height=dp(44), spacing=dp(7))
        self.search_input = TextInput(hint_text="Cari makanan...", multiline=False, size_hint_x=1,
                                      font_size=sp(14), padding=[dp(10), dp(10), dp(10), dp(8)],
                                      background_normal="", background_active="", background_color=WHITE,
                                      foreground_color=INK, cursor_color=ORANGE)
        self.search_input.bind(text=self.on_search)
        search_row.add_widget(self.search_input)
        reset_btn = FoodieButton(text="Reset", bg=PALE_ORANGE, fg=DARK_ORANGE)
        reset_btn.size_hint_x = None
        reset_btn.width = dp(62)
        reset_btn.bind(on_release=lambda *_: self.reset_filters())
        search_row.add_widget(reset_btn)
        self.content.add_widget(search_row)

        self.category_row = BoxLayout(size_hint_y=None, height=dp(42), spacing=dp(5))
        self.content.add_widget(self.category_row)

        self.content.add_widget(self.section_label("Menu favorit"))
        self.menu_grid = GridLayout(cols=2, spacing=dp(9), size_hint_y=None, padding=0)
        self.menu_grid.bind(minimum_height=self.menu_grid.setter("height"))
        self.content.add_widget(self.menu_grid)

        self.content.add_widget(self.section_label("🛒 Keranjang kamu"))
        self.cart_panel = RoundedPanel(orientation="vertical", bg=WHITE, padding=dp(12),
                                       spacing=dp(6), size_hint_y=None)
        self.cart_panel.bind(minimum_height=self.cart_panel.setter("height"))
        self.content.add_widget(self.cart_panel)

        self.content.add_widget(self.section_label("🧾 Riwayat pesanan demo"))
        self.history_panel = RoundedPanel(orientation="vertical", bg=WHITE, padding=dp(12),
                                          spacing=dp(5), size_hint_y=None)
        self.history_panel.bind(minimum_height=self.history_panel.setter("height"))
        self.content.add_widget(self.history_panel)

        footer = Label(text="[b]FOODIE GO[/b]\\nCreated by Revan", markup=True, color=DARK_ORANGE,
                       font_size=sp(12), size_hint_y=None, height=dp(48), halign="center")
        self.content.add_widget(footer)
        scroll.add_widget(self.content)
        self.root_layout.add_widget(scroll)

        self.render_categories()
        self.render_menu()
        self.render_cart()
        self.render_history()
        Window.bind(size=self.on_window_size)
        return self.root_layout

    def _update_bg(self, *_):
        self.bg_rect.pos = self.root_layout.pos
        self.bg_rect.size = self.root_layout.size

    def on_window_size(self, *_):
        # Dua kolom di ponsel, tiga kolom jika jendela cukup lebar.
        if hasattr(self, "menu_grid"):
            self.menu_grid.cols = 3 if Window.width >= dp(700) else 2

    def section_label(self, text):
        label = Label(text=f"[b]{text}[/b]", markup=True, color=INK, font_size=sp(17),
                      size_hint_y=None, height=dp(31), halign="left", valign="middle")
        label.bind(size=lambda inst, val: setattr(inst, "text_size", val))
        return label

    def render_categories(self):
        self.category_row.clear_widgets()
        # Spinner lebih ramah layar kecil daripada tombol yang berjajar panjang.
        spinner = Spinner(text=self.selected_category, values=CATEGORIES, size_hint_x=1,
                          size_hint_y=None, height=dp(40), font_size=sp(13),
                          background_normal="", background_color=PALE_ORANGE, color=DARK_ORANGE)
        spinner.bind(text=self.on_category)
        self.category_row.add_widget(spinner)
        self.category_spinner = spinner
        fav_btn = FoodieButton(text="♡ Favorit", bg=PALE_ORANGE, fg=DARK_ORANGE)
        fav_btn.size_hint_x = None
        fav_btn.width = dp(100)
        fav_btn.bind(on_release=lambda *_: self.show_favorites())
        self.category_row.add_widget(fav_btn)

    def on_category(self, _spinner, value):
        self.selected_category = value
        self.render_menu()

    def on_search(self, _instance, value):
        self.search_text = value.lower().strip()
        self.render_menu()

    def reset_filters(self):
        self.search_input.text = ""
        self.selected_category = "Semua"
        self.category_spinner.text = "Semua"
        self.render_menu()

    def show_favorites(self):
        if not self.favorites:
            self.info_popup("Favorit", "Belum ada menu favorit. Tambahkan menu dari tombol ♡ di kartu makanan.")
            return
        self.render_menu(favorites_only=True)

    def render_menu(self, favorites_only=False):
        if not hasattr(self, "menu_grid"):
            return
        self.menu_grid.clear_widgets()
        q = self.search_text
        results = []
        for food in FOODS:
            match_cat = self.selected_category == "Semua" or food["cat"] == self.selected_category
            match_q = q in food["name"].lower() or q in food["desc"].lower() or q in food["cat"].lower()
            match_fav = (not favorites_only) or food["id"] in self.favorites
            if match_cat and match_q and match_fav:
                results.append(food)
        # Kartu ditempatkan di grid responsif; tingginya tetap konsisten.
        for food in results:
            self.menu_grid.add_widget(self.make_food_card(food))
        if not results:
            self.menu_grid.add_widget(Label(text="Menu tidak ditemukan.", color=MUTED,
                                            size_hint_y=None, height=dp(42)))
        self.menu_grid.cols = 3 if Window.width >= dp(700) else 2

    def make_food_card(self, food):
        card = RoundedPanel(orientation="vertical", padding=dp(9), spacing=dp(4), bg=WHITE,
                            radius=14, size_hint_y=None, height=dp(202))
        emoji_row = BoxLayout(size_hint_y=None, height=dp(40))
        emoji_row.add_widget(Label(text=food["emoji"], font_size=sp(31), color=INK))
        fav_text = "♥" if food["id"] in self.favorites else "♡"
        fav = FoodieButton(text=fav_text, bg=PALE_ORANGE, fg=DARK_ORANGE)
        fav.size_hint_x = None
        fav.width = dp(34)
        fav.height = dp(32)
        fav.bind(on_release=lambda *_args, fid=food["id"]: self.toggle_favorite(fid))
        emoji_row.add_widget(fav)
        card.add_widget(emoji_row)
        name = Label(text=f"[b]{food['name']}[/b]", markup=True, color=INK, font_size=sp(13),
                     size_hint_y=None, height=dp(25), halign="left", valign="middle")
        name.bind(size=lambda inst, val: setattr(inst, "text_size", val))
        card.add_widget(name)
        desc = Label(text=food["desc"], color=MUTED, font_size=sp(10), size_hint_y=None,
                     height=dp(31), halign="left", valign="top")
        desc.bind(size=lambda inst, val: setattr(inst, "text_size", val))
        card.add_widget(desc)
        tag = Label(text=f"★ {food['tag']}", color=DARK_ORANGE, font_size=sp(9),
                    size_hint_y=None, height=dp(17), halign="left")
        tag.bind(size=lambda inst, val: setattr(inst, "text_size", val))
        card.add_widget(tag)
        bottom = BoxLayout(size_hint_y=None, height=dp(35), spacing=dp(3))
        price = Label(text=rupiah(food["price"]), color=DARK_ORANGE, bold=True, font_size=sp(11),
                      halign="left", valign="middle")
        price.bind(size=lambda inst, val: setattr(inst, "text_size", val))
        bottom.add_widget(price)
        add = FoodieButton(text="+", bg=ORANGE)
        add.size_hint_x = None
        add.width = dp(36)
        add.height = dp(32)
        add.bind(on_release=lambda *_args, fid=food["id"]: self.add_to_cart(fid))
        bottom.add_widget(add)
        card.add_widget(bottom)
        return card

    def toggle_favorite(self, food_id):
        if food_id in self.favorites:
            self.favorites.remove(food_id)
        else:
            self.favorites.add(food_id)
        self.render_menu()

    def add_to_cart(self, food_id):
        self.cart[food_id] = self.cart.get(food_id, 0) + 1
        self.render_cart()

    def change_quantity(self, food_id, delta):
        self.cart[food_id] = self.cart.get(food_id, 0) + delta
        if self.cart[food_id] <= 0:
            self.cart.pop(food_id, None)
        self.render_cart()

    def clear_cart(self):
        self.cart = {}
        self.render_cart()

    def cart_totals(self):
        count = sum(self.cart.values())
        subtotal = sum(next(f["price"] for f in FOODS if f["id"] == fid) * qty
                       for fid, qty in self.cart.items())
        service = 2000 if count else 0
        return count, subtotal, service, subtotal + service

    def render_cart(self):
        if not hasattr(self, "cart_panel"):
            return
        self.cart_panel.clear_widgets()
        count, subtotal, service, total = self.cart_totals()
        if not self.cart:
            self.cart_panel.add_widget(Label(text="Keranjang masih kosong. Pilih menu dulu! 😋",
                                             color=MUTED, size_hint_y=None, height=dp(36),
                                             font_size=sp(12)))
        else:
            for fid, qty in list(self.cart.items()):
                food = next(f for f in FOODS if f["id"] == fid)
                row = BoxLayout(size_hint_y=None, height=dp(45), spacing=dp(4))
                info = Label(text=f"[b]{food['emoji']} {food['name']}[/b]\\n{rupiah(food['price'])} × {qty} = {rupiah(food['price'] * qty)}",
                             markup=True, color=INK, font_size=sp(10), halign="left", valign="middle")
                info.bind(size=lambda inst, val: setattr(inst, "text_size", val))
                row.add_widget(info)
                minus = FoodieButton(text="−", bg=PALE_ORANGE, fg=DARK_ORANGE)
                minus.size_hint_x = None
                minus.width = dp(32)
                minus.bind(on_release=lambda *_args, f_id=fid: self.change_quantity(f_id, -1))
                row.add_widget(minus)
                qty_label = Label(text=str(qty), color=INK, size_hint_x=None, width=dp(20), font_size=sp(12))
                row.add_widget(qty_label)
                plus = FoodieButton(text="+", bg=PALE_ORANGE, fg=DARK_ORANGE)
                plus.size_hint_x = None
                plus.width = dp(32)
                plus.bind(on_release=lambda *_args, f_id=fid: self.change_quantity(f_id, 1))
                row.add_widget(plus)
                self.cart_panel.add_widget(row)
        self.cart_panel.add_widget(self.summary_line("Subtotal", rupiah(subtotal)))
        self.cart_panel.add_widget(self.summary_line("Biaya layanan demo", rupiah(service)))
        self.cart_panel.add_widget(self.summary_line("TOTAL", rupiah(total), bold=True))
        checkout = FoodieButton(text="Lanjut ke checkout", bg=GREEN)
        checkout.disabled = count == 0
        checkout.bind(on_release=lambda *_: self.checkout_popup())
        self.cart_panel.add_widget(checkout)
        clear = FoodieButton(text="Kosongkan keranjang", bg=PALE_ORANGE, fg=DARK_ORANGE)
        clear.bind(on_release=lambda *_: self.clear_cart())
        self.cart_panel.add_widget(clear)

    def summary_line(self, label, value, bold=False):
        text = f"[b]{label}: {value}[/b]" if bold else f"{label}: {value}"
        lab = Label(text=text, markup=True, color=INK, font_size=sp(12), size_hint_y=None,
                    height=dp(24), halign="right", valign="middle")
        lab.bind(size=lambda inst, val: setattr(inst, "text_size", val))
        return lab

    def checkout_popup(self):
        if not self.cart:
            self.info_popup("Keranjang kosong", "Tambahkan makanan sebelum checkout.")
            return
        layout = BoxLayout(orientation="vertical", padding=dp(14), spacing=dp(7))
        scroll = ScrollView(do_scroll_x=False)
        fields = BoxLayout(orientation="vertical", spacing=dp(7), size_hint_y=None)
        fields.bind(minimum_height=fields.setter("height"))
        fields.add_widget(Label(text="[b]Detail pesanan[/b]", markup=True, color=INK,
                                size_hint_y=None, height=dp(30), font_size=sp(17)))
        self.name_input = TextInput(hint_text="Nama pemesan *", multiline=False, size_hint_y=None,
                                    height=dp(43), font_size=sp(13), padding=dp(10))
        self.phone_input = TextInput(hint_text="Nomor HP *", multiline=False, size_hint_y=None,
                                     height=dp(43), font_size=sp(13), input_filter="int", padding=dp(10))
        self.address_input = TextInput(hint_text="Alamat pengantaran *", multiline=True, size_hint_y=None,
                                       height=dp(70), font_size=sp(13), padding=dp(10))
        self.payment_input = Spinner(text="Bayar tunai (COD)",
                                     values=("Bayar tunai (COD)", "Transfer bank (demo)", "QRIS (demo)"),
                                     size_hint_y=None, height=dp(43), font_size=sp(12))
        self.notes_input = TextInput(hint_text="Catatan untuk penjual (opsional)", multiline=True,
                                     size_hint_y=None, height=dp(62), font_size=sp(13), padding=dp(10))
        for widget in (self.name_input, self.phone_input, self.address_input,
                       self.payment_input, self.notes_input):
            fields.add_widget(widget)
        count, subtotal, service, total = self.cart_totals()
        fields.add_widget(Label(text=f"Total pembayaran demo: {rupiah(total)}",
                                color=DARK_ORANGE, bold=True, size_hint_y=None,
                                height=dp(30), font_size=sp(13)))
        fields.add_widget(Label(text="Demo saja: tidak ada pembayaran/pengiriman nyata.",
                                color=MUTED, size_hint_y=None, height=dp(28), font_size=sp(10)))
        scroll.add_widget(fields)
        layout.add_widget(scroll)
        actions = BoxLayout(size_hint_y=None, height=dp(43), spacing=dp(8))
        self.checkout_popup_ref = Popup(title="FOODIE GO — Checkout", content=layout,
                                        size_hint=(0.94, 0.84), auto_dismiss=False)
        cancel = FoodieButton(text="Kembali", bg=PALE_ORANGE, fg=DARK_ORANGE)
        cancel.bind(on_release=lambda *_: self.checkout_popup_ref.dismiss())
        submit = FoodieButton(text="Buat ringkasan", bg=GREEN)
        submit.bind(on_release=lambda *_: self.make_order())
        actions.add_widget(cancel)
        actions.add_widget(submit)
        layout.add_widget(actions)
        self.checkout_popup_ref.open()

    def make_order(self):
        name = self.name_input.text.strip()
        phone = self.phone_input.text.strip()
        address = self.address_input.text.strip()
        if not name or not phone or not address:
            self.info_popup("Data belum lengkap", "Isi nama, nomor HP, dan alamat terlebih dahulu.")
            return
        count, subtotal, service, total = self.cart_totals()
        lines = []
        for fid, qty in self.cart.items():
            food = next(f for f in FOODS if f["id"] == fid)
            lines.append(f"{food['name']} x{qty} — {rupiah(food['price'] * qty)}")
        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M")
        note = self.notes_input.text.strip() or "-"
        message = (
            "RINGKASAN PESANAN FOODIE GO\\nCreated by Revan\\n"
            f"Waktu: {timestamp}\\nNama: {name}\\nNomor HP: {phone}\\nAlamat: {address}\\n\\n"
            + "\\n".join(lines) + f"\\n\\nSubtotal: {rupiah(subtotal)}\\nBiaya layanan demo: {rupiah(service)}"
            + f"\\nTOTAL: {rupiah(total)}\\nPembayaran: {self.payment_input.text}\\nCatatan: {note}"
            + "\\n\\nDEMO: belum dikirim ke restoran dan tidak memproses pembayaran."
        )
        try:
            target = Path(self.user_data_dir) / "pesanan_foodie_go.txt"
            target.write_text(message, encoding="utf-8")
            saved = f"\\n\\nFile ringkasan disimpan di:\\n{target}"
        except Exception:
            saved = "\\n\\nSalin ringkasan ini jika ingin menyimpannya."
        self.history.insert(0, {"time": timestamp, "name": name, "total": total, "payment": self.payment_input.text})
        self.checkout_popup_ref.dismiss()
        self.cart = {}
        self.render_cart()
        self.render_history()
        self.receipt_popup(message + saved)

    def receipt_popup(self, message):
        layout = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(8))
        scroll = ScrollView()
        text = Label(text=message, color=INK, font_size=sp(11), size_hint_y=None,
                     halign="left", valign="top")
        text.bind(width=lambda inst, val: setattr(inst, "text_size", (val, None)))
        text.bind(texture_size=lambda inst, val: setattr(inst, "height", val[1] + dp(10)))
        scroll.add_widget(text)
        layout.add_widget(scroll)
        actions = BoxLayout(size_hint_y=None, height=dp(43), spacing=dp(8))
        copy_btn = FoodieButton(text="Salin teks", bg=PALE_ORANGE, fg=DARK_ORANGE)
        copy_btn.bind(on_release=lambda *_: self.copy_receipt(message))
        close_btn = FoodieButton(text="Tutup", bg=GREEN)
        actions.add_widget(copy_btn)
        actions.add_widget(close_btn)
        layout.add_widget(actions)
        popup = Popup(title="Ringkasan pesanan", content=layout, size_hint=(0.94, 0.78))
        close_btn.bind(on_release=popup.dismiss)
        popup.open()

    def copy_receipt(self, message):
        try:
            Clipboard.copy(message)
            self.info_popup("Tersalin", "Ringkasan pesanan disalin ke clipboard.")
        except Exception:
            self.info_popup("Info", "Fitur salin tidak tersedia di perangkat ini.")

    def render_history(self):
        if not hasattr(self, "history_panel"):
            return
        self.history_panel.clear_widgets()
        if not self.history:
            self.history_panel.add_widget(Label(text="Belum ada pesanan demo.", color=MUTED,
                                                size_hint_y=None, height=dp(34), font_size=sp(12)))
            return
        for index, item in enumerate(self.history[:8], start=1):
            lab = Label(text=f"[b]Pesanan #{index}[/b]  •  {item['time']}\\n{item['name']} — {rupiah(item['total'])}\\n{item['payment']}",
                        markup=True, color=INK, font_size=sp(11), size_hint_y=None,
                        height=dp(53), halign="left", valign="middle")
            lab.bind(size=lambda inst, val: setattr(inst, "text_size", val))
            self.history_panel.add_widget(lab)
        clear = FoodieButton(text="Hapus riwayat demo", bg=PALE_ORANGE, fg=DARK_ORANGE)
        clear.bind(on_release=lambda *_: self.clear_history())
        self.history_panel.add_widget(clear)

    def clear_history(self):
        self.history = []
        self.render_history()

    def info_popup(self, title, message):
        box = BoxLayout(orientation="vertical", padding=dp(14), spacing=dp(10))
        label = Label(text=message, color=INK, font_size=sp(13), halign="center", valign="middle")
        label.bind(size=lambda inst, val: setattr(inst, "text_size", val))
        box.add_widget(label)
        ok = FoodieButton(text="Oke", bg=ORANGE)
        box.add_widget(ok)
        popup = Popup(title=title, content=box, size_hint=(0.86, 0.34))
        ok.bind(on_release=popup.dismiss)
        popup.open()


if __name__ == "__main__":
    FoodieGoApp().run()

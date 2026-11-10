import json
import os
from datetime import datetime

from kivy.app import App
from kivy.core.clipboard import Clipboard
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

FILE_DATA = "data_tahanan.json"

BLOK_FIELDS = [
    ("sat_reskrim", "Sat Reskrim"),
    ("sat_narkoba", "Sat Narkoba"),
    ("sat_lantas", "Sat Lantas"),
    ("sat_polair", "Sat Polair"),
    ("titipan", "Titipan"),
]

KASUS_FIELDS = [
    ("krimum", "KRIMUM"),
    ("krimsus", "KRIMSUS"),
    ("narkoba", "NARKOBA"),
    ("laka_lantas", "LAKA LANTAS"),
]

POLRI_ROWS = [
    ("satreskrim", "SATRESKRIM"),
    ("satnarkoba", "SATNARKOBA"),
    ("satpolair", "SATPOLAIR"),
    ("satlantas", "SATLANTAS"),
    ("polsek", "POLSEK"),
]

TITIPAN_ROWS = [
    ("polsek", "POLSEK"),
    ("jaksa", "JAKSA"),
    ("pengadilan", "PENGADILAN"),
    ("kehutanan", "KEHUTANAN"),
]

DEMO_FIELDS = [
    ("laki", "LAKI"),
    ("prmpuan", "PEREMPUAN"),
    ("anak_lk", "ANAK LK"),
    ("anak_pr", "ANAK PR"),
]

MUTASI_FIELDS = [
    ("laki", "LAKI"),
    ("prmpuan", "PEREMPUAN"),
]

JABATAN_FIELDS = [
    ("jabatan_1", "1. Pangkat / Nama"),
    ("jabatan_2", "2. Pangkat / Nama"),
    ("jabatan_3", "3. Pangkat / Nama"),
    ("jabatan_4", "4. Pangkat / Nama"),
]


def struktur_baru():
    return {
        "blok": {
            str(i): {key: 0 for key, _ in BLOK_FIELDS}
            for i in range(1, 15)
        },
        "polri": {
            "tabel": {
                row: {key: 0 for key, _ in KASUS_FIELDS}
                for row, _ in POLRI_ROWS
            },
            "demo": {key: 0 for key, _ in DEMO_FIELDS},
            "mutasi": {
                "bon": {key: 0 for key, _ in MUTASI_FIELDS},
                "tahap2": {key: 0 for key, _ in MUTASI_FIELDS},
                "masuk": {key: 0 for key, _ in MUTASI_FIELDS},
            },
        },
        "titipan": {
            "tabel": {
                row: {key: 0 for key, _ in KASUS_FIELDS}
                for row, _ in TITIPAN_ROWS
            },
            "demo": {key: 0 for key, _ in DEMO_FIELDS},
            "mutasi": {
                "bon": {key: 0 for key, _ in MUTASI_FIELDS},
                "tahap2": {key: 0 for key, _ in MUTASI_FIELDS},
                "masuk": {key: 0 for key, _ in MUTASI_FIELDS},
            },
        },
    }


def muat_data():
    data = struktur_baru()

    if not os.path.exists(FILE_DATA):
        return data

    try:
        with open(FILE_DATA, "r", encoding="utf-8") as file:
            simpanan = json.load(file)

        data["blok"].update(simpanan.get("blok", {}))
        data["polri"].update(simpanan.get("polri", {}))
        data["titipan"].update(simpanan.get("titipan", {}))

        for kategori in ["polri", "titipan"]:
            mutasi_lama = data[kategori].get("mutasi", {})

            data[kategori]["mutasi"] = {
                "bon": mutasi_lama.get(
                    "bon", {"laki": 0, "prmpuan": 0}
                ),
                "tahap2": mutasi_lama.get(
                    "tahap2", {"laki": 0, "prmpuan": 0}
                ),
                "masuk": mutasi_lama.get(
                    "masuk", {"laki": 0, "prmpuan": 0}
                ),
            }

    except (json.JSONDecodeError, OSError):
        pass

    return data


def simpan_data(data):
    with open(FILE_DATA, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def ambil_angka(teks):
    try:
        return max(0, int(teks or 0))
    except (TypeError, ValueError):
        return 0


class TahananApp(App):
    def build(self):
        self.title = "Sistem Tahanan"
        self.mode_gelap = True

        self.data = muat_data()

        self.data_laporan = {
            "jabatan_1": "",
            "jabatan_2": "",
            "jabatan_3": "",
            "jabatan_4": "",
        }

        self.root = BoxLayout(orientation="vertical")
        self.buat_tampilan()
        return self.root

    def warna(self):
        if self.mode_gelap:
            return {
                "latar": (0.08, 0.09, 0.12, 1),
                "kartu": (0.14, 0.16, 0.2, 1),
                "teks": (0.93, 0.95, 0.98, 1),
                "redup": (0.7, 0.75, 0.82, 1),
                "biru": (0.16, 0.45, 0.85, 1),
                "hijau": (0.1, 0.6, 0.4, 1),
                "oranye": (0.9, 0.55, 0.1, 1),
                "merah": (0.85, 0.25, 0.25, 1),
                "ungu": (0.55, 0.35, 0.9, 1),
                "teal": (0.1, 0.65, 0.65, 1),
                "input": (0.2, 0.22, 0.27, 1),
            }

        return {
            "latar": (0.95, 0.96, 0.98, 1),
            "kartu": (1, 1, 1, 1),
            "teks": (0.1, 0.15, 0.25, 1),
            "redup": (0.4, 0.45, 0.52, 1),
            "biru": (0.08, 0.25, 0.55, 1),
            "hijau": (0.05, 0.45, 0.3, 1),
            "oranye": (0.75, 0.45, 0.05, 1),
            "merah": (0.75, 0.2, 0.2, 1),
            "ungu": (0.45, 0.25, 0.75, 1),
            "teal": (0.05, 0.5, 0.5, 1),
            "input": (0.94, 0.96, 0.99, 1),
        }

    def buat_tampilan(self):
        warna = self.warna()
        Window.clearcolor = warna["latar"]

        self.root.clear_widgets()

        utama = BoxLayout(
            orientation="vertical",
            padding=dp(10),
            spacing=dp(10),
        )

        header = BoxLayout(
            size_hint=(1, None),
            height=dp(48),
            spacing=dp(8),
        )

        judul = Label(
            text="SISTEM TAHANAN",
            bold=True,
            font_size="17sp",
            color=warna["teks"],
            size_hint=(0.6, 1),
            halign="left",
            valign="middle",
        )
        judul.bind(size=judul.setter("text_size"))
        header.add_widget(judul)

        tombol_mode = Button(
            text="Mode",
            bold=True,
            font_size="12sp",
            size_hint=(0.18, 1),
            background_normal="",
            background_down="",
            background_color=warna["biru"],
            color=(1, 1, 1, 1),
        )
        tombol_mode.bind(on_press=self.ganti_mode)
        header.add_widget(tombol_mode)

        tombol_menu = Button(
            text="Menu",
            bold=True,
            font_size="12sp",
            size_hint=(0.22, 1),
            background_normal="",
            background_down="",
            background_color=warna["hijau"],
            color=(1, 1, 1, 1),
        )
        tombol_menu.bind(on_press=self.buka_menu)
        header.add_widget(tombol_menu)

        utama.add_widget(header)

        self.konten = BoxLayout()
        utama.add_widget(self.konten)

        self.root.add_widget(utama)
        self.buka_halaman("Blok")

    def ganti_mode(self, instance):
        self.mode_gelap = not self.mode_gelap
        self.buat_tampilan()

    def buka_menu(self, instance):
        warna = self.warna()

        isi = BoxLayout(
            orientation="vertical",
            padding=dp(12),
            spacing=dp(8),
            size_hint=(1, None),
        )
        isi.bind(minimum_height=isi.setter("height"))

        daftar = [
            ("Blok", warna["biru"]),
            ("Polri", warna["teal"]),
            ("Titipan", warna["ungu"]),
            ("Bon Polri", warna["oranye"]),
            ("Bon Titipan", warna["merah"]),
            ("Laporan", warna["hijau"]),
            ("Rekap", warna["biru"]),
        ]

        for nama, warna_tombol in daftar:
            tombol = Button(
                text=nama,
                bold=True,
                font_size="14sp",
                size_hint=(1, None),
                height=dp(46),
                background_normal="",
                background_down="",
                background_color=warna_tombol,
                color=(1, 1, 1, 1),
            )
            tombol.bind(
                on_press=lambda instance, halaman=nama: self.pilih_menu(halaman)
            )
            isi.add_widget(tombol)

        self.popup_menu = Popup(
            title="Pilih Halaman",
            title_size="14sp",
            content=isi,
            size_hint=(0.8, 0.7),
            auto_dismiss=True,
        )
        self.popup_menu.open()

    def pilih_menu(self, nama):
        if hasattr(self, "popup_menu"):
            self.popup_menu.dismiss()

        self.buka_halaman(nama)

    def buat_scroll(self, isi):
        scroll = ScrollView(do_scroll_x=False)
        scroll.add_widget(isi)
        return scroll

    def buat_kolom(self):
        isi = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=dp(10),
            padding=[dp(2), dp(2), dp(2), dp(24)],
        )
        isi.bind(minimum_height=isi.setter("height"))
        return isi

    def buat_label(self, teks, ukuran="14sp", tebal=False, warna=None):
        return Label(
            text=teks,
            bold=tebal,
            font_size=ukuran,
            color=warna or self.warna()["teks"],
            size_hint=(1, None),
            height=dp(24),
            halign="left",
            valign="middle",
        )

    def buat_input_angka(self, nilai, callback):
        warna = self.warna()

        input_angka = TextInput(
            text=str(nilai),
            input_filter="int",
            multiline=False,
            font_size="15sp",
            size_hint=(0.45, 1),
            background_normal="",
            background_active="",
            background_color=warna["input"],
            foreground_color=warna["teks"],
            cursor_color=warna["biru"],
            padding=[dp(10), dp(10), dp(10), dp(10)],
        )

        input_angka.bind(
            text=lambda instance, teks: callback(ambil_angka(teks))
        )
        return input_angka

    def buat_baris_input(self, nama, nilai, callback):
        warna = self.warna()

        baris = BoxLayout(
            size_hint=(1, None),
            height=dp(46),
            spacing=dp(8),
        )

        label = Label(
            text=nama,
            font_size="14sp",
            color=warna["redup"],
            size_hint=(0.55, 1),
            halign="left",
            valign="middle",
        )
        label.bind(size=label.setter("text_size"))
        baris.add_widget(label)

        baris.add_widget(
            self.buat_input_angka(nilai, callback)
        )
        return baris

    def buat_form(self, judul, fields, nilai, callback, warna_border):
        warna = self.warna()

        kartu = BoxLayout(
            orientation="vertical",
            padding=dp(12),
            spacing=dp(8),
            size_hint=(1, None),
        )
        kartu.bind(minimum_height=kartu.setter("height"))

        kartu.add_widget(
            self.buat_label(judul, "15sp", True, warna["teks"])
        )

        for key, nama in fields:
            kartu.add_widget(
                self.buat_baris_input(
                    nama,
                    nilai.get(key, 0),
                    lambda angka, kunci=key: callback(kunci, angka),
                )
            )

        return kartu

    def buka_halaman(self, nama):
        self.konten.clear_widgets()

        if nama == "Blok":
            self.konten.add_widget(self.halaman_blok())

        elif nama == "Polri":
            self.konten.add_widget(
                self.halaman_kategori("polri", POLRI_ROWS, "POLRI")
            )

        elif nama == "Titipan":
            self.konten.add_widget(
                self.halaman_kategori("titipan", TITIPAN_ROWS, "TITIPAN")
            )

        elif nama == "Bon Polri":
            self.konten.add_widget(
                self.halaman_mutasi("polri", "POLRI")
            )

        elif nama == "Bon Titipan":
            self.konten.add_widget(
                self.halaman_mutasi("titipan", "TITIPAN")
            )

        elif nama == "Laporan":
            self.konten.add_widget(self.halaman_laporan())

        else:
            self.konten.add_widget(self.halaman_rekap())

    def halaman_blok(self):
        warna = self.warna()
        isi = self.buat_kolom()

        label = self.buat_label("NOMOR BLOK", "14sp", True, warna["teks"])
        isi.add_widget(label)

        pilih_blok = TextInput(
            text="1",
            input_filter="int",
            multiline=False,
            font_size="16sp",
            size_hint=(1, None),
            height=dp(44),
            background_normal="",
            background_active="",
            background_color=warna["input"],
            foreground_color=warna["teks"],
            cursor_color=warna["biru"],
            padding=[dp(10), dp(10), dp(10), dp(10)],
        )
        isi.add_widget(pilih_blok)

        self.input_blok = {}

        for key, nama in BLOK_FIELDS:
            baris = self.buat_baris_input(
                nama,
                self.data["blok"]["1"][key],
                lambda angka, kunci=key: None,
            )

            self.input_blok[key] = baris.children[0]
            isi.add_widget(baris)

        status = Label(
            text="",
            font_size="12sp",
            color=warna["hijau"],
            size_hint=(1, None),
            height=dp(22),
        )
        isi.add_widget(status)

        tombol = Button(
            text="SIMPAN BLOK",
            bold=True,
            font_size="14sp",
            size_hint=(1, None),
            height=dp(46),
            background_normal="",
            background_down="",
            background_color=warna["biru"],
            color=(1, 1, 1, 1),
        )

        def simpan(instance):
            try:
                nomor = str(max(1, min(14, int(pilih_blok.text or 1))))
            except (TypeError, ValueError):
                nomor = "1"

            for key, _ in BLOK_FIELDS:
                self.data["blok"][nomor][key] = ambil_angka(
                    self.input_blok[key].text
                )

            simpan_data(self.data)
            status.text = f"Data Blok {nomor} tersimpan."

        tombol.bind(on_press=simpan)
        isi.add_widget(tombol)

        return self.buat_scroll(isi)

    def halaman_kategori(self, kategori, rows, judul):
        isi = self.buat_kolom()
        warna = self.warna()

        for row_key, row_name in rows:
            kartu = self.buat_form(
                row_name,
                KASUS_FIELDS,
                self.data[kategori]["tabel"][row_key],
                lambda kunci, angka, baris=row_key: self.simpan_nilai(
                    kategori, "tabel", baris, kunci, angka
                ),
                warna["teal"] if kategori == "polri" else warna["ungu"],
            )
            isi.add_widget(kartu)

        kartu_demo = self.buat_form(
            f"TAH {judul}",
            DEMO_FIELDS,
            self.data[kategori]["demo"],
            lambda kunci, angka: self.simpan_nilai(
                kategori, "demo", None, kunci, angka
            ),
            warna["hijau"],
        )
        isi.add_widget(kartu_demo)

        return self.buat_scroll(isi)

    def simpan_nilai(self, kategori, jenis, baris, kunci, angka):
        if jenis == "tabel":
            self.data[kategori]["tabel"][baris][kunci] = angka
        else:
            self.data[kategori]["demo"][kunci] = angka

        simpan_data(self.data)

    def halaman_mutasi(self, kategori, judul):
        isi = self.buat_kolom()
        warna = self.warna()

        kartu_bon = self.buat_form(
            "BON TAHANAN",
            MUTASI_FIELDS,
            self.data[kategori]["mutasi"]["bon"],
            lambda kunci, angka: self.simpan_mutasi(
                kategori, "bon", kunci, angka
            ),
            warna["oranye"],
        )
        isi.add_widget(kartu_bon)

        kartu_tahap2 = self.buat_form(
            "TAHAP 2",
            MUTASI_FIELDS,
            self.data[kategori]["mutasi"]["tahap2"],
            lambda kunci, angka: self.simpan_mutasi(
                kategori, "tahap2", kunci, angka
            ),
            warna["merah"],
        )
        isi.add_widget(kartu_tahap2)

        kartu_masuk = self.buat_form(
            "TAHANAN MASUK",
            MUTASI_FIELDS,
            self.data[kategori]["mutasi"]["masuk"],
            lambda kunci, angka: self.simpan_mutasi(
                kategori, "masuk", kunci, angka
            ),
            warna["hijau"],
        )
        isi.add_widget(kartu_masuk)

        demo = self.data[kategori]["demo"]
        mutasi = self.data[kategori]["mutasi"]

        stok_laki = (
            demo["laki"]
            - mutasi["bon"]["laki"]
            - mutasi["tahap2"]["laki"]
            + mutasi["masuk"]["laki"]
        )

        stok_perempuan = (
            demo["prmpuan"]
            - mutasi["bon"]["prmpuan"]
            - mutasi["tahap2"]["prmpuan"]
            + mutasi["masuk"]["prmpuan"]
        )

        isi.add_widget(
            self.buat_label(
                f"STOK AKHIR LAKI: {max(0, stok_laki)}",
                "16sp",
                True,
                warna["teks"],
            )
        )

        isi.add_widget(
            self.buat_label(
                f"STOK AKHIR PEREMPUAN: {max(0, stok_perempuan)}",
                "16sp",
                True,
                warna["teks"],
            )
        )

        return self.buat_scroll(isi)

    def simpan_mutasi(self, kategori, jenis, kunci, angka):
        self.data[kategori]["mutasi"][jenis][kunci] = angka
        simpan_data(self.data)

    def halaman_rekap(self):
        warna = self.warna()
        isi = self.buat_kolom()

        total_blok = sum(
            sum(nilai.values())
            for nilai in self.data["blok"].values()
        )

        total_polri = sum(
            sum(nilai.values())
            for nilai in self.data["polri"]["tabel"].values()
        )

        total_titipan = sum(
            sum(nilai.values())
            for nilai in self.data["titipan"]["tabel"].values()
        )

        total_keseluruhan = total_polri + total_titipan

        isi.add_widget(
            self.buat_label(
                f"TOTAL BLOK: {total_blok}",
                "16sp",
                True,
                warna["teks"],
            )
        )

        isi.add_widget(
            self.buat_label(
                f"TOTAL POLRI: {total_polri}",
                "16sp",
                True,
                warna["teks"],
            )
        )

        isi.add_widget(
            self.buat_label(
                f"TOTAL TITIPAN: {total_titipan}",
                "16sp",
                True,
                warna["teks"],
            )
        )

        isi.add_widget(
            self.buat_label(
                f"TOTAL KESELURUHAN: {total_keseluruhan}",
                "18sp",
                True,
                warna["hijau"],
            )
        )

        rows_blok = []
        total_kolom_blok = {key: 0 for key, _ in BLOK_FIELDS}

        for nomor in range(1, 15):
            nilai = self.data["blok"][str(nomor)]

            for key, _ in BLOK_FIELDS:
                total_kolom_blok[key] += nilai[key]

            rows_blok.append([
                nomor,
                nilai["sat_reskrim"],
                nilai["sat_narkoba"],
                nilai["sat_lantas"],
                nilai["sat_polair"],
                nilai["titipan"],
                sum(nilai.values()),
            ])

        rows_blok.append([
            "JMLH",
            total_kolom_blok["sat_reskrim"],
            total_kolom_blok["sat_narkoba"],
            total_kolom_blok["sat_lantas"],
            total_kolom_blok["sat_polair"],
            total_kolom_blok["titipan"],
            sum(total_kolom_blok.values()),
        ])

        isi.add_widget(
            self.buat_tabel(
                [
                    "BLOK", "RESKRIM", "NARKOBA",
                    "LANTAS", "POLAIR", "TITIPAN", "TOTAL",
                ],
                rows_blok,
            )
        )

        rows_polri = []
        total_kolom_polri = {key: 0 for key, _ in KASUS_FIELDS}

        for row_key, row_name in POLRI_ROWS:
            nilai = self.data["polri"]["tabel"][row_key]

            for key, _ in KASUS_FIELDS:
                total_kolom_polri[key] += nilai[key]

            rows_polri.append([
                row_name,
                nilai["krimum"],
                nilai["krimsus"],
                nilai["narkoba"],
                nilai["laka_lantas"],
                sum(nilai.values()),
            ])

        rows_polri.append([
            "JUMLAH",
            total_kolom_polri["krimum"],
            total_kolom_polri["krimsus"],
            total_kolom_polri["narkoba"],
            total_kolom_polri["laka_lantas"],
            sum(total_kolom_polri.values()),
        ])

        isi.add_widget(
            self.buat_tabel(
                [
                    "SAT FUNG", "KRIMUM", "KRIMSUS",
                    "NARKOBA", "LAKA", "JUMLAH",
                ],
                rows_polri,
            )
        )

        rows_titipan = []
        total_kolom_titipan = {key: 0 for key, _ in KASUS_FIELDS}

        for row_key, row_name in TITIPAN_ROWS:
            nilai = self.data["titipan"]["tabel"][row_key]

            for key, _ in KASUS_FIELDS:
                total_kolom_titipan[key] += nilai[key]

            rows_titipan.append([
                row_name,
                nilai["krimum"],
                nilai["krimsus"],
                nilai["narkoba"],
                nilai["laka_lantas"],
                sum(nilai.values()),
            ])

        rows_titipan.append([
            "JUMLAH",
            total_kolom_titipan["krimum"],
            total_kolom_titipan["krimsus"],
            total_kolom_titipan["narkoba"],
            total_kolom_titipan["laka_lantas"],
            sum(total_kolom_titipan.values()),
        ])

        isi.add_widget(
            self.buat_tabel(
                [
                    "TITIPAN", "KRIMUM", "KRIMSUS",
                    "NARKOBA", "LAKA", "JUMLAH",
                ],
                rows_titipan,
            )
        )

        tombol_png = Button(
            text="BUAT GAMBAR PNG",
            bold=True,
            font_size="14sp",
            size_hint=(1, None),
            height=dp(46),
            background_normal="",
            background_down="",
            background_color=warna["hijau"],
            color=(1, 1, 1, 1),
        )
        tombol_png.bind(on_press=lambda instance: self.buat_gambar("png"))
        isi.add_widget(tombol_png)

        tombol_jpg = Button(
            text="BUAT GAMBAR JPG",
            bold=True,
            font_size="14sp",
            size_hint=(1, None),
            height=dp(46),
            background_normal="",
            background_down="",
            background_color=warna["oranye"],
            color=(1, 1, 1, 1),
        )
        tombol_jpg.bind(on_press=lambda instance: self.buat_gambar("jpg"))
        isi.add_widget(tombol_jpg)

        return self.buat_scroll(isi)

    def buat_tabel(self, header, rows):
        warna = self.warna()

        tabel = GridLayout(
            cols=len(header),
            padding=dp(6),
            spacing=dp(3),
            size_hint=(1, None),
        )
        tabel.bind(minimum_height=tabel.setter("height"))

        for teks in header:
            tabel.add_widget(Label(
                text=teks,
                bold=True,
                font_size="10sp",
                color=warna["teks"],
                size_hint=(1, None),
                height=dp(24),
            ))

        for baris in rows:
            for teks in baris:
                tabel.add_widget(Label(
                    text=str(teks) if teks != 0 else "",
                    font_size="11sp",
                    color=warna["redup"],
                    size_hint=(1, None),
                    height=dp(26),
                ))

        return tabel

    def halaman_laporan(self):
        warna = self.warna()
        isi = self.buat_kolom()

        for key, nama in JABATAN_FIELDS:
            isi.add_widget(
                self.buat_label(nama, "13sp", True, warna["teks"])
            )

            input_jabatan = TextInput(
                text=self.data_laporan[key],
                multiline=False,
                font_size="14sp",
                size_hint=(1, None),
                height=dp(42),
                background_normal="",
                background_active="",
                background_color=warna["input"],
                foreground_color=warna["teks"],
                cursor_color=warna["biru"],
                padding=[dp(10), dp(10), dp(10), dp(10)],
            )

            input_jabatan.bind(
                text=lambda instance, teks, kunci=key: self.data_laporan.update(
                    {kunci: teks}
                )
            )

            isi.add_widget(input_jabatan)

        isi.add_widget(
            self.buat_label("TEKS LAPORAN", "15sp", True, warna["teks"])
        )

        kotak_laporan = Label(
            text=self.buat_teks_laporan(),
            font_size="12sp",
            color=warna["teks"],
            size_hint=(1, None),
            halign="left",
            valign="top",
        )

        kotak_laporan.bind(
            width=lambda instance, lebar: setattr(
                instance,
                "text_size",
                (lebar, None),
            )
        )

        kotak_laporan.bind(
            texture_size=lambda instance, ukuran: setattr(
                instance,
                "height",
                ukuran[1],
            )
        )

        isi.add_widget(kotak_laporan)

        tombol_perbarui = Button(
            text="PERBARUI TEKS",
            bold=True,
            font_size="14sp",
            size_hint=(1, None),
            height=dp(46),
            background_normal="",
            background_down="",
            background_color=warna["biru"],
            color=(1, 1, 1, 1),
        )
        tombol_perbarui.bind(
            on_press=lambda instance: self.perbarui_laporan(kotak_laporan)
        )
        isi.add_widget(tombol_perbarui)

        tombol_salina = Button(
            text="SALIN TEKS LAPORAN",
            bold=True,
            font_size="14sp",
            size_hint=(1, None),
            height=dp(46),
            background_normal="",
            background_down="",
            background_color=warna["hijau"],
            color=(1, 1, 1, 1),
        )
        tombol_salina.bind(
            on_press=lambda instance: self.salin_laporan()
        )
        isi.add_widget(tombol_salina)

        return self.buat_scroll(isi)

    def perbarui_laporan(self, kotak_laporan):
        kotak_laporan.text = self.buat_teks_laporan()

    def salin_laporan(self):
        Clipboard.copy(self.buat_teks_laporan())

    def buat_teks_laporan(self):
        data = self.data
        waktu = datetime.now()

        if waktu.hour < 12:
            salam = "Pagi"
        elif waktu.hour < 15:
            salam = "Siang"
        elif waktu.hour < 18:
            salam = "Sore"
        else:
            salam = "Malam"

        hari_inggris = waktu.strftime("%A")

        hari_indonesia = {
            "Monday": "Senin",
            "Tuesday": "Selasa",
            "Wednesday": "Rabu",
            "Thursday": "Kamis",
            "Friday": "Jumat",
            "Saturday": "Sabtu",
            "Sunday": "Minggu",
        }

        hari = hari_indonesia.get(hari_inggris, hari_inggris)
        tanggal = waktu.strftime("%d %B %Y")

        blok = data["blok"]

        jumlah_blok = [
            sum(blok[str(i)].values())
            for i in range(1, 15)
        ]

        total_blok = sum(jumlah_blok)

        polri = data["polri"]
        titipan = data["titipan"]

        total_polri = sum(
            sum(nilai.values())
            for nilai in polri["tabel"].values()
        )

        total_titipan = sum(
            sum(nilai.values())
            for nilai in titipan["tabel"].values()
        )

        total_reskrim = sum(polri["tabel"]["satreskrim"].values())
        total_narkoba = sum(polri["tabel"]["satnarkoba"].values())
        total_polair = sum(polri["tabel"]["satpolair"].values())
        total_lantas = sum(polri["tabel"]["satlantas"].values())

        titipan_polsek = sum(titipan["tabel"]["polsek"].values())
        titipan_kejaksaan = sum(titipan["tabel"]["jaksa"].values())
        titipan_pengadilan = sum(titipan["tabel"]["pengadilan"].values())
        titipan_kehutanan = sum(titipan["tabel"]["kehutanan"].values())

        laki_polri = polri["demo"]["laki"]
        perempuan_polri = polri["demo"]["prmpuan"]

        laki_titipan = titipan["demo"]["laki"]
        perempuan_titipan = titipan["demo"]["prmpuan"]

        total_laki = laki_polri + laki_titipan
        total_perempuan = perempuan_polri + perempuan_titipan

        dewasa = (
            laki_polri
            + perempuan_polri
            + laki_titipan
            + perempuan_titipan
        )

        anak = (
            polri["demo"]["anak_lk"]
            + polri["demo"]["anak_pr"]
            + titipan["demo"]["anak_lk"]
            + titipan["demo"]["anak_pr"]
        )

        teks = f"""*POLRES KUTAI KARTANEGARA*

Selamat {salam} Komandan mohon ijin melaporkan jumlah tahanan di Rutan Polres Kutai Kartanegara pada :

Hari  : {hari}
Tgl    : {tanggal}

Dengan rincian tahanan per blok:
1) Blok 1 = {jumlah_blok[0]} Orang
2) Blok 2 = {jumlah_blok[1]} Orang
3) Blok 3 = {jumlah_blok[2]} Orang
4) Blok 4 = {jumlah_blok[3]} Orang
5) Blok 5 = {jumlah_blok[4]} Orang
6) Blok 6 = {jumlah_blok[5]} Orang
7) Blok 7 = {jumlah_blok[6]} Orang
8) Blok 8 = {jumlah_blok[7]} Orang
9) Blok 9 = {jumlah_blok[8]} Orang
10) Blok 10 = {jumlah_blok[9]} Orang
11) Blok 11 = {jumlah_blok[10]} Orang
12) Blok 12 = {jumlah_blok[11]} Orang
13) Blok 13 = {jumlah_blok[12]} Orang
14) Blok Wanita = {jumlah_blok[13]} Orang

Dengan rincian :
Jumlah Tahanan keseluruhan : {total_blok} Orang
Laki- laki : {total_laki} orang
Perempuan : {total_perempuan} orang
Dewasa : {dewasa} orang
Anak-anak : {anak} orang

Tahanan Polres : {total_polri} orang, Dengan rincian : 
Tahanan Reskrim : {total_reskrim} orang 
Tahanan Narkoba : {total_narkoba} orang
Tahanan Polair : {total_polair} orang 
Tahanan Lantas : {total_lantas} orang

Tahanan Titipan : {total_titipan} orang, Dengan rincian :
Titipan polsek : {titipan_polsek} orang
Titipan Kejaksaan : {titipan_kejaksaan} orang
Titipan Pengadilan : {titipan_pengadilan} orang
Titipan Kehutanan : {titipan_kehutanan} orang

*1.* {self.data_laporan.get("jabatan_1", "")}
*2.* {self.data_laporan.get("jabatan_2", "")}
*3.* {self.data_laporan.get("jabatan_3", "")}
*4.* {self.data_laporan.get("jabatan_4", "")}


Situasi dalam keadaan aman dan tertib.
Demikian kami laporkan.
*DUM*
*Dokumentasi terlampir*"""

        return teks

    def buat_gambar(self, format_gambar):
        try:
            from PIL import Image, ImageDraw, ImageFont
        except ImportError:
            print("Install Pillow: pip install pillow")
            return

        lebar = 1300
        tinggi_baris = 50
        tinggi = 2300

        gambar = Image.new("RGB", (lebar, tinggi), "white")
        draw = ImageDraw.Draw(gambar)

        try:
            font_judul = ImageFont.truetype("arial.ttf", 34)
            font_isi = ImageFont.truetype("arial.ttf", 22)
        except OSError:
            font_judul = ImageFont.load_default()
            font_isi = ImageFont.load_default()

        y = 60
        draw.text(
            (lebar // 2, y),
            "JUMLAH TAHANAN",
            fill="black",
            font=font_judul,
            anchor="mm",
        )
        y += 80

        kolom_blok = [100, 280, 480, 680, 880, 1050, 1190]
        header_blok = [
            "BLOK", "RESKRIM", "NARKOBA",
            "LANTAS", "POLAIR", "TITIPAN", "TOTAL",
        ]

        for teks, x in zip(header_blok, kolom_blok):
            draw.text((x, y), teks, fill="black", font=font_isi, anchor="mm")

        y += tinggi_baris
        draw.line([(60, y), (lebar - 60, y)], fill="black", width=3)

        total_blok = {key: 0 for key, _ in BLOK_FIELDS}

        for nomor in range(1, 15):
            y += tinggi_baris
            nilai = self.data["blok"][str(nomor)]

            draw.text(
                (kolom_blok[0], y),
                str(nomor),
                fill="black",
                font=font_isi,
                anchor="mm",
            )

            for indeks, (key, _) in enumerate(BLOK_FIELDS, start=1):
                total_blok[key] += nilai[key]
                teks = str(nilai[key]) if nilai[key] > 0 else ""
                draw.text(
                    (kolom_blok[indeks], y),
                    teks,
                    fill="black",
                    font=font_isi,
                    anchor="mm",
                )

            jumlah = sum(nilai.values())
            draw.text(
                (kolom_blok[6], y),
                str(jumlah) if jumlah > 0 else "",
                fill="black",
                font=font_isi,
                anchor="mm",
            )

        y += tinggi_baris
        draw.line([(60, y), (lebar - 60, y)], fill="black", width=3)
        y += tinggi_baris

        draw.text(
            (kolom_blok[0], y),
            "JMLH",
            fill="black",
            font=font_isi,
            anchor="mm",
        )

        for indeks, (key, _) in enumerate(BLOK_FIELDS, start=1):
            draw.text(
                (kolom_blok[indeks], y),
                str(total_blok[key]),
                fill="black",
                font=font_isi,
                anchor="mm",
            )

        draw.text(
            (kolom_blok[6], y),
            str(sum(total_blok.values())),
            fill="black",
            font=font_isi,
            anchor="mm",
        )

        waktu = datetime.now().strftime("%Y%m%d_%H%M%S")
        nama_file = f"rekap_tahanan_{waktu}.{format_gambar}"

        if format_gambar in ("jpg", "jpeg"):
            gambar.save(nama_file, "JPEG", quality=95)
        else:
            gambar.save(nama_file, "PNG")

        print(f"Gambar tersimpan: {nama_file}")


if __name__ == "__main__":
    TahananApp().run()
# Sistem Informasi Data Toko Mabel Cycle (Python PyQt5 + MySQL)

Project mata kuliah Database Management System (Kelompok 2). Aplikasi desktop berbasis GUI untuk admin toko mabel Cycle, digunakan untuk mengelola data produk, produsen, dan transaksi penjualan yang tersimpan di database MySQL.

## Fitur

- **Welcome screen**, **Sign Up**, dan **Login** untuk produsen
- **Pengelolaan stok produk**: tambah produk baru, tambah stok produk yang sudah ada, dan hapus produk
- **Pencarian produk** berdasarkan ID produk (nama dan harga tampil otomatis)
- **Transaksi penjualan**: hitung total, uang bayar, dan kembalian, lalu simpan ke tabel transaksi
- **Tabel stok** yang diperbarui langsung dari database

## Teknologi

- Python 3
- PyQt5 (antarmuka GUI, dirancang dengan Qt Designer)
- MySQL dan `mysql-connector-python`

## Struktur File

| File | Keterangan |
|---|---|
| `main.py` | Program utama (logika aplikasi dan koneksi database) |
| `welcomescreen.ui`, `Login.ui`, `SignUp.ui`, `MenuAdmin.ui`, `Struk.ui` | Desain tampilan dari Qt Designer |
| `Login.py`, `SignUp.py`, `MenuAdmin.py` | Kode tampilan hasil konversi dari file `.ui` |
| `res.qrc`, `res.py`, `tes.qrc`, `tes.py` | Resource gambar beserta hasil kompilasinya |
| `cycle_prime.sql` | Struktur database `cycle_prime` |
| `dokumentasi/` | ERD database |

## Cara Menjalankan

1. Install Python 3 dan MySQL Server.
2. Buat database dengan menjalankan `cycle_prime.sql` di MySQL Workbench.
3. Install library:
   ```
   pip install -r requirements.txt
   ```
4. Jalankan program:
   ```
   python main.py
   ```

Secara bawaan program terhubung ke MySQL di `localhost` dengan user `root` tanpa password dan database `cycle_prime`. Jika pengaturan MySQL kamu berbeda, ubah bagian `mysql.connector.connect(...)` pada method `lakukanKoneksi` di `main.py`.

## Anggota Kelompok

- Akbar Haqi Nasrullah
- Aqil Miftahul Fath
- Nadziah Fitriani
- Nur Hasanah Perangin Angin
- Ramadhani

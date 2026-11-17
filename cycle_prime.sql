-- Struktur database untuk aplikasi Sistem Informasi Toko Mabel Cycle.
-- CATATAN: file ini dibuat ulang dari kode program (main.py). Jika kamu punya
-- hasil export database asli dari MySQL Workbench, pakai file itu sebagai gantinya.

CREATE DATABASE IF NOT EXISTS cycle_prime;

USE cycle_prime;

CREATE TABLE IF NOT EXISTS Produsen (
  id_produsen   VARCHAR(20)  NOT NULL,
  nama_produsen VARCHAR(50)  NOT NULL,
  alamat        VARCHAR(200) NOT NULL,
  no_hp         VARCHAR(15)  NOT NULL,
  Password      VARCHAR(50)  NOT NULL,
  PRIMARY KEY (id_produsen)
);

CREATE TABLE IF NOT EXISTS Produk (
  id_produk    VARCHAR(10) NOT NULL,
  nama_produk  VARCHAR(50) NOT NULL,
  jenis_barang VARCHAR(30) NOT NULL,
  stok         INT         NOT NULL,
  harga        INT         NOT NULL,
  nama_agen    VARCHAR(50) NOT NULL,
  PRIMARY KEY (id_produk)
);

CREATE TABLE IF NOT EXISTS Transaksi (
  kd_pembelian    INT         NOT NULL AUTO_INCREMENT,
  nama_pembeli    VARCHAR(50) NOT NULL,
  tanggal         DATETIME    NOT NULL,
  id_produk       VARCHAR(10) NOT NULL,
  nama_barang     VARCHAR(50) NOT NULL,
  jumlah_barang   INT         NOT NULL,
  harga_barang    INT         NOT NULL,
  total_transaksi VARCHAR(20) NOT NULL,
  cash            VARCHAR(20) NOT NULL,
  kembalian       VARCHAR(20) NOT NULL,
  PRIMARY KEY (kd_pembelian)
);

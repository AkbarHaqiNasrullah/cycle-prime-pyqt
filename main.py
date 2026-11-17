import mysql.connector, sys, os
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QMessageBox, QTableWidgetItem, QDateTimeEdit, QVBoxLayout, QLabel, QWidget
from PyQt5.QtCore import QTimer, QDateTime
from PyQt5.QtGui import QFont
from mysql.connector import Error
from tes import* 

# Pastikan file .ui dibaca dari folder yang sama dengan main.py
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi("welcomescreen.ui", self)
        self.wlogin.clicked.connect(self.gotologin)
        self.wsignup.clicked.connect(self.gotosignup)

    def gotologin(self):
        login = LoginScreen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotosignup(self):
        signup = SignUpScreen()
        widget.addWidget(signup)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class LoginScreen(QDialog):
    def __init__(self):
        super(LoginScreen, self).__init__()
        loadUi("Login.ui", self)
        self.login.clicked.connect(self.CariData)
        self.kembali.clicked.connect(self.gotowelcome)

    def lakukanKoneksi(self):
        koneksi = mysql.connector.connect(host='localhost', user='root', database='cycle_prime')
        cur = koneksi.cursor()
        return cur, koneksi

    def CariData(self):
        statemenSQL = "SELECT id_produsen, Password FROM Produsen WHERE id_produsen = %s AND Password = %s"
        cur = None
        koneksi = None
        try:
            cur, koneksi = self.lakukanKoneksi()
            cur.execute(statemenSQL, (self.leID.text(), self.lePasspro.text()))
            data = cur.fetchone()
            if data is None:
                QMessageBox.critical(self, "Error", "Maaf, ID atau Password salah")
            else:
                self.gotomenu()
        except Error as e:
            QMessageBox.critical(self, "Error", "Error saat mengakses Data")
        finally:
            if koneksi is not None:
                koneksi.close()
            
    def gotomenu(self):
        menu = Menu()
        widget.addWidget(menu)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        
    def gotowelcome(self):
        welcome = WelcomeScreen()
        widget.addWidget(welcome)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class SignUpScreen(QDialog):
    def __init__(self):
        super(SignUpScreen, self).__init__()
        loadUi("SignUp.ui", self)
        self.SignIn.clicked.connect(self.BuatData)
        self.kembali.clicked.connect(self.gotowelcome)
        
    def lakukanKoneksi(self):
        koneksi = mysql.connector.connect(host='localhost', user='root', database='cycle_prime')
        cur = koneksi.cursor()
        return cur, koneksi

    def BuatData(self):
        id_produsen = self.leIDpro.text()
        nama_produsen = self.leNamaPro.text()
        alamat = self.leAlamat.text()
        no_hp = self.leHP.text()
        password = self.lePassPro.text()

        statemenSQL = "INSERT INTO Produsen (id_produsen, nama_produsen, alamat, no_hp, Password) VALUES (%s, %s, %s, %s, %s)"
        data = (id_produsen, nama_produsen, alamat, no_hp, password)
        
        cur = None
        koneksi = None
        try:
            cur, koneksi = self.lakukanKoneksi()
            cur.execute(statemenSQL, data)
            koneksi.commit()
            QMessageBox.information(self, "Sign In", "Data Telah dimasukkan")
            self.gotologin()
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error", "Error saat mengakses Data")
        finally:
            if cur is not None:
                cur.close()
            if koneksi is not None:
                koneksi.close()
            
    def gotologin(self):
        login = LoginScreen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    
    def gotowelcome(self):
        welcome = WelcomeScreen()
        widget.addWidget(welcome)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class Menu(QDialog):
    def __init__(self):
        super(Menu, self).__init__()
        loadUi("MenuAdmin.ui", self)
        self.pbUpdateStok.clicked.connect(self.UpdateDataStok)
        self.pbOK.clicked.connect(self.CariProduk)
        self.sbJumlah.valueChanged.connect(self.Hitung)
        self.pbBayar.clicked.connect(self.Total)
        self.sbJumlah.editingFinished.connect(self.JualProduk)
        self.pbHapusStok.clicked.connect(self.HapusDataStok)
        self.kembali.clicked.connect(self.gotowelcome)
        self.labelPaid.hide()
        self.labelChange.hide()
        self.labelRP_2.hide()
        self.labelRP_3.hide()
        self.membayar.hide()
        self.kembalian.hide()
        self.TampilTabel()
        self.UpdateTabelStok()
        self.UpdateDayTime()

    def lakukanKoneksi(self):
        koneksi = mysql.connector.connect(host='localhost', user='root', database='cycle_prime')
        cur = koneksi.cursor()
        return cur, koneksi
    
    def CariProduk(self):
        statemenSQL = "SELECT nama_produk, harga FROM produk WHERE id_produk = %s"
        cur = None
        koneksi = None
        try:
            cur, koneksi = self.lakukanKoneksi()
            cur.execute(statemenSQL, (self.id_trans.text(),))
            baris = cur.fetchone()
            if baris is None:
                QMessageBox.critical(self, "Error", "Tidak ditemukan Nama dan harga barang dengan Id Produk ini")
                self.leNamaBarang.clear()
                self.leHarga.clear()
            else:
                self.leNamaBarang.setText(str(baris[0]))
                self.leHarga.setText(str(baris[1]))
                self.Hitung()
        except Error as e:
            QMessageBox.critical(self, "Error", "Error mengakses Tabel Produk")
        finally:
            if koneksi is not None:
                koneksi.close()

    def Hitung(self):
        if len(self.leHarga.text()) != 0:
            hargaTotalBeli = int(self.leHarga.text())
        else:
            hargaTotalBeli = 0
        Jumlah = self.sbJumlah.value()
        hargaTotalAwal = Jumlah * hargaTotalBeli
        self.menghitung.setText(str(hargaTotalAwal))
        if Jumlah == 0:
            self.labelPaid.hide()
            self.labelChange.hide()
            self.labelRP_2.hide()
            self.labelRP_3.hide()
            self.membayar.hide()
            self.kembalian.hide()
        else:
            self.labelPaid.show()
            self.labelChange.show()
            self.labelRP_2.show()
            self.labelRP_3.show()
            self.membayar.show()
            self.kembalian.show()
            self.membayar.clear()
            self.kembalian.clear()

    def Total(self):
        if len(self.membayar.text()) !=0:
            bayar=int(self.membayar.text())
        else:
            bayar=0
        hargaTotalAwal=int(self.menghitung.text())
        hargaTotalAkhir=bayar-hargaTotalAwal
        if hargaTotalAkhir > 0:
            self.kembalian.setText(str (hargaTotalAkhir))
            self.Transaksi()
        else:
            self.membayar.clear()
            self.kembalian.clear()
            QMessageBox.critical(self, "Error", "Uang yang anda kasih kurang")

    def JualProduk(self):
        product = self.id_trans.text()
        jumlah = int(self.sbJumlah.value())
        
        cur, koneksi = self.lakukanKoneksi()
        query = "SELECT stok FROM produk WHERE id_produk = %s"
        cur.execute(query, (product,))
        result = cur.fetchone()
        
        if result:
            stok = result[0]
            if stok >= jumlah:
                stokBaru = stok - jumlah
                update_query = "UPDATE produk SET stok = %s WHERE id_produk = %s"
                cur.execute(update_query, (stokBaru, product))
                koneksi.commit()
                self.TampilTabel()
            else:
                QMessageBox.warning(self, "Error", "Stok Tidak Mencukupi")
        else:
            QMessageBox.warning(self, "Error", "Product not found!")
        
        koneksi.close()         

    def TampilTanggal(self):
        self.dtNOW = QDateTimeEdit()
        self.dtNOW.setDateTime(QDateTime.currentDateTime())
        self.dtNOW.setDisplayFormat("dd/MM/yyyy hh:mm:ss")

        timer = QTimer(self)
        timer.timeout.connect(self.UpdateDayTime)
        timer.start(1000)  # Update setiap 1 detik

    def UpdateDayTime(self):
        self.dtNOW.setDateTime(QDateTime.currentDateTime())

    def Transaksi(self):
        nama_pembeli = self.leNama.text()
        tanggal = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
        id_produk = self.id_trans.text()
        nama_barang = self.leNamaBarang.text()
        jumlah_barang = int(self.sbJumlah.value())
        harga_barang = self.leHarga.text()
        total_transaksi = "Rp. " + self.menghitung.text()
        cash = "Rp. " + self.membayar.text()
        kembalian = "Rp. " + self.kembalian.text()

        statemenSQL = "INSERT INTO Transaksi (nama_pembeli, tanggal, id_produk, nama_barang, jumlah_barang, harga_barang, total_transaksi, cash, kembalian) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        data = (nama_pembeli, tanggal, id_produk, nama_barang, jumlah_barang, harga_barang, total_transaksi, cash, kembalian)

        cur = None
        koneksi = None
        try:
            cur, koneksi = self.lakukanKoneksi()
            cur.execute(statemenSQL, data)
            koneksi.commit()
            QMessageBox.information(self, "Insert Data", "Data Telah dimasukkan")
            #self.gotostruk()
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error", "Error saat mengakses Data")
        finally:
            if cur is not None:
                cur.close()
            if koneksi is not None:
                koneksi.close()
    
    def TampilTabel(self):
        statemenSQL = "SELECT * FROM Produk"
        cur = None
        koneksi = None
        try:
            cur, koneksi = self.lakukanKoneksi()
            cur.execute(statemenSQL)
            result = cur.fetchall()
            self.tbl_stok.clearContents()
            self.tbl_stok.setRowCount(0)
            for row_number, row_data in enumerate(result):
                self.tbl_stok.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    item = QTableWidgetItem(str(data))
                    self.tbl_stok.setItem(row_number, column_number, item)
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error", "Error saat mengakses Tabel")
        finally:
            if koneksi is not None:
                koneksi.close()

    def UpdateDataStok(self):
        id_produk = self.id_product.text()
        nama_produk = self.nama_product.text()
        jenis_barang = self.jenis_barang.text()
        stok = int(self.stok.text())
        harga = self.harga.text()
        penyuplai = self.penyuplai.text()

        statemenSQL = "INSERT INTO Produk (id_produk, nama_produk, jenis_barang, stok, harga, nama_agen) VALUES (%s, %s, %s, %s, %s, %s)"
        data = (id_produk, nama_produk, jenis_barang, stok, harga, penyuplai)

        cur = None
        koneksi = None
        try:
            cur, koneksi = self.lakukanKoneksi()
            cur.execute("SELECT * FROM Produk WHERE id_produk=%s", (id_produk,))
            result = cur.fetchone()
            if result is None:
                cur.execute(statemenSQL, data)
                koneksi.commit()
                QMessageBox.information(self, "Insert Data", "Data Telah dimasukkan")
                self.id_product.clear()
                self.nama_product.clear()
                self.jenis_barang.clear()
                self.stok.clear()
                self.harga.clear()
                self.penyuplai.clear()
                self.UpdateTabelStok()
                self.TampilTabel()
            else:
                stokBaru = result[3] + stok
                cur.execute("UPDATE Produk SET stok=%s WHERE id_produk=%s", (stokBaru, id_produk))
                koneksi.commit()
                QMessageBox.information(self, "Update Data", "Update Data Stok Telah diperbarui")
                self.id_product.clear()
                self.nama_product.clear()
                self.jenis_barang.clear()
                self.stok.clear()
                self.harga.clear()
                self.penyuplai.clear()
                self.UpdateTabelStok()
                self.TampilTabel()
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error", "Error saat mengakses Data")
        finally:
            if cur is not None:
                cur.close()
            if koneksi is not None:
                koneksi.close()
            
    def HapusDataStok(self):
        id_produk = self.id_product.text()
        statemenSQL = "DELETE FROM Produk WHERE id_produk=%s"

        cur = None
        koneksi = None
        try:
            cur, koneksi = self.lakukanKoneksi()
            cur.execute("SELECT * FROM Produk WHERE id_produk=%s", (id_produk,))
            result = cur.fetchone()
            if result is None:
                QMessageBox.warning(self, "Error", "Data Id Produk Tidak ditemukan")
                self.id_product.clear()
                self.UpdateTabelStok()
            else:
                cur.execute(statemenSQL, (id_produk,))
                koneksi.commit()
                QMessageBox.information(self, "DELETE Data", "Data Telah dihapuskan")
                self.id_product.clear()
                self.UpdateTabelStok()
                self.TampilTabel()
                QMessageBox.information(self, "Update Data", "Update Data Stok Telah diperbarui")
                self.id_product.clear()
                self.UpdateTabelStok()
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error", "Error saat mengakses Data")
        finally:
            if koneksi is not None:
                koneksi.close()

    
    def UpdateTabelStok(self):
        statemenSQL = "SELECT * FROM Produk"
        cur = None
        koneksi = None
        try:
            cur, koneksi = self.lakukanKoneksi()
            cur.execute(statemenSQL)
            result = cur.fetchall()
            self.table_update.clearContents()
            self.table_update.setRowCount(0)
            for row_number, row_data in enumerate(result):
                self.table_update.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    item = QTableWidgetItem(str(data))
                    self.table_update.setItem(row_number, column_number, item)
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error", "Error saat mengakses Tabel")
        finally:
            if koneksi is not None:
                koneksi.close()
            
    def gotostruk(self):
        struk = StrukPembayaran()
        widget.addWidget(struk)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    
    def gotowelcome(self):
        welcome = WelcomeScreen()
        widget.addWidget(welcome)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        
class StrukPembayaran(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Struk Pembayaran')
        self.setGeometry(100, 100, 400, 500)
        self.layout = QVBoxLayout()

        self.label = QLabel()
        self.label.setFont(QFont('Times New Roman', 16))
        self.layout.addWidget(self.label)

        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

        self.load_data()
        
    def lakukanKoneksi(self):
        koneksi = mysql.connector.connect(host='localhost', user='root', database='cycle_prime')
        cur = koneksi.cursor()
        return cur, koneksi
    
    def load_data(self):
        cur = None
        koneksi = None
        try:
            cur, koneksi = self.lakukanKoneksi()
            # Mengambil data dari tabel Transaksi
            query = "SELECT * FROM Transaksi"
            cur.execute(query)
            results = cur.fetchall()

            # Membuat struk pembayaran dari data yang diambil
            struk = ""
            for row in results:
                kd_pembelian = row[0]
                nama_pembeli = row[1]
                tanggal = row[2]
                id_produk = row[3]
                nama_barang = row[4]
                harga_barang = row[5]
                jumlah_barang = row[6]
                total_transaksi = row[7]
                cash = row[8]
                kembalian = row[9]

                struk += "=======================================\n"
                struk += f"Kode Pembelian: {kd_pembelian}\n"
                struk += f"Nama Pembeli: {nama_pembeli}\n"
                struk += f"Tanggal: {tanggal}\n"
                struk += "---------------------------------------\n"
                struk += f"ID Produk: {id_produk}\n"
                struk += f"Nama Barang: {nama_barang}\n"
                struk += f"Harga Barang: {harga_barang}\n"
                struk += f"Jumlah Barang: {jumlah_barang}\n"
                struk += "---------------------------------------\n"
                struk += f"Total Transaksi: {total_transaksi}\n"
                struk += f"Cash: {cash}\n"
                struk += f"Kembalian: {kembalian}\n"
                struk += "=======================================\n\n"

            self.label.setText(struk)
            self.show()
            if koneksi is not None:
                koneksi.close()

        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error", "Error saat mengakses Data")


# Main
app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
welcome = WelcomeScreen()
widget.addWidget(welcome)
widget.setFixedHeight(720)
widget.setFixedWidth(1280)
widget.show()
sys.exit(app.exec_())
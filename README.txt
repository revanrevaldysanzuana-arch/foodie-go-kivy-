FOODIE GO — Python + Kivy
Created by Revan

ISI PAKET
- main.py: kode aplikasi Python/Kivy.
- buildozer.spec: konfigurasi untuk membuat APK Android.
- requirements.txt: dependensi untuk menjalankan di komputer.

FITUR
- 18 menu makanan/minuman.
- Cari menu dan filter kategori.
- Menu favorit.
- Keranjang dengan tambah/kurangi kuantitas.
- Perhitungan subtotal, biaya layanan demo Rp2.000, dan total.
- Form checkout dengan nama, nomor HP, alamat, pilihan pembayaran demo, dan catatan.
- Ringkasan pesanan, tombol salin, dan file teks yang disimpan pada folder data aplikasi.
- Riwayat pesanan selama aplikasi berjalan.
- Tampilan scroll responsif untuk HP, dan 2/3 kolom berdasarkan lebar jendela.
- Branding "Created by Revan".

CARA COBA DI KOMPUTER
1. Instal Python 3.
2. Jalankan: pip install kivy
3. Masuk folder paket dan jalankan: python main.py

CARA MEMBANGUN APK ANDROID
Buildozer umumnya paling cocok dijalankan di Linux (misalnya Ubuntu/WSL atau mesin Linux), bukan langsung di Android.
1. Siapkan Python, Java JDK, Buildozer, dan dependensi Android sesuai dokumentasi Buildozer.
2. Di folder yang berisi buildozer.spec, jalankan: buildozer android debug
3. Setelah berhasil, APK biasanya berada di folder bin/.
4. Pindahkan APK ke HP Android dan instal. Android mungkin meminta izin instal aplikasi dari sumber tersebut.

CATATAN PENTING
- ZIP ini berisi source code Python/Kivy dan konfigurasi, BUKAN APK yang sudah jadi.
- Checkout, COD, transfer, dan QRIS hanya simulasi. Tidak ada server, restoran, kurir, atau transaksi nyata.
- Data riwayat hanya tersimpan selama aplikasi terbuka. File ringkasan disimpan ke folder data aplikasi.
- Build APK pertama dapat lama dan cukup berat; sebaiknya jangan menjalankan kompilasi berat di browser HP.


CLOUD BUILD DENGAN GITHUB ACTIONS (TIDAK BUILD DI HP)
1. Di browser, buka https://github.com dan masuk/daftar akun.
2. Buat repository baru bernama foodie-go-kivy. Pilih Public agar pemakaian Actions lebih mudah untuk repo baru; jangan unggah password, API key, atau data pribadi.
3. Ekstrak ZIP ini. Pastikan file main.py, buildozer.spec, requirements.txt, dan folder tersembunyi .github/workflows/build-apk.yml ada.
4. Di halaman repo, pilih Add file > Upload files. Unggah main.py, buildozer.spec, requirements.txt, README.txt, dan folder .github beserta isinya. Jika browser HP tidak bisa mengunggah folder .github, buat folder/file lewat Add file > Create new file dengan nama persis .github/workflows/build-apk.yml lalu tempel isi workflow yang ada di paket.
5. Commit perubahan ke branch main.
6. Buka tab Actions di repository, pilih "Build FOODIE GO APK", tekan Run workflow bila diperlukan.
7. Tunggu workflow selesai. Buka run yang berstatus hijau, cari bagian Artifacts, lalu unduh FOODIE-GO-APK. Ekstrak ZIP artifact untuk mendapatkan file .apk.
8. Buka APK di Android untuk menginstal. Android mungkin meminta izin "Install unknown apps" untuk browser/file manager.

CATATAN
- GitHub Actions menjalankan build di cloud; proses kompilasi tidak berlangsung di HP. Build pertama dapat cukup lama dan bisa gagal jika dependency upstream berubah.
- File APK diunduh sebagai artifact ZIP bernama FOODIE-GO-APK, bukan langsung dari repo.
- Ini debug APK untuk uji coba, bukan release APK untuk Play Store.
- Checkout dan metode pembayaran tetap simulasi.

# Sistem Monitoring Kehadiran Dosen (PresensiDosenPro)

Aplikasi berbasis web & automasi laporan untuk monitoring kehadiran dosen dengan dukungan input file **Spreadsheet / Excel / CSV** dan keluaran berkas cetak **PDF profesional & bersih (clean layout)**.

---

## 🎯 Fitur Utama

1. **Upload Spreadsheet & Excel Otomatis**:
   - Mendukung format `.xlsx`, `.xls`, dan `.csv`.
   - Menggunakan parser otomatis yang membaca kolom: `No`, `Grup`, `Kode MK dan Kelas`, `Tanggal`, `Nama Mata Kuliah`, `SKS`, `Jadwal`, `Ruangan`, `Pengajar`, `Presensi`, `Datang`, `Kembali`, `Terlambat`, `Komentar`, `Ganti Jadwal`.
   - Dapat mengedit status kehadiran atau jam hadir langsung dari antarmuka web.

2. **Dashboard Pemantauan & Analitik Interaktif**:
   - **Kartu Ringkasan Real-Time**: Total Sesi, Sesi Terlaksana, Hadir Tepat Waktu, Terlambat, Alpha, dan Jadwal Mendatang.
   - **Tingkat Persentase Kehadiran**: Penghitungan otomatis rasio kehadiran terhadap sesi terlaksana.
   - **Filter Multi-Kriteria**:
     - **Per Dosen**: Memilih dan memantau kinerja per individu dosen.
     - **Per Bulan**: Memilih periode bulan perkuliahan (September 2026, Oktober 2026, dst.).
     - **Program Studi**: Teknik Informatika (TI & PU 7201) dan Teknik Lingkungan (TL).
     - **Jenis Kelas**: Kelas Pagi Reguler (Romawi), Kelas Sore Karyawan (Angka), Mahasiswa Khusus PDAM Depok.
   - **Kelola & Hapus Data per Dosen**:
     - Tersedia tombol **"Hapus per Dosen"** di header dan ikon tempat sampah di samping filter dosen.
     - Modal interaktif menampilkan nama dosen, jumlah sesi yang akan dihapus, serta daftar mata kuliah yang diampu sebelum konfirmasi penghapusan permanen dari browser.
     - Tombol hapus satuan di setiap baris tabel.

3. **Ekspor Berkas PDF Desain Bersih & Profesional**:
   - **One-Click PDF Export**: Menggunakan library `html2pdf.js` untuk langsung mengunduh file `.pdf`.
   - **Standar Format Cetak Resmi**: Dilengkapi dengan Kop Fakultas/Institusi Resmi, Metadata Dosen (NIDN, Fakultas, Semester), Ringkasan Eksekutif KPI, Tabel Realisasi per Mata Kuliah, Tabel Log Presensi, serta Lembar Tanda Tangan Pengesahan Ketua Program Studi / Dekan.
   - Siap cetak langsung dalam ukuran standar **A4**.

---

## 📂 Struktur Berkas

- [index.html](file:///c:/Users/USER/Documents/agi-proj/index.html) : Aplikasi web mandiri (dashboard + parser Excel/CSV + exporter PDF). Cukup buka langsung di browser Chrome/Edge/Firefox.
- [sample_presensi.csv](file:///c:/Users/USER/Documents/agi-proj/sample_presensi.csv) : Salinan data CSV 128 baris presensi dosen (Mega Wahyu Rhamadani, S.T., M.M.S.I).
- [generate_pdf.py](file:///c:/Users/USER/Documents/agi-proj/generate_pdf.py) : Script generator laporan HTML/PDF jika ingin diintegrasikan dengan backend Python.

---

## 🚀 Cara Menjalankan

### Cara 1: Menggunakan Antarmuka Web (Paling Mudah)
1. Buka file [index.html](file:///c:/Users/USER/Documents/agi-proj/index.html) dengan klik ganda atau buka lewat Google Chrome / Microsoft Edge.
2. Data sampel presensi sudah otomatis termuat secara lengkap.
3. Untuk memperbarui data:
   - Klik tombol **"Upload Excel / CSV"** atau drag-and-drop berkas baru Anda.
   - Atau klik icon pensil di baris tabel untuk mengubah status presensi (misal mengubah jam datang atau status Alpha/Hadir).
4. Untuk menghasilkan PDF:
   - Klik tombol biru **"Cetak / Ekspor PDF"** di pojok kanan atas.
   - Dokumen PDF rapi dan bersih akan otomatis terunduh atau siap dicetak langsung (Save as PDF).

### Cara 2: Menjalankan Generator Python
Jalankan perintah berikut di terminal:
```bash
python generate_pdf.py
```
Script akan menghasilkan file `laporan_monitoring_presensi.html` yang siap dibuka dan disimpan sebagai PDF via browser.

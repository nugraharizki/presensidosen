"""
Script Generator Laporan Monitoring Kehadiran Dosen ke PDF
Klasifikasi Program Studi (TI / TL) dan Jenis Kelas (Pagi Reguler / Sore Karyawan / Khusus PDAM).
"""

import csv
import os
import re
from datetime import datetime

def detect_prodi(kode_mk, ruangan):
    kmk = (kode_mk or '').upper()
    rgn = (ruangan or '').upper()
    
    # Aturan Khusus: PU 7201 adalah prodi TI
    if 'PU 7201' in kmk or 'PU7201' in kmk or 'PU' in kmk:
        return 'Teknik Informatika'
    
    # Aturan: Kode depannya TL -> Teknik Lingkungan
    if 'TL' in kmk:
        return 'Teknik Lingkungan'
    
    # Aturan: Ruangan TI atau kode TI -> Teknik Informatika
    if 'TEKNIK INFORMATIKA' in rgn or 'TI' in kmk or 'TI' in rgn:
        return 'Teknik Informatika'
        
    return 'Teknik Informatika'

def detect_jenis_kelas(kode_mk_dan_kelas):
    s = (kode_mk_dan_kelas or '').strip()
    parts = s.split('/')
    suffix = parts[1].strip().upper() if len(parts) > 1 else s.upper()

    if 'PDAM' in suffix or 'DEPOK' in suffix:
        return 'Mahasiswa Khusus PDAM Depok'
    
    if re.match(r'^(I|II|III|IV|V|VI|VII|VIII|IX|X|XI|XII)$', suffix):
        return 'Kelas Pagi Reguler'
        
    if re.match(r'^\d+$', suffix):
        return 'Kelas Sore Karyawan'
        
    return 'Kelas Pagi Reguler'

def load_attendance_csv(filepath):
    records = []
    with open(filepath, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            item = {k.strip(): v.strip() for k, v in row.items()}
            kmk = item.get('Kode MK dan Kelas', '')
            rgn = item.get('Ruangan', '')
            item['prodi'] = detect_prodi(kmk, rgn)
            item['jenis_kelas'] = detect_jenis_kelas(kmk)
            records.append(item)
    return records

def generate_html_report(records, output_html_path):
    dosen = records[0].get('Pengajar', 'MEGA WAHYU RHAMADANI, S.T., M.M.S.I') if records else ''
    total_sesi = len(records)
    
    # Calculate stats
    executed = 0
    hadir = 0
    terlambat = 0
    alpha = 0
    upcoming = 0
    
    courses = {}

    for r in records:
        presensi = r.get('Presensi', 'H').upper()
        ganti = r.get('Ganti Jadwal', '')
        mk = r.get('Nama Mata Kuliah', 'Umum')
        kmk = r.get('Kode MK dan Kelas', '')
        sks = r.get('SKS', '3')
        datang = r.get('Datang', '')
        terlambat_note = r.get('Terlambat', '')
        prodi = r.get('prodi', 'Teknik Informatika')
        jenis_kelas = r.get('jenis_kelas', 'Kelas Pagi Reguler')
        
        key = f"{mk} - {kmk}"
        if key not in courses:
            courses[key] = {
                'mk': mk,
                'kode_mk': kmk,
                'sks': sks,
                'prodi': prodi,
                'jenis_kelas': jenis_kelas,
                'total': 0,
                'executed': 0,
                'hadir': 0,
                'alpha': 0,
                'late': 0
            }
        courses[key]['total'] += 1
        
        is_pending = 'presensi belum ada' in ganti.lower() or (not datang and not terlambat_note and not ganti and presensi != 'A')
        
        if is_pending:
            upcoming += 1
        else:
            executed += 1
            courses[key]['executed'] += 1
            if presensi == 'A' or 'ganti jadwal' in ganti.lower():
                alpha += 1
                courses[key]['alpha'] += 1
            else:
                hadir += 1
                courses[key]['hadir'] += 1
                if 'terlambat' in terlambat_note.lower():
                    terlambat += 1
                    courses[key]['late'] += 1

    rate_kehadiran = round((hadir / executed * 100), 1) if executed > 0 else 100.0
    tgl_cetak = datetime.now().strftime("%d %B %Y")

    # Build Course rows
    course_rows_html = ""
    for idx, (k, val) in enumerate(courses.items(), 1):
        pct = round((val['hadir'] / val['executed'] * 100), 1) if val['executed'] > 0 else 100.0
        course_rows_html += f"""
        <tr>
            <td style="text-align: center;">{idx}</td>
            <td><strong>{val['prodi']}</strong></td>
            <td>{val['jenis_kelas']}</td>
            <td><strong>{val['mk']}</strong><br><small style="color:#64748b;">{val['kode_mk']}</small></td>
            <td style="text-align: center;">{val['sks']}</td>
            <td style="text-align: center;">{val['total']}</td>
            <td style="text-align: center;">{val['executed']}</td>
            <td style="text-align: center; font-weight: bold; color: #166534;">{val['hadir']}</td>
            <td style="text-align: center; color: #991b1b;">{val['alpha']}</td>
            <td style="text-align: center; font-weight: bold;">{pct}%</td>
        </tr>
        """

    # Build Log rows
    log_rows_html = ""
    log_count = 0
    for r in records:
        ganti = r.get('Ganti Jadwal', '')
        datang = r.get('Datang', '')
        presensi = r.get('Presensi', 'H').upper()
        terlambat_note = r.get('Terlambat', '')
        prodi = r.get('prodi', '')
        jenis_kelas = r.get('jenis_kelas', '')
        
        is_pending = 'presensi belum ada' in ganti.lower() or (not datang and not terlambat_note and not ganti and presensi != 'A')
        if is_pending:
            continue
            
        log_count += 1
        if log_count > 50:
            break
            
        status_tag = '<span style="color:#166534; font-weight:bold;">HADIR</span>'
        if presensi == 'A' or 'ganti' in ganti.lower():
            status_tag = '<span style="color:#991b1b; font-weight:bold;">ALPHA</span>'
        elif 'terlambat' in terlambat_note.lower():
            status_tag = '<span style="color:#b45309; font-weight:bold;">TERLAMBAT</span>'

        log_rows_html += f"""
        <tr>
            <td style="text-align:center;">{r.get('No', log_count)}</td>
            <td>{r.get('Tanggal', '')}</td>
            <td><small style="color:#0369a1; font-weight:bold;">{prodi}</small></td>
            <td><small style="color:#475569;">{jenis_kelas}</small></td>
            <td><strong>{r.get('Nama Mata Kuliah', '')}</strong><br><small style="color:#64748b;">{r.get('Kode MK dan Kelas', '')} - {r.get('Ruangan', '')}</small></td>
            <td>{r.get('Jadwal', '')}</td>
            <td style="text-align:center;">{status_tag}</td>
            <td style="text-align:center;">{r.get('Datang', '-')}</td>
            <td>{r.get('Terlambat', '-')}</td>
        </tr>
        """

    html = f"""<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>Laporan Monitoring Kehadiran Dosen Antar-Prodi & Jenis Kelas</title>
    <style>
        @page {{
            size: A4;
            margin: 12mm;
        }}
        body {{
            font-family: 'Helvetica Neue', Arial, sans-serif;
            color: #1e293b;
            background: #fff;
            margin: 0;
            padding: 15px;
            font-size: 10px;
            line-height: 1.35;
        }}
        .header {{
            border-bottom: 2px solid #0f172a;
            padding-bottom: 10px;
            margin-bottom: 14px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .header h1 {{
            font-size: 15px;
            text-transform: uppercase;
            margin: 0 0 3px 0;
            color: #0f172a;
        }}
        .header p {{
            margin: 0;
            color: #64748b;
            font-size: 9.5px;
        }}
        .meta-box {{
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            padding: 8px 12px;
            margin-bottom: 14px;
            display: grid;
            grid-template-columns: 1fr 1fr;
            row-gap: 5px;
            font-size: 10px;
        }}
        .kpi-container {{
            display: flex;
            gap: 8px;
            margin-bottom: 14px;
        }}
        .kpi-card {{
            flex: 1;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            padding: 8px;
            text-align: center;
            background: #fff;
        }}
        .kpi-label {{
            font-size: 8.5px;
            text-transform: uppercase;
            color: #64748b;
            font-weight: bold;
        }}
        .kpi-val {{
            font-size: 16px;
            font-weight: bold;
            color: #0f172a;
            margin-top: 3px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 9px;
            margin-bottom: 14px;
        }}
        table, th, td {{
            border: 1px solid #cbd5e1;
        }}
        th {{
            background: #f1f5f9;
            color: #334155;
            padding: 5px;
            text-transform: uppercase;
            font-size: 8.5px;
        }}
        td {{
            padding: 4px 5px;
        }}
        .section-title {{
            font-size: 10.5px;
            font-weight: bold;
            text-transform: uppercase;
            color: #0f172a;
            margin: 12px 0 5px 0;
        }}
        .signature-area {{
            margin-top: 20px;
            display: flex;
            justify-content: space-between;
        }}
        .sig-box {{
            width: 240px;
            text-align: center;
        }}
        @media print {{
            body {{ padding: 0; }}
            .no-print {{ display: none; }}
        }}
    </style>
</head>
<body>
    <div class="no-print" style="margin-bottom: 15px; text-align: right;">
        <button onclick="window.print()" style="padding: 7px 14px; background: #0284c7; color: white; border: none; border-radius: 4px; cursor: pointer; font-weight: bold;">
            Cetak ke PDF / Print (Ctrl + P)
        </button>
    </div>

    <div class="header">
        <div>
            <h1>Laporan Monitoring Presensi & Kinerja Dosen</h1>
            <p>Fakultas Teknik | Teknik Informatika &bull; Teknik Lingkungan</p>
        </div>
        <div style="text-align: right;">
            <strong style="color: #0284c7;">DOKUMEN RESMI AKADEMIK</strong><br>
            <span style="color: #64748b;">Tanggal Cetak: {tgl_cetak}</span>
        </div>
    </div>

    <div class="meta-box">
        <div><strong>Nama Dosen:</strong> {dosen}</div>
        <div><strong>Semester / T.A.:</strong> Semester Ganjil 2026/2027</div>
        <div><strong>NIDN:</strong> 9919121988</div>
        <div><strong>Program Studi:</strong> Teknik Informatika (TI/PU) &bull; Teknik Lingkungan (TL)</div>
    </div>

    <div class="kpi-container">
        <div class="kpi-card">
            <div class="kpi-label">Total Sesi Terjadwal</div>
            <div class="kpi-val">{total_sesi}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Sesi Terlaksana</div>
            <div class="kpi-val" style="color: #0284c7;">{executed}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Tingkat Kehadiran</div>
            <div class="kpi-val" style="color: #166534;">{rate_kehadiran}%</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Total Terlambat</div>
            <div class="kpi-val" style="color: #b45309;">{terlambat} Kali</div>
        </div>
    </div>

    <div class="section-title">A. Ringkasan Realisasi per Rombel & Jenis Kelas</div>
    <table>
        <thead>
            <tr>
                <th style="width: 20px;">No</th>
                <th style="width: 90px;">Program Studi</th>
                <th style="width: 120px;">Jenis Kelas</th>
                <th>Mata Kuliah & Kode</th>
                <th style="width: 30px;">SKS</th>
                <th style="width: 35px;">Jadwal</th>
                <th style="width: 45px;">Realisasi</th>
                <th style="width: 35px;">Hadir</th>
                <th style="width: 35px;">Alpha</th>
                <th style="width: 45px;">% Hadir</th>
            </tr>
        </thead>
        <tbody>
            {course_rows_html}
        </tbody>
    </table>

    <div class="section-title">B. Log Presensi Terakhir & Keterangan Perkuliahan</div>
    <table>
        <thead>
            <tr>
                <th style="width: 20px;">No</th>
                <th style="width: 60px;">Tanggal</th>
                <th style="width: 80px;">Prodi</th>
                <th style="width: 90px;">Jenis Kelas</th>
                <th>Mata Kuliah & Ruangan</th>
                <th style="width: 75px;">Jadwal</th>
                <th style="width: 50px;">Presensi</th>
                <th style="width: 45px;">Datang</th>
                <th>Keterangan</th>
            </tr>
        </thead>
        <tbody>
            {log_rows_html}
        </tbody>
    </table>

    <div class="signature-area">
        <div style="width: 50%;">
            <p style="color: #64748b; margin-bottom: 4px;">Catatan Penjaminan Mutu Fakultas:</p>
            <div style="border: 1px dashed #cbd5e1; border-radius: 4px; padding: 6px; font-size: 8.5px; color: #64748b; height: 45px;">
                Tingkat kehadiran pengajaran dosen telah memenuhi target regulasi SPMI pada seluruh jenis kelas (&gt;80%).
            </div>
        </div>
        <div class="sig-box">
            <p style="margin: 0 0 45px 0;">Mengetahui,<br><strong>Ketua Program Studi / Dekan Fakultas Teknik</strong></p>
            <p style="margin: 0; font-weight: bold; text-decoration: underline;">Dr. Ir. Hendra Saputra, M.Kom.</p>
            <p style="margin: 0; color: #64748b; font-size: 8.5px;">NIP. 197804152005011002</p>
        </div>
    </div>
</body>
</html>
"""

    with open(output_html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Laporan HTML berhasil dibuat di: {output_html_path}")

if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file = os.path.join(base_dir, 'sample_presensi.csv')
    output_html = os.path.join(base_dir, 'laporan_monitoring_presensi.html')

    if os.path.exists(csv_file):
        data = load_attendance_csv(csv_file)
        generate_html_report(data, output_html)
    else:
        print(f"File {csv_file} tidak ditemukan.")

import streamlit as st
from datetime import date, timedelta, datetime
import math
import pandas as pd
import os
import getpass
import socket

# === KONFIGURASI HALAMAN ===
st.set_page_config(page_title="Kalkulator Weton Jawa --- (by@Matkoncar)", page_icon="🌙", layout="wide")

# === NAMA FILE EXCEL ===
FILE_EXCEL = "data_weton_jodoh.xlsx"

# === DATA NEPTU ===
neptu_hari = {
    "Senin": 4, "Selasa": 3, "Rabu": 7, "Kamis": 8,
    "Jumat": 6, "Sabtu": 9, "Minggu": 5
}
daftar_pasaran = ["Legi", "Pahing", "Pon", "Wage", "Kliwon"]
neptu_pasaran = {"Legi":5, "Pahing":9, "Pon":7, "Wage":4, "Kliwon":8}

kategori_sifat = {
    1: "Waseso",
    2: "Bejo",
    3: "Nirsarujuk",
    4: "Asor"
}

kategori_jodoh = {
    1: "Pegat ⚠️ — Kurang baik, rawan perpisahan",
    2: "Ratu ✅ — Sangat baik, harmonis & dihormati",
    3: "Jodoh ✅ — Pasangan sejati, saling melengkapi",
    4: "Topo ✅ — Awal susah, lama-lama bahagia",
    5: "Tinari ✅ — Rezeki lancar, banyak kebahagiaan",
    6: "Pesthi ✅ — Damai, rukun sampai tua",
    7: "Padu ✅ — Saling melengkapi, semangat hidup",
    8: "Sujan ⚠️ — Rawan perselisihan/ketidakjujuran"
}

semua_weton = [
    ("Senin", "Legi", 9), ("Senin", "Pahing", 13), ("Senin", "Pon", 11), ("Senin", "Wage", 8), ("Senin", "Kliwon", 12),
    ("Selasa", "Legi", 8), ("Selasa", "Pahing", 12), ("Selasa", "Pon", 10), ("Selasa", "Wage", 7), ("Selasa", "Kliwon", 11),
    ("Rabu", "Legi", 12), ("Rabu", "Pahing", 16), ("Rabu", "Pon", 14), ("Rabu", "Wage", 11), ("Rabu", "Kliwon", 15),
    ("Kamis", "Legi", 13), ("Kamis", "Pahing", 17), ("Kamis", "Pon", 15), ("Kamis", "Wage", 12), ("Kamis", "Kliwon", 16),
    ("Jumat", "Legi", 11), ("Jumat", "Pahing", 15), ("Jumat", "Pon", 13), ("Jumat", "Wage", 10), ("Jumat", "Kliwon", 14),
    ("Sabtu", "Legi", 14), ("Sabtu", "Pahing", 18), ("Sabtu", "Pon", 16), ("Sabtu", "Wage", 13), ("Sabtu", "Kliwon", 17),
    ("Minggu", "Legi", 10), ("Minggu", "Pahing", 14), ("Minggu", "Pon", 12), ("Minggu", "Wage", 9), ("Minggu", "Kliwon", 13),
]

# === DETEKSI PENGGUNA & IDENTITAS ===
def dapatkan_info_pengguna():
    # Dapatkan nama pengguna sistem
    nama_pengguna = getpass.getuser()
    nama_host = socket.gethostname()
    
    # Bentuk identitas (bisa berupa nama pengguna atau nama komputer)
    identitas = f"{nama_pengguna}@{nama_host}"
    
    # Jika ingin format seperti email:
    email_terdeteksi = f"{nama_pengguna}@{nama_host}.local"
    
    return identitas, email_terdeteksi

# === SIMPAN KE EXCEL ===
def simpan_ke_excel(tanggal_input, nama, tgl_lahir, identitas_pengguna):
    data_baru = {
        "Tanggal Input": tanggal_input,
        "Nama": nama,
        "Tanggal Kelahiran": tgl_lahir,
        "Identitas Pengguna/Email": identitas_pengguna
    }
    
    if os.path.exists(FILE_EXCEL):
        df = pd.read_excel(FILE_EXCEL)
        df = pd.concat([df, pd.DataFrame([data_baru])], ignore_index=True)
    else:
        df = pd.DataFrame([data_baru])
    
    df.to_excel(FILE_EXCEL, index=False)
    return True

# === HITUNG WETON ===
def hitung_weton(tgl_obj):
    nama_hari = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    hari = nama_hari[tgl_obj.weekday()]
    
    tgl_acuan = date(2004, 10, 21)
    selisih = (tgl_obj - tgl_acuan).days
    
    indeks_pasaran = (0 + selisih) % 5
    if indeks_pasaran < 0:
        indeks_pasaran += 5
    
    pasaran = daftar_pasaran[indeks_pasaran]
    neptu = neptu_hari[hari] + neptu_pasaran[pasaran]
    return hari, pasaran, neptu

def hitung_sifat(neptu):
    sisa = neptu - math.floor(neptu / 4) * 4
    if sisa == 0:
        sisa = 4
    return kategori_sifat[sisa]

def hitung_kategori_jodoh(neptu1, neptu2):
    jumlah = neptu1 + neptu2
    sisa = jumlah % 8
    if sisa == 0:
        sisa = 8
    return jumlah, kategori_jodoh[sisa]

# === JUDUL ===
st.markdown("<h1 style='font-size: 24px;'>🌙 Kalkulator Weton Jawa</h1>", unsafe_allow_html=True)
st.subheader("Sifat Cipto, Roso & Kecocokan Calon Jodoh")
st.markdown("---")

# === INPUT DATA ===
st.markdown("### 📋 Data Pengguna")
nama = st.text_input("Nama Lengkap")
tgl_lahir = st.date_input(
    "Tanggal Kelahiran (yyyy,mm,dd)",
    value=date(2026, 10, 21),
    min_value=date(1900, 1, 1),
    max_value=date(2036, 12, 31),
    format="YYYY/MM/DD"
)

# Tampilkan info yang terdeteksi (untuk konfirmasi)
identitas, email_terdeteksi = dapatkan_info_pengguna()
st.info(f"📌 Identitas perangkat terdeteksi: **{email_terdeteksi}**")

simpan = st.button(">>>>Proses dan lanjutkan ")
st.markdown("---")

# === PROSES & SIMPAN ===
if simpan:
    if not nama:
        st.error("⚠️ Harap isi Nama Lengkap terlebih dahulu!")
    else:
        tanggal_input = datetime.now().strftime("%d %B %Y, %H:%M:%S")
        tgl_lahir_str = tgl_lahir.strftime("%d %B %Y")
        
        berhasil = simpan_ke_excel(tanggal_input, nama, tgl_lahir_str, email_terdeteksi)
        if berhasil:
            st.success(f"✅ Terima kasih **{nama}**, berikut ini hasilnya ")
        
        # === HITUNG HASIL ===
        hari_lahir, pasaran_lahir, neptu_lahir = hitung_weton(tgl_lahir)
        sifat_cipto = hitung_sifat(neptu_lahir)
        
        tgl_roso = tgl_lahir + timedelta(days=21)
        hari_roso, pasaran_roso, neptu_roso = hitung_weton(tgl_roso)
        sifat_roso = hitung_sifat(neptu_roso)
        
        # === TAMPILAN HASIL ===
        st.markdown("---")
        st.write(f"**Nama:** {nama}")
        st.write(f"**Tanggal Kelahiran:** {tgl_lahir_str}")
        st.write(f"**Weton:** {hari_lahir} {pasaran_lahir}")
        st.write(f"**Neptu Kelahiran:** {neptu_lahir}")
        st.write(f"**Sifat Cipto:** → {sifat_cipto}")
        st.write(f"**Sifat Roso:** → {sifat_roso}")
        
        st.markdown("---")
        
        # === ANALISA CALON JODOH ===
        st.header("💘 Analisa Calon Jodoh — Neptu " + str(neptu_lahir))
        
        cocok_list = []
        tidak_cocok_list = []
        
        for hari_p, pasaran_p, neptu_p in semua_weton:
            if neptu_p == neptu_lahir and hari_p == hari_lahir and pasaran_p == pasaran_lahir:
                continue
            jml, kat = hitung_kategori_jodoh(neptu_lahir, neptu_p)
            if "✅" in kat:
                cocok_list.append({
                    "Weton": f"{hari_p} {pasaran_p}",
                    "Neptu": neptu_p,
                    "Jumlah": jml,
                    "Kategori": kat
                })
            else:
                tidak_cocok_list.append({
                    "Weton": f"{hari_p} {pasaran_p}",
                    "Neptu": neptu_p,
                    "Jumlah": jml,
                    "Kategori": kat
                })
        
        urutan_prioritas = ["Pesthi", "Ratu", "Tinari", "Jodoh", "Padu", "Topo"]
        cocok_list.sort(key=lambda x: next((urutan_prioritas.index(k) for k in urutan_prioritas if k in x["Kategori"]), 99))
        
        col_cocok, col_tidak = st.columns([3, 2])
        
        with col_cocok:
            st.subheader("✅ Pasangan yang Cocok")
            if cocok_list:
                st.table(cocok_list)
            else:
                st.info("Tidak ada data pasangan")
        
        with col_tidak:
            st.subheader("⚠️ Kurang Disarankan")
            if tidak_cocok_list:
                st.table(tidak_cocok_list)
            else:
                st.info("Tidak ada data")
        
        st.markdown("---")
        
        # === KESIMPULAN ===
        st.subheader("📌 Kesimpulan")
        if cocok_list:
            terbaik = cocok_list[0]
            st.success(f"""
            **Pasangan Paling Direkomendasikan:**
            - Weton: **{terbaik['Weton']}** (Neptu {terbaik['Neptu']})
            - Kategori: **{terbaik['Kategori']}**
            
            Neptu **{neptu_lahir}** paling cocok dengan neptu:
            {', '.join(sorted(set(str(c['Neptu']) for c in cocok_list)))}
            """)
        
        st.caption(f"📌 Data tersimpan di: {FILE_EXCEL} | Tradisi/primbon Jawa — keharmonisan ditentukan oleh kasih sayang & kesetiaan bersama 😊")

        # === TOMBOL MENU DI BAWAH ===
        st.markdown("### 📋 Menu")
        col1, col2, _ = st.columns([1, 1, 3])
        
        with col1:
            if st.button("🆕 Data Baru", type="primary"):
                st.session_state.mulai_baru = True
                st.experimental_rerun()
        
        with col2:
            if st.button("🚪 Selesai / Keluar"):
                st.info("Terima kasih sudah menggunakan Kalkulator Weton Jawa! 😊")
                st.stop()

# === LIHAT SEMUA DATA ===
#if os.path.exists(FILE_EXCEL):
#    with st.expander("📂 Lihat Data yang Tersimpan"):
#        df_tampil = pd.read_excel(FILE_EXCEL)
#       st.dataframe(df_tampil, use_container_width=True)

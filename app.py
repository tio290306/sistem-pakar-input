import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Sistem Pakar Diskon", page_icon="🧠", layout="centered")

st.title("🧠 Sistem Pakar Diskon Pelanggan")

st.write("Masukkan data pelanggan di bawah ini. Jika email sudah terdaftar, data pelanggan akan diperbarui otomatis.")

with st.form("form_data"):
    nama = st.text_input("Nama Pelanggan")
    email = st.text_input("Email Pelanggan")
    nomor = st.text_input("Nomor Telepon")

    st.subheader("Data Perilaku Belanja")
    kunjungan_baru = st.number_input("Jumlah kunjungan (baru)", min_value=0, step=1)
    belanja_baru = st.number_input("Total belanja (baru) (Rp)", min_value=0, step=1000)

    submit = st.form_submit_button("Proses & Simpan Data")

def hitung_diskon(total_kunjungan, total_belanja):
    if total_kunjungan >= 10 and total_belanja >= 2000000:
        return "Diskon 25%"
    elif total_kunjungan >= 7 and total_belanja >= 1500000:
        return "Diskon 20%"
    elif total_kunjungan >= 5 and total_belanja >= 1000000:
        return "Diskon 15%"
    elif total_kunjungan >= 3 and total_belanja >= 500000:
        return "Diskon 10%"
    else:
        return "Diskon 5%"

FILE = "database.xlsx"

def update_database(nama, email, nomor, kunjungan_baru, belanja_baru):
    if not os.path.exists(FILE):
        df = pd.DataFrame([{
            "tanggal_update": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "nama": nama,
            "email": email,
            "nomor": nomor,
            "total_kunjungan": kunjungan_baru,
            "total_belanja": belanja_baru
        }])
        df.to_excel(FILE, index=False)
        return df.loc[0]

    df = pd.read_excel(FILE)

    if email in df["email"].values:
        row_index = df[df["email"] == email].index[0]

        old_kunjungan = df.loc[row_index, "total_kunjungan"]
        old_belanja = df.loc[row_index, "total_belanja"]

        new_kunjungan = old_kunjungan + kunjungan_baru
        new_belanja = old_belanja + belanja_baru

        df.loc[row_index, "total_kunjungan"] = new_kunjungan
        df.loc[row_index, "total_belanja"] = new_belanja
        df.loc[row_index, "tanggal_update"] = datetime.now().strftime("%Y-%m-%d %H:%M")

        df.to_excel(FILE, index=False)
        return df.loc[row_index]

    else:
        new_row = {
            "tanggal_update": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "nama": nama,
            "email": email,
            "nomor": nomor,
            "total_kunjungan": kunjungan_baru,
            "total_belanja": belanja_baru
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_excel(FILE, index=False)

        return pd.Series(new_row)

if submit:
    if email == "" or nama == "":
        st.warning("⚠ Harap isi seluruh data pelanggan!")
    else:
        updated_row = update_database(nama, email, nomor, kunjungan_baru, belanja_baru)

        hasil_diskon = hitung_diskon(updated_row["total_kunjungan"], updated_row["total_belanja"])

        st.success(f"🎉 Diskon Pelanggan: **{hasil_diskon}**")

        st.subheader("📌 Riwayat Pelanggan (Model Ringkas)")
        st.write(f"**Nama:** {updated_row['nama']}")
        st.write(f"**Email:** {updated_row['email']}")
        st.write(f"**Nomor:** {updated_row['nomor']}")
        st.write(f"**Total Kunjungan:** {updated_row['total_kunjungan']}")
        st.write(f"**Total Belanja:** Rp {updated_row['total_belanja']:,}")
        st.write(f"**Terakhir Update:** {updated_row['tanggal_update']}")

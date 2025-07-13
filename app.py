import streamlit as st
import pandas as pd
from statistics import mode, StatisticsError
import matplotlib.pyplot as plt

st.set_page_config(page_title="Statistik dari Excel", layout="wide")
st.title("Aplikasi Simulasi Statistik Deskriptif Matematika Terapan")
st.subheader("Perhitungan untuk mencari Mean, Median, Modus, Varians dan Standar Deviasi")

def show_statistics(mean, median, mode, var, std, text):
    st.subheader(f"📈 Statistik dari {text}")
    st.markdown(f"- **Mean (Rata-rata):** {mean:.2f}")
    st.text("Didapatkan dari penjumlahan keseluruhan data dan dibagi dengan jumlah banyaknya data.")
    st.markdown(f"- **Median:** {median:.2f}")
    st.text("Urutkan data dari kecil ke besar. Jika data genap maka dijumlahkan dan dibagi 2 / ketika ganjil ambil yang paling tengah.")
    st.markdown(f"- **Modus:** {mode}")
    st.text("Temukan nilai yang sering muncul, maka itulah hasilnya.")
    st.markdown(f"- **Varians:** {var:.2f}")
    st.text("Berkaitan dengan mean, cari selisih dan kuadratnya, kemudian jumlahkan dan dibagi dengan jumlah banyaknya data.")
    st.markdown(f"- **Standar Deviasi:** {std:.2f}")
    st.text("Hasil dari varians diakarkan.")


def show_charts(data):
    st.subheader("📈 Visualisasi Data")

    col1, col2 = st.columns([1, 1])

    with col1:
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.hist(data, bins="auto", color="#3ed2e6", edgecolor="black")
        ax.set_title("Histogram")
        ax.set_xlabel("Nilai")
        ax.set_ylabel("Frekuensi")
        st.pyplot(fig)

    with col2:
        fig2, ax2 = plt.subplots(figsize=(8, 4))
        ax2.boxplot(data, vert=False)
        ax2.set_title("Boxplot")
        st.pyplot(fig2)


def File(file):
    try:
        # Membaca file Excel
        if file.name.endswith(".csv"):
            df = pd.read_csv(file)
        elif file.name.endswith(".xlsx"):
            df = pd.read_excel(file, engine="openpyxl")
        else:
            st.error("Format file tidak dikenali.")
            df = None
        st.success("✅ File berhasil dibaca!")
        col1, col2s = st.columns([1, 1])
        # Tampilkan preview data
        with col1:
            st.subheader("📄 Data Preview")
            st.dataframe(df)
        numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns.tolist()

        if not numeric_cols:
            st.warning("❗ Tidak ditemukan kolom numerik dalam file Excel.")
        else:
            # Pilih kolom untuk analisis
            with col1:
                selected_col = st.selectbox(
                    "Pilih kolom numerik yang akan dianalisis:", numeric_cols
                )

            if selected_col:
                data = df[selected_col].dropna()
                mean_val = data.mean()
                median_val = data.median()
                try:
                    mode_val = mode(data)
                except StatisticsError:
                    mode_val = "Tidak ada (semua unik)"
                var_val = data.var()
                std_dev = data.std()
                # Tampilkan hasil
                with col2s:
                    st.subheader(f"Hasil Statistik Kolom: **{selected_col}**")
                    show_statistics(
                        mean_val, median_val, mode_val, var_val, std_dev, "File Excel"
                    )
                show_charts(data)

    except Exception as e:
        st.error(f"❌ Gagal membaca file Excel. Error: {e}")


def Manual(args):
    try:
        to_num_int = [float(x.strip()) for x in args.split(",")]
        data = pd.Series(to_num_int)
        mean_val = data.mean()
        median_val = data.median()
        try:
            mode_val = mode(data.tolist())
        except StatisticsError:
            mode_val = "Tidak ada (semua unik)"
        st.success("✅ Data berhasil dianalisis.")
        col1, col2 = st.columns([1, 2])
        var_val = data.var()
        std_dev = data.std()
        with col1:
            show_statistics(
                mean_val, median_val, mode_val, var_val, std_dev, "Manual Input"
            )
        with col2:
            show_charts(data)
    except Exception as e:
        st.error(f"❌ Terjadi kesalahan saat memproses data manual: {e}")


seg_control = st.segmented_control(
    "Pilih input", ["Manual", "Excel"], selection_mode="single"
)
# Upload File
if seg_control == "Manual":
    num_input = st.text_input("Masukan data numericnya")
    st.caption(
        "Contoh : 1,2,3,4,5,6. Gunakan tanda koma (,) untuk memisahkan data numericnya."
    )
    if not num_input:
        st.info("⬆️ Silakan input angka yang akan di analisis.")
    if num_input:
        Manual(num_input)

elif seg_control == "Excel":
    uploaded_file = st.file_uploader(
        "📥 Upload file Excel (.xlsx) di sini:", type=["xlsx", "csv"]
    )
    if not uploaded_file:
        st.info("⬆️ Silakan upload file Excel untuk memulai analisis.")

    if uploaded_file is not None:
        File(uploaded_file)

else:
    st.warning("Pilih menu terlebih dahulu.")

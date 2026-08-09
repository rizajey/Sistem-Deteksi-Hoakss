import streamlit as st
from preprocessing import preprocess_text
from model import predict
import re


st.set_page_config(
    page_title="Deteksi Berita Hoaks",
    page_icon="📰",
    layout="wide"
)

# ================= HEADER =================
st.title("Sistem Deteksi Berita Hoaks")
st.markdown(
    """
    Sistem ini menggunakan **Model IndoBERT** untuk melakukan klasifikasi teks berita berbahasa Indonesia.
    
    """
)

col1, col2 = st.columns(2)

with col1:
    st.info(""" 
    Ciri-Ciri **Berita Hoaks**   

    1. **Judul Provokatif**, Menggunakan kata-kata sensasional, atau bertujuan memancing emosi pembaca.
    2. **Sumber Tidak Jelas**, Berita tidak mencantumkan sumber, penulis, atau media yang dapat dipercaya dan diverifikasi.
    3. **Bahasa Emosional dan Mengajak Menyebarkan**, Menggunakan kalimat yang menimbulkan rasa takut, marah, atau panik serta sering disertai ajakan seperti "sebarkan sekarang", "viralkan".
    
    """ )

with col2:
    st.warning("""
    Contoh **Berita Hoaks** :

    **Judul:**
    HEBOH! Mulai Besok Semua Rekening Bank Akan Diblokir Permanen, Segera Tarik Uang Anda Sebelum Terlambat!

    **Isi Berita:**
    Beredar informasi bahwa seluruh rekening bank di Indonesia akan diblokir secara permanen mulai besok pagi akibat adanya kebijakan rahasia yang belum diumumkan kepada masyarakat. Informasi ini disebut berasal dari orang dalam yang mengetahui keputusan tersebut, namun identitasnya tidak dapat diungkapkan.
    Sebarkan informasi ini kepada keluarga, teman, dan kerabat Anda sebelum berita ini dihapus! Jangan sampai mereka menjadi korban.
    """ )
st.divider()

# ================ LAYOUT ==================
col1, col2 = st.columns([2, 1])

with col1:

    st.subheader("Cek Berita")


    # Fungsi reset
    def reset_input():
        st.session_state.input_text = ""
        st.session_state.hasil_prediksi = False
        st.session_state.label = None
        st.session_state.confidence = None
        st.session_state.clean_text = None


    # Inisialisasi session state
    if "input_text" not in st.session_state:
        st.session_state.input_text = ""

    if "hasil_prediksi" not in st.session_state:
        st.session_state.hasil_prediksi = False


    input_text = st.text_area(
        "Masukkan isi berita  untuk memeriksa apakah berita tersebut termasuk fakta atau hoaks.",
        height=350,
        placeholder="Masukan narasi berita disini",
        key="input_text"
    )


    col_btn1, col_btn2 = st.columns(2)


    with col_btn1:
        prediksi = st.button(
            "🔍 Prediksi",
            use_container_width=True
        )


    with col_btn2:
        reset = st.button(
            "🗑 Reset",
            use_container_width=True,
            on_click=reset_input
        )

with col2:

    st.subheader("Hasil Prediksi")

    if prediksi:

        if input_text.strip() == "":
            st.warning("Masukkan isi berita terlebih dahulu.")

        else:

            # Preprocessing
            clean_text = preprocess_text(input_text)

            # Prediksi
            label, confidence = predict(clean_text)

            if label == 1:
                st.error("🟥 Hoaks")
            else:
                st.success("🟩 Fakta")

            st.metric(
                label="Confidence",
                value=f"{confidence*100:.2f}%"
            )

            st.progress(confidence)

            with st.expander("Hasil Preprocessing"):
                st.write(clean_text)

    else:

        st.info("Belum ada hasil prediksi.")

        st.metric(
            label="Confidence",
            value="-"
        )

        st.progress(0)

# ================ FOOTER ==================
st.caption(
    "Sistem Deteksi Berita Hoaks menggunakan model IndoBERT."
)
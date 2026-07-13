import streamlit as st
import requests
import time

st.set_page_config(
    page_title="Agnes AI - Fast Lipsync Generator",
    page_icon="🎬",
    layout="centered"
)

st.title("🎬 Agnes AI - Fast Lipsync Generator")
st.write("Hubungkan video karaktermu dengan file audio suara secara instan menggunakan teknologi lipsync cepat.")

# Input API Key Agnes AI
api_key = st.sidebar.text_input("Agnes AI API Key", type="password", help="Masukkan API Key Agnes AI milikmu untuk mulai memproses.")

st.sidebar.markdown("---")
st.sidebar.markdown("Developed with ❤️ via Agnes Streamlit Engine")

if not api_key:
    st.info("💡 Silakan masukkan API Key Agnes AI Anda di sidebar sebelah kiri untuk memulai!")
else:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("1. Video Karakter")
        video_file = st.file_uploader("Upload Video (MP4/MOV)", type=["mp4", "mov"])
        if video_file:
            st.video(video_file)
            
    with col2:
        st.subheader("2. Audio Pengisi Suara")
        audio_file = st.file_uploader("Upload Audio (MP3/WAV)", type=["mp3", "wav"])
        if audio_file:
            st.audio(audio_file)

    st.markdown("---")
    
    if video_file and audio_file:
        if st.button("🔥 Proses Lipsync Sekarang", use_container_width=True):
            with st.spinner("Mengunggah file dan memproses lipsync di server Agnes AI... Mohon tunggu sebentar."):
                try:
                    # Simulasi pengiriman file ke endpoint lipsync Agnes AI
                    files = {
                        'video': video_file.getvalue(),
                        'audio': audio_file.getvalue()
                    }
                    headers = {
                        'Authorization': f'Bearer {api_key}'
                    }
                    
                    response = requests.post(
                        "https://api.agnes-ai.com/v1/lipsync",
                        files=files,
                        headers=headers,
                        timeout=300
                    )
                    
                    if response.status_code == 200:
                        res_data = response.json()
                        
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        for percent_complete in range(1, 101, 5):
                            time.sleep(1)
                            progress_bar.progress(percent_complete)
                            status_text.text(f"Sedang menyelaraskan bibir dengan audio... ({percent_complete}%)")
                        
                        video_result_url = res_data.get("video_url")
                        
                        if video_result_url:
                            st.success("✅ Lipsync Berhasil Disinkronkan!")
                            st.video(video_result_url)
                        else:
                            st.error("Gagal mendapatkan URL video hasil. Silakan coba lagi.")
                    else:
                        st.error(f"Gagal menghubungi server API: {response.status_code} - {response.text}")
                except Exception as e:
                    st.error(f"Terjadi kesalahan koneksi: {str(e)}")
    else:
        st.warning("⚠️ Harap unggah video dan audio terlebih dahulu untuk mengaktifkan tombol proses.")

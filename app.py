import streamlit as st
import pandas as pd
import subprocess
import os
from typing import List
import whisper

# Configuração da página
st.set_page_config(
    page_title="Transcritor de Vídeos",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título e descrição
st.title("🎬 Transcritor de Vídeos")
st.markdown("""
Insira uma lista de URLs de vídeos para extrair o áudio e gerar transcrições automaticamente.
Suporta YouTube e links diretos de vídeo.
""")

@st.cache_resource
def load_whisper_model():
    return whisper.load_model("base")

model = load_whisper_model()

def download_audio(url: str, output_path: str) -> str:
    """
    Downloads audio from a video URL. Tries yt-dlp first, then falls back to direct download.
    """
    temp_video = os.path.join(output_path, "temp_video")
    audio_file = os.path.join(output_path, "temp_audio.mp3")
    
    # Clean up previous temp files
    for f in [temp_video, audio_file]:
        if os.path.exists(f):
            os.remove(f)
            
    # Strategy 1: yt-dlp (best for YouTube and supported sites)
    try:
        command = ["yt-dlp", "-x", "--audio-format", "mp3", "-o", audio_file, url]
        subprocess.run(command, check=True, capture_output=True)
        if os.path.exists(audio_file):
            return audio_file
    except Exception:
        pass

    # Strategy 2: Direct download + ffmpeg conversion
    try:
        # Download file
        subprocess.run(["curl", "-L", "-o", temp_video, url], check=True, capture_output=True)
        # Convert to mp3
        subprocess.run(["ffmpeg", "-i", temp_video, "-vn", "-acodec", "libmp3lame", audio_file], check=True, capture_output=True)
        if os.path.exists(audio_file):
            return audio_file
    except Exception as e:
        st.warning(f"Erro ao processar {url}: {e}")
        
    return None

def transcribe_audio(audio_path: str) -> str:
    """
    Transcribes audio file using OpenAI Whisper.
    """
    if not audio_path or not os.path.exists(audio_path):
        return "Erro: Arquivo de áudio não encontrado."
    
    try:
        st.info(f"Transcrevendo áudio com Whisper: {os.path.basename(audio_path)}...")
        result = model.transcribe(audio_path)
        return result["text"]
    except Exception as e:
        return f"Erro durante a transcrição com Whisper: {e}"

def process_urls(urls: List[str]) -> pd.DataFrame:
    """
    Processes a list of URLs and returns a DataFrame with results.
    """
    results = []
    temp_dir = "temp_files"
    os.makedirs(temp_dir, exist_ok=True)
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for idx, url in enumerate(urls):
        status_text.text(f"Processando {idx + 1}/{len(urls)}: {url[:50]}...")
        
        audio_file = download_audio(url, temp_dir)
        if audio_file:
            transcription = transcribe_audio(audio_file)
            results.append({"URL": url, "Transcrição": transcription})
            # Clean up
            if os.path.exists(audio_file):
                os.remove(audio_file)
        else:
            results.append({"URL": url, "Transcrição": "Falha ao baixar ou converter vídeo."})
        
        progress_bar.progress((idx + 1) / len(urls))
    
    status_text.text("✅ Processamento concluído!")
    return pd.DataFrame(results)

# Sidebar para configurações
with st.sidebar:
    st.header("⚙️ Configurações")
    input_method = st.radio(
        "Escolha como inserir as URLs:",
        ["Colar múltiplas URLs", "Arquivo CSV"]
    )

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📝 Insira as URLs dos Vídeos")
    
    if input_method == "Colar múltiplas URLs":
        urls_text = st.text_area(
            "Cole as URLs (uma por linha):",
            placeholder="https://www.youtube.com/watch?v=...\nhttps://exemplo.com/video.mp4\n...",
            height=150
        )
        urls = [url.strip() for url in urls_text.split("\n") if url.strip()]
    else:
        uploaded_file = st.file_uploader("Faça upload de um arquivo CSV com URLs", type=["csv"])
        urls = []
        if uploaded_file is not None:
            try:
                df_uploaded = pd.read_csv(uploaded_file)
                # Assume the first column contains URLs
                urls = df_uploaded.iloc[:, 0].tolist()
                st.success(f"✅ {len(urls)} URLs carregadas do arquivo!")
            except Exception as e:
                st.error(f"Erro ao ler o arquivo: {e}")

with col2:
    st.subheader("📊 Resumo")
    st.metric("URLs a processar", len(urls))

# Botão para processar
st.divider()
if st.button("🚀 Iniciar Transcrição", type="primary", use_container_width=True):
    if not urls:
        st.error("⚠️ Por favor, insira pelo menos uma URL!")
    else:
        st.info(f"Iniciando processamento de {len(urls)} vídeo(s)...")
        df_results = process_urls(urls)
        
        # Exibir resultados
        st.subheader("📋 Resultados da Transcrição")
        st.dataframe(df_results, use_container_width=True, height=400)
        
        # Opções de download
        st.divider()
        col1, col2 = st.columns(2)
        
        with col1:
            csv = df_results.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Baixar como CSV",
                data=csv,
                file_name="transcricoes.csv",
                mime="text/csv"
            )
        
        with col2:
            # Exportar para Excel
            try:
                import io
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine=\'openpyxl\') as writer:
                    df_results.to_excel(writer, index=False, sheet_name=\'Transcrições\')
                buffer.seek(0)
                st.download_button(
                    label="📥 Baixar como Excel",
                    data=buffer.getvalue(),
                    file_name="transcricoes.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            except Exception as e:
                st.warning(f"Não foi possível exportar para Excel: {e}")

# Footer
st.divider()
st.markdown("""
---
**Dicas de Uso:**
- 🎥 Suporta URLs do YouTube, Vimeo e outros sites compatíveis com `yt-dlp`
- 📁 Também aceita links diretos para arquivos de vídeo (MP4, WebM, etc.)
- ⏱️ O tempo de processamento depende da duração do vídeo
- 💾 Os resultados são salvos automaticamente em CSV ou Excel

**Requisitos do Sistema:**
- Python 3.8+
- FFmpeg instalado
- Conexão com internet
""")

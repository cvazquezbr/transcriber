import os
import sys
import pandas as pd
import subprocess
from typing import List
import whisper

# Load Whisper model once
model = whisper.load_model("base")

def download_audio(url: str, output_path: str) -> str:
    """
    Downloads audio from a video URL. Tries yt-dlp first, then falls back to direct download.
    """
    print(f"Processando: {url}...")
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
        subprocess.run(["wget", "-O", temp_video, url], check=True, capture_output=True)
        # Convert to mp3
        subprocess.run(["ffmpeg", "-i", temp_video, "-vn", "-acodec", "libmp3lame", audio_file], check=True, capture_output=True)
        if os.path.exists(audio_file):
            return audio_file
    except Exception as e:
        print(f"Erro ao processar {url}: {e}")
        
    return None

def transcribe_audio(audio_path: str) -> str:
    """
    Transcribes audio file using OpenAI Whisper.
    """
    if not audio_path or not os.path.exists(audio_path):
        return "Erro: Arquivo de áudio não encontrado."
    
    print(f"Transcrevendo áudio com Whisper: {os.path.basename(audio_path)}...")
    try:
        result = model.transcribe(audio_path)
        return result["text"]
    except Exception as e:
        print(f"Erro durante a transcrição com Whisper: {e}")
        return "Erro durante a transcrição."

def process_urls(urls: List[str]) -> pd.DataFrame:
    """
    Processes a list of URLs and returns a DataFrame with results.
    """
    results = []
    temp_dir = "temp_files"
    os.makedirs(temp_dir, exist_ok=True)
    
    for url in urls:
        audio_file = download_audio(url, temp_dir)
        if audio_file:
            transcription = transcribe_audio(audio_file)
            results.append({"URL": url, "Transcrição": transcription})
            # Clean up
            if os.path.exists(audio_file):
                os.remove(audio_file)
        else:
            results.append({"URL": url, "Transcrição": "Falha ao baixar ou converter vídeo."})
            
    return pd.DataFrame(results)

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 transcriber.py <url1> <url2> ...")
        return

    urls = sys.argv[1:]
    df = process_urls(urls)
    
    print("\n--- Resultado da Transcrição ---\n")
    print(df.to_markdown(index=False))
    
    df.to_csv("transcricoes.csv", index=False)
    print("\nResultados salvos em \'transcricoes.csv\'.")

if __name__ == "__main__":
    main()

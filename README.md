# Transcritor de Vídeos em Python

Este aplicativo permite receber uma lista de URLs de vídeos, extrair o áudio automaticamente e realizar a transcrição do conteúdo, gerando uma tabela organizada com os resultados.

## Funcionalidades

- Suporte a URLs do YouTube e outras plataformas (via `yt-dlp`).
- Download direto de arquivos de vídeo (via `curl`).
- Extração de áudio de alta qualidade (via `ffmpeg`).
- Transcrição automática de fala para texto.
- Exportação dos resultados para uma tabela no console e arquivo CSV.

## Pré-requisitos

Antes de começar, você precisará ter instalado em sua máquina:
- Python 3.8 ou superior
- FFmpeg (para processamento de áudio)

## Passo a Passo

### 1. Clonar o Repositório

Abra o terminal e execute o comando abaixo para clonar o projeto:

```bash
git clone https://github.com/cvazquezbr/transcriber.git
cd transcriber
```

### 2. Instalar Dependências

Instale as bibliotecas Python necessárias utilizando o `pip`:

```bash
pip install yt-dlp pandas tabulate
```

*Nota: Certifique-se de que o `ffmpeg` está instalado no seu sistema e acessível via linha de comando.*

### 3. Executar o Aplicativo

Para transcrever vídeos, basta executar o script passando as URLs como argumentos:

```bash
python transcriber.py "URL_DO_VIDEO_1" "URL_DO_VIDEO_2"
```

### Exemplo de Uso

```bash
python transcriber.py "https://www.youtube.com/watch?v=exemplo"
```

O resultado será exibido no terminal em formato de tabela e também será salvo em um arquivo chamado `transcricoes.csv` no mesmo diretório.

## Estrutura do Projeto

- `transcriber.py`: Script principal contendo a lógica de download e transcrição.
- `README.md`: Instruções de uso e instalação.
- `transcricoes.csv`: Arquivo gerado após a execução com os resultados.

---
Desenvolvido para automação de transcrição de mídia.

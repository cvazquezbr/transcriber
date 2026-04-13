# 🎬 Transcritor de Vídeos em Python

Um aplicativo Python completo com interface gráfica que permite receber uma lista de URLs de vídeos, extrair o áudio automaticamente e realizar a transcrição do conteúdo, gerando uma tabela organizada com os resultados.

## ✨ Funcionalidades

- **Interface Web Intuitiva:** Interface moderna construída com Streamlit
- **Suporte Amplo:** URLs do YouTube, Vimeo e links diretos de vídeo
- **Extração de Áudio:** Processamento de alta qualidade com FFmpeg
- **Transcrição Automática:** Conversão de fala para texto
- **Múltiplos Formatos de Entrada:** Cole URLs ou faça upload de arquivo CSV
- **Exportação Flexível:** Baixe resultados em CSV ou Excel
- **Processamento em Tempo Real:** Acompanhe o progresso com barra de progresso

## 📋 Pré-requisitos

Antes de começar, você precisará ter instalado em sua máquina:

- **Python 3.8 ou superior**
- **FFmpeg** (para processamento de áudio)
- **Git** (para clonar o repositório)

### Instalando FFmpeg

#### Windows
```bash
# Usando Chocolatey
choco install ffmpeg

# Ou baixe manualmente de: https://ffmpeg.org/download.html
```

#### macOS
```bash
brew install ffmpeg
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

## 🚀 Passo a Passo de Instalação e Execução

### 1. Clonar o Repositório

Abra o terminal e execute:

```bash
git clone https://github.com/cvazquezbr/transcriber.git
cd transcriber
```

### 2. Criar um Ambiente Virtual (Recomendado)

Crie um ambiente virtual para isolar as dependências:

```bash
# No Windows
python -m venv venv
venv\Scripts\activate

# No macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependências

Com o ambiente virtual ativado, instale as dependências:

```bash
pip install -r requirements.txt
```

Ou instale manualmente:

```bash
pip install streamlit pandas yt-dlp tabulate openpyxl
```

### 4. Executar a Aplicação

Inicie o servidor Streamlit:

```bash
streamlit run app.py
```

A aplicação será aberta automaticamente em seu navegador padrão no endereço `http://localhost:8501`.

## 📖 Como Usar

### Via Interface Web

1. **Abra a aplicação** em seu navegador (normalmente em `http://localhost:8501`)

2. **Escolha o método de entrada:**
   - **Colar múltiplas URLs:** Cole as URLs diretamente na área de texto (uma por linha)
   - **Arquivo CSV:** Faça upload de um arquivo CSV com URLs na primeira coluna

3. **Clique em "🚀 Iniciar Transcrição"**

4. **Acompanhe o progresso** com a barra de progresso em tempo real

5. **Baixe os resultados:**
   - Clique em "📥 Baixar como CSV" para exportar em CSV
   - Clique em "📥 Baixar como Excel" para exportar em XLSX

### Via Linha de Comando (Script Legado)

Você também pode usar o script de linha de comando:

```bash
python transcriber.py "URL_DO_VIDEO_1" "URL_DO_VIDEO_2"
```

## 📁 Estrutura do Projeto

```
transcriber/
├── app.py                 # Aplicação principal com interface Streamlit
├── transcriber.py         # Script de linha de comando (legado)
├── requirements.txt       # Dependências do projeto
├── README.md             # Este arquivo
└── temp_files/           # Diretório temporário (criado automaticamente)
```

## 🔧 Configurações Avançadas

### Variáveis de Ambiente

Você pode configurar algumas opções via variáveis de ambiente:

```bash
# Definir porta customizada (padrão: 8501)
streamlit run app.py --server.port 8000

# Desabilitar o navegador automático
streamlit run app.py --logger.level=info
```

### Arquivo de Configuração

Crie um arquivo `.streamlit/config.toml` para configurações persistentes:

```toml
[server]
port = 8501
headless = false

[logger]
level = "info"
```

## 🐛 Solução de Problemas

### Erro: "ffmpeg not found"
Certifique-se de que o FFmpeg está instalado e acessível no PATH do seu sistema.

### Erro: "yt-dlp failed"
Atualize o yt-dlp:
```bash
pip install --upgrade yt-dlp
```

### Erro de SSL/Certificado
Se encontrar erros de SSL ao baixar vídeos, tente:
```bash
pip install --upgrade certifi
```

### Transcrição vazia ou incompleta
- Verifique se o vídeo contém áudio
- Certifique-se de que o idioma do áudio é suportado
- Tente com um vídeo diferente para descartar problemas específicos

## 📝 Exemplo de Arquivo CSV

Se preferir usar um arquivo CSV, crie um arquivo com a seguinte estrutura:

```csv
URL
https://www.youtube.com/watch?v=exemplo1
https://www.youtube.com/watch?v=exemplo2
https://exemplo.com/video.mp4
```

## 🔐 Privacidade e Segurança

- Os arquivos temporários são deletados automaticamente após o processamento
- Nenhum dado é enviado para servidores externos (exceto para download dos vídeos)
- As transcrições são processadas localmente em sua máquina

## 📊 Limites e Considerações

- **Tempo de Processamento:** Depende da duração do vídeo e velocidade da internet
- **Espaço em Disco:** Certifique-se de ter espaço suficiente para os arquivos temporários
- **Qualidade de Áudio:** Vídeos com áudio de melhor qualidade produzem transcrições mais precisas

## 🤝 Contribuindo

Se encontrar bugs ou tiver sugestões de melhorias, sinta-se livre para abrir uma issue ou pull request no repositório.

## 📄 Licença

Este projeto é fornecido como está, sem garantias.

---

**Desenvolvido para automação de transcrição de mídia.**

Última atualização: 2026-04-13

# Bot de Download do YouTube

Um bot do Telegram capaz de baixar vídeos do YouTube em até **4K**. Este projeto é destinado apenas a fins educacionais. Vídeos acima de **2 GB** são automaticamente comprimidos.

## Recursos
- ✅ Downloads rápidos
- ✅ Escolha da qualidade antes do download
- ✅ Fila de downloads por usuário
- ✅ Redução automática com ffmpeg para vídeos maiores que 2 GB
- ✅ Economia de recursos do servidor
- ✅ Sem limites definidos pelo desenvolvedor

## Como Configurar

### 1. Variáveis de Ambiente
1. Obtenha seu [`BOT_API_KEY`](https://core.telegram.org/bots/tutorial#obtain-your-bot-token).
2. Crie um arquivo `.env` na pasta do projeto e preencha conforme o exemplo:

```ini
BOT_API_KEY="seu_token"
```

### 2. Instalação das Dependências
```bash
git clone https://github.com/hansanaD/TelegramYTDLBot.git
cd TelegramYTDLBot
pip install -r requirements.txt
```

### 3. Iniciando o Bot
Abra um novo terminal ou use `screen` e execute:

```bash
python bot.py
```

O bot e o servidor da API (caso utilize) precisam estar rodando simultaneamente.

## Aviso
Este repositório é apenas para uso pessoal e educacional. Não utilize o projeto para fins comerciais ou atividades ilícitas. O mantenedor não se responsabiliza por mau uso do software ou consequências legais resultantes.

**APIs utilizadas:** [y2mate-api](https://github.com/Simatwa/y2mate-api/) e [pytelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI/).

Dúvidas ou problemas? Entre em contato com [@dev00111](https://t.me/dev00111).

_Espero que este README em português seja mais claro para todos._

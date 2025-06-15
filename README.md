# TelegramYTDLBot

Um bot do Telegram capaz de baixar vídeos do YouTube em até **4K**. Para vídeos maiores que 2 GB, o bot aplica compressão automaticamente.

## Sumário

* [Funcionalidades](#funcionalidades)
* [Requisitos](#requisitos)
* [Instalação](#instalação)
* [Configuração](#configuração)
* [Uso](#uso)
* [API](#api)
* [Aviso](#aviso)
* [Créditos](#créditos)

## Funcionalidades

* Downloads rápidos
* Escolha da qualidade antes do download
* Fila de downloads por usuário
* Compressão automática com ffmpeg para vídeos maiores que 2 GB
* Economia de recursos do servidor
* Sem limites definidos pelo desenvolvedor

## Requisitos

* Python 3.x
* FFmpeg
* Token do bot do Telegram

## Instalação

```bash
git clone https://github.com/hansanaD/TelegramYTDLBot.git
cd TelegramYTDLBot
pip install -r requirements.txt
```

## Configuração

Crie um arquivo `.env` com o token do seu bot:

```ini
BOT_API_KEY="seu_token"
# Opcional: defina BOT_API_URL para apontar para um servidor API do Telegram
```

Para uso com servidor local:

1. Gere instruções a partir de [telegram-bot-api](https://tdlib.github.io/telegram-bot-api/build.html).
2. Acesse:

```bash
cd telegram-bot-api/bin
```

3. Obtenha API ID e HASH: [link](https://core.telegram.org/api/obtaining_api_id)
4. Inicie o servidor:

```bash
./telegram-bot-api --api-id=XXXXX --api-hash=XXXXXXXXXXXX --http-port=8081 --local
```

Referências adicionais:

* [eternnoir/pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI/#using-local-bot-api-sever)
* [tdlib/telegram-bot-api](https://github.com/tdlib/telegram-bot-api)

## Uso

Inicie o bot em um terminal ou usando `screen`:

```bash
python bot.py
```

Mantenha o servidor da API local ativo simultaneamente para pleno funcionamento.

## Deploy com Docker

1. Crie o `.env` com `BOT_API_KEY` e opcional `BOT_API_URL`
2. Execute:

```bash
docker-compose up -d --build
```

O `docker-compose.yml` está preparado para `linux/amd64`, compatível com VPS x86, mesmo em hosts Apple Silicon.

## API

O bot responde a comandos via mensagens no Telegram.

### Endpoints

| Comando/Ação       | Descrição                                           |
| ------------------ | --------------------------------------------------- |
| `/start`           | Saudação e introdução                               |
| `/help`            | Instruções de uso                                   |
| `link do YouTube`  | O bot responde com botões de qualidade para escolha |
| Botão de qualidade | Baixa e envia o vídeo, se menor que 2 GB            |

### Fluxo de exemplo

```text
Usuário: /start
Bot: Hello, I'm a Simple Youtube Downloader!

Usuário: /help
Bot: <b>Just send your youtube link and select the video quality.</b>

Usuário: https://youtu.be/dQw4w9WgXcQ
Bot: Choose a stream:
  [360p] [720p]

Usuário pressiona 720p
Bot: envia o vídeo
```

### Limitações

* Arquivos maiores que **2 GB** não serão enviados
* Apenas links do YouTube são reconhecidos
* Sem servidor local (`BOT_API_URL`), uploads são limitados a **50 MB**

## Aviso

Este projeto é apenas para uso pessoal e educacional. Não use para fins comerciais ou ilegais. O autor não se responsabiliza por qualquer uso indevido.

## Créditos

* [y2mate-api](https://github.com/Simatwa/y2mate-api/)
* [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI/)

Dúvidas ou problemas? Contate [@dev00111](https://t.me/dev00111).

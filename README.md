# TelegramYTDLBot

Um bot do Telegram capaz de baixar vídeos do YouTube em até **4K**. Para vídeos maiores que 2 GB, o bot aplica compressão automaticamente.

## Sumário
- [Funcionalidades](#funcionalidades)
- [Requisitos](#requisitos)
- [Instalação](#instalacao)
- [Configuração](#configuracao)
- [Uso](#uso)
- [Aviso](#aviso)
- [Créditos](#creditos)

## Funcionalidades
- Downloads rápidos
- Escolha da qualidade antes do download
- Fila de downloads por usuário
- Compressão automática com ffmpeg para vídeos maiores que 2 GB
- Economia de recursos do servidor
- Sem limites definidos pelo desenvolvedor

## Requisitos
- Python 3.x
- FFmpeg
- Token do bot do Telegram

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

## Uso
Inicie o bot em um terminal ou usando `screen`:
```bash
python bot.py
```
Mantenha um servidor API do Telegram rodando caso queira acelerar uploads.

## Aviso
Este projeto é apenas para uso pessoal e educacional. Não utilize o código para fins comerciais ou ilegais. O mantenedor não se responsabiliza por mau uso do software ou consequências legais.

## Créditos
- [y2mate-api](https://github.com/Simatwa/y2mate-api/)
- [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI/)

Dúvidas ou problemas? Entre em contato com [@dev00111](https://t.me/dev00111).

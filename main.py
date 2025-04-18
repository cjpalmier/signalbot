import os
import asyncio
from telethon import TelegramClient, events

api_id = int(os.environ['API_ID'])
api_hash = os.environ['API_HASH']
source_channel = int(os.environ['SOURCE_CHANNEL'])      # e.g. -1002680229935
destination_channel = os.environ['CHANNEL_ID']          # e.g. @your_channel or ID
keywords = [kw.strip().lower() for kw in os.environ['KEYWORDS'].split(',')]

client = TelegramClient('cjp', api_id, api_hash)

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    if event.chat_id == source_channel:
        msg = event.raw_text.lower()
        print(f"📩 New message: {msg}")

        if any(keyword in msg for keyword in keywords):
            print("✅ Match found. Forwarding...")
            await client.send_message(destination_channel, event.raw_text)
        else:
            print("❌ No keyword match.")

async def main():
    await client.connect()
    if not await client.is_user_authorized():
        print("❗ Session not authorized. Please generate session file locally.")
        return
    print("✅ Bot connected and listening...")
    await client.run_until_disconnected()

asyncio.run(main())

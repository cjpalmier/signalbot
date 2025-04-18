import os
import asyncio
from telethon import TelegramClient, events

# Load environment variables
api_id = int(os.environ['API_ID'])
api_hash = os.environ['API_HASH']
source_channel = int(os.environ['SOURCE_CHANNEL'])        # Group/channel to listen to
destination_channel = int(os.environ['CHANNEL_ID'])       # Where to forward filtered messages
keywords = [kw.strip().lower() for kw in os.environ['KEYWORDS'].split(',')]

# Start the client session using your session file (e.g., cjp.session)
client = TelegramClient('cjp', api_id, api_hash)

@client.on(events.NewMessage(chats=source_channel, incoming=True, outgoing=True))
async def handler(event):
    msg = event.raw_text.lower()
    print(f"📩 Received message: {msg}")

    if any(keyword in msg for keyword in keywords):
        print("✅ Keyword match! Forwarding message...")
        await client.send_message(destination_channel, event.raw_text)
    else:
        print("❌ No keyword match.")

async def main():
    await client.connect()
    if not await client.is_user_authorized():
        print("❗ Session not authorized. Please create your session file locally.")
        return

    print("✅ Bot is connected and listening...")
    await client.run_until_disconnected()

asyncio.run(main())

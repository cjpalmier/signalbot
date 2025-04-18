import os
from telethon import TelegramClient, events

# Load environment variables
api_id = int(os.environ['API_ID'])
api_hash = os.environ['API_HASH']
source_channel = int(os.environ['SOURCE_CHANNEL'])  # e.g. -1002680229935
destination_channel = os.environ['CHANNEL_ID']      # e.g. @yourprivatechannel or channel ID
keywords = [kw.strip().lower() for kw in os.environ['KEYWORDS'].split(',')]

# Use your saved session name (should match your .session file name without extension)
client = TelegramClient('cjp', api_id, api_hash)

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    if event.chat_id == source_channel:
        msg = event.raw_text.lower()
        print(f"📩 New message from signal channel: {msg}")

        if any(keyword in msg for keyword in keywords):
            print("✅ Keyword matched. Forwarding message...")
            await client.send_message(destination_channel, event.raw_text)
        else:
            print("❌ No keyword match.")

# Start the client and keep it running
client.start()
print("🚀 Bot is running and listening for messages...")
client.run_until_disconnected()

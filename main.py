import os
from telethon import TelegramClient, events

# Load environment variables
api_id = int(os.environ['API_ID'])
api_hash = os.environ['API_HASH']
channel_id = os.environ['CHANNEL_ID']  # Where to forward filtered messages
keywords = [kw.strip().lower() for kw in os.environ['KEYWORDS'].split(',')]
signal_channel_username = os.environ['SOURCE_CHANNEL']  # e.g. 'KingmakerAISignals'

# Start session using your logged-in account
client = TelegramClient('cjp', api_id, api_hash)

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    # Check if message is from the signal channel
    if event.chat and getattr(event.chat, 'username', '').lower() == signal_channel_username.lower():
        msg = event.raw_text.lower()
        print(f"📩 New message from signal channel: {msg}")

        if any(keyword in msg for keyword in keywords):
            print("✅ Keyword matched. Forwarding message...")
            await client.send_message(channel_id, event.raw_text)
        else:
            print("❌ No keyword match.")
    else:
        pass  # Ignore messages from other chats

async def main():
    print("🔄 Starting filtered signal forwarder...")
    await client.start()
    print("✅ Logged in and listening...")
    await client.run_until_disconnected()

client.loop.run_until_complete(main())

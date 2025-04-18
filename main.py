
import os
from telethon import TelegramClient, events

api_id = int(os.environ['API_ID'])
api_hash = os.environ['API_HASH']
group_id = int(os.environ['GROUP_ID'])
channel_id = os.environ['CHANNEL_ID']
keywords = [kw.strip().lower() for kw in os.environ['KEYWORDS'].split(',')]

client = TelegramClient('cjp', api_id, api_hash)

@client.on(events.NewMessage(chats=group_id))
async def handler(event):
    msg = event.raw_text.lower()
    print(f"📩 Received message: {msg}")
    if any(keyword in msg for keyword in keywords):
        await client.send_message(channel_id, event.raw_text)

client.start()
print("Bot is running...")
client.run_until_disconnected()

import json
from channels.generic.websocket import AsyncWebsocketConsumer
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from hashlib import sha256

# ===== AES ENCRYPT/DECRYPT UTILS (as provided) =====

def get_key(secret: str):
    return sha256(secret.encode()).digest()

def aes_encrypt(text: str, secret: str):
    cipher = AES.new(get_key(secret), AES.MODE_ECB)
    ct_bytes = cipher.encrypt(pad(text.encode(), AES.block_size))
    return base64.urlsafe_b64encode(ct_bytes).decode()

def aes_decrypt(encrypted_text: str, secret: str):
    cipher = AES.new(get_key(secret), AES.MODE_ECB)
    ct = base64.urlsafe_b64decode(encrypted_text)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    return pt.decode()

# ===== WebSocket Consumer =====

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.key = self.scope['url_route']['kwargs']['key']
        self.room_group_name = f'chat_{self.key}'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        nickname = data['nickname']
        raw_message = data['message']

        # 🔐 Encrypt the message before broadcasting
        encrypted_message = aes_encrypt(raw_message, self.key)

        #print(f"[{self.key}] {nickname} sent: {encrypted_message}")

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'nickname': nickname,
                'message': encrypted_message,
            }
        )

    async def chat_message(self, event):
        encrypted_message = event['message']

        # 🔓 Decrypt the message before sending to client
        try:
            decrypted_message = aes_decrypt(encrypted_message, self.key)
        except Exception as e:
            decrypted_message = "[DECRYPTION ERROR]"
            print(f"Decryption failed: {e}")

        await self.send(text_data=json.dumps({
            'nickname': event['nickname'],
            'message': decrypted_message,
        }))

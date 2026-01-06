from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import base64

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from hashlib import sha256


# ===== AES ENCRYPT/DECRYPT UTILS =====

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

# ===== CHAT VIEWS =====

def join_chat(request):
    if request.method == "POST":
        plain_key = request.POST.get("key")
        nickname = request.POST.get("nickname")
        request.session['nickname'] = nickname

        # Encrypt the key using master secret
        encrypted_key = aes_encrypt(plain_key, "chat-master-key")

        return redirect(f'/chat/{encrypted_key}/')
    return render(request, 'onlinechat/join.html')


def chat_room(request, key):
    nickname = request.session.get('nickname')
    if not nickname:
        return redirect('home')

    try:
        room_key = aes_decrypt(key, "chat-master-key")
    except Exception:
        return redirect('home')  # invalid or modified key

    return render(request, 'onlinechat/chat_room.html', {
        'key': room_key,
        'nickname': nickname
    })

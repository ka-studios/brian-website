from fastapi import FastAPI, Request, Response, UploadFile, File
from cryptography.fernet import Fernet
from Crypto.Cipher import AES, DES
from Crypto.Random import get_random_bytes
import hashlib
import os
import json
import base64
import shutil

api = FastAPI()

# Helper function to encrypt data
def encrypt_data(data, key, algorithm):
    if algorithm == "aes256":
        key = hashlib.sha256(key.encode()).digest()
        cipher = AES.new(key, AES.MODE_EAX)
        nonce = cipher.nonce
        ciphertext, tag = cipher.encrypt_and_digest(data)
        return nonce + ciphertext
    elif algorithm == "des":
        key = hashlib.md5(key.encode()).digest()[:8]
        cipher = DES.new(key, DES.MODE_EAX)
        nonce = cipher.nonce
        ciphertext, tag = cipher.encrypt_and_digest(data)
        return nonce + ciphertext
    else:
        raise ValueError("Unsupported algorithm")

# Helper function to decrypt data
def decrypt_data(data, key, algorithm):
    if algorithm == "aes256":
        key = hashlib.sha256(key.encode()).digest()
        nonce = data[:16]
        ciphertext = data[16:]
        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
        return cipher.decrypt(ciphertext)
    elif algorithm == "des":
        key = hashlib.md5(key.encode()).digest()[:8]
        nonce = data[:8]
        ciphertext = data[8:]
        cipher = DES.new(key, DES.MODE_EAX, nonce=nonce)
        return cipher.decrypt(ciphertext)
    else:
        raise ValueError("Unsupported algorithm")

@api.post("/getkey")
async def getkey(response: Response):
    key = Fernet.generate_key()
    return Response(key)

@api.post("/allocate")
async def allocate(request: Request, response: Response):
    data = await request.json()
    username = data.get('username')
    password = data.get('password')
    algorithm = data.get('algorithm')
    key = data.get('key')

    if not all([username, password, algorithm, key]):
        return Response(content="Missing fields", status_code=400)

    if algorithm not in ["aes256", "des"]:
        return Response(content="Unsupported algorithm", status_code=400)

    folder_name = f"{username}-{algorithm}"
    folder_path = f"/var/db/{folder_name}"
    os.makedirs(folder_path, exist_ok=True)

    recovery_key = Fernet.generate_key().decode()
    with open(os.path.join(folder_path, "recovery_key.txt"), "w") as f:
        f.write(recovery_key)

    return Response(content=json.dumps({"recovery_key": recovery_key}), media_type="application/json")

@api.post("/upload")
async def upload_file(request: Request, username: str, algorithm: str, file: UploadFile = File(...)):
    data = await request.form()
    password = data.get('password')

    folder_path = f"/var/db/{username}-{algorithm}"
    if not os.path.exists(folder_path):
        return Response(content="Invalid user or algorithm", status_code=400)

    content = await file.read()
    encrypted_content = encrypt_data(content, password, algorithm)

    with open(os.path.join(folder_path, file.filename), "wb") as f:
        f.write(encrypted_content)

    return Response(content="File uploaded successfully", status_code=200)

@api.get("/files/{username}/{algorithm}")
async def list_files(username: str, algorithm: str):
    folder_path = f"/var/db/{username}-{algorithm}"
    if not os.path.exists(folder_path):
        return Response(content="Invalid user or algorithm", status_code=400)

    files = os.listdir(folder_path)
    files.remove("recovery_key.txt")

    return Response(content=json.dumps(files), media_type="application/json")

@api.get("/download/{username}/{algorithm}/{filename}")
async def download_file(username: str, algorithm: str, filename: str, password: str):
    folder_path = f"/var/db/{username}-{algorithm}"
    if not os.path.exists(folder_path):
        return Response(content="Invalid user or algorithm", status_code=400)

    file_path = os.path.join(folder_path, filename)
    if not os.path.exists(file_path):
        return Response(content="File not found", status_code=404)

    with open(file_path, "rb") as f:
        encrypted_content = f.read()

    decrypted_content = decrypt_data(encrypted_content, password, algorithm)

    return Response(content=decrypted_content, media_type="application/octet-stream")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(api, port=5555)

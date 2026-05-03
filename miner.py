import hashlib
import struct

# Mines a nonce for difficulty 28
def mine(email: str, github_url: str) -> int:
    print("Mining for a valid nonce...")
    nonce = 0
    while True:
        hash_result = hashlib.sha256(email.encode("utf-8") + b"\n" + github_url.encode("utf-8") + b"\n" + struct.pack(">q", nonce)).digest()
        
        if hash_result[0] == 0 and hash_result[1] == 0 and hash_result[2] == 0 and hash_result[3] < 16:
            print("Found a valid nonce:", nonce)
            return nonce
        nonce += 1
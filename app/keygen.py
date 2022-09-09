from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey as EPK
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key
from cryptography import exceptions
import glob, json

class Keys:

    def gen_priv_key(self):
        private_key = EPK.generate()
        return private_key

    def gen_pub_key(self, private_key=None, serialized=False):
        if private_key and serialized:
            public_key = private_key.public_key()
            return self.serialized_public(public_key)
        private_key = self.gen_priv_key()
        return private_key.public_key()

    @staticmethod
    def SHA256(data):
        if isinstance(data, dict):
            data = json.dumps(data).encode()
        digest = hashes.Hash(hashes.SHA256())
        digest.update(data)
        hash = digest.finalize()
        return hash.hex()

    @staticmethod
    def load_pem_private(password):
        password = password.encode()
        with open(".pem", "rb") as f:
            pem_data = f.read()
        private_key = load_pem_private_key(pem_data, password)
        return private_key

    @staticmethod
    def load_pem_public(pem):
        return load_pem_public_key(pem)

    def gen_key_pem(self, password):
        private_key = self.gen_priv_key()
        pem = self.serialized_private(private_key, password)
        with open('.pem', "wb") as pem_in:
            pem_in.write(pem)
        return self.gen_pub_key(private_key, True)

    @staticmethod
    def signMessage(privKey, message):
        try:
            signature = privKey.sign(message)
        except TypeError:
            print("Message must be in bytes")
            return
        return signature

    @staticmethod
    def verify(public_key, message, signature):
        try:
            public_key.verify(signature, message)
            return True
        except exceptions.InvalidSignature:
            return False

    @staticmethod
    def serialized_public(key):
        serialized_public = key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return serialized_public

    @staticmethod
    def serialized_private(key, password=None):
        if password:
            serialized_private = key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.BestAvailableEncryption(password.encode())
                )
            return serialized_private
        else:
            serialized_private = key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
                )
            return serialized_private

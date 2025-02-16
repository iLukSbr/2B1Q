from codecs.binary_converter import BinaryConverter
from codecs.isdn_2b1q import ISDN2B1Q
from codecs.key_manager import KeyManager
from codecs.xor_cipher import XORCipher

binary_converter = BinaryConverter()
key_manager = KeyManager()
xor_cipher = XORCipher(key=key_manager.get_key())
isdn_2b1q = ISDN2B1Q()
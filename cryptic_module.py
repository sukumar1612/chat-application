from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from base64 import b64decode, b64encode

# 1024 means the keysize will be 1024 bits

def encrypt_message(message, public_key):
    message = bytes(message, 'ascii')
    recipient_key=RSA.import_key(public_key)
    cipher = PKCS1_OAEP.new(recipient_key, hashAlgo=SHA256)
    msg=cipher.encrypt(message)
    msg=b64encode(msg)
    return msg

def decrypt_message(message, private_key):
    message = bytes(message, 'ascii')
    message=b64decode(message)
    recipient_key=RSA.import_key(private_key)
    cipher = PKCS1_OAEP.new(recipient_key, hashAlgo=SHA256)
    msg=cipher.decrypt(message)
    return msg


#public = '-----BEGIN PUBLIC KEY-----\r\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQClqUZ+qU/2xjOCI3GekauEjnNu\r\nU1tey0S9ptz3veEo9eCLSBm5A/YOf14cvZyLespVQxx+cS1yBPi0rVX6xlwO3Ae5\r\nvQKEmlJtmJnAuPSWMitJyoBeXLHAfKvy6HHmulTxJ44TxYf+vjK85KShK9Z1Kqf6\r\ns56CS5/FNFNTz0uMgQIDAQAB\r\n-----END PUBLIC KEY-----\r\n'
#private='-----BEGIN RSA PRIVATE KEY-----\r\nMIICXQIBAAKBgQClqUZ+qU/2xjOCI3GekauEjnNuU1tey0S9ptz3veEo9eCLSBm5\r\nA/YOf14cvZyLespVQxx+cS1yBPi0rVX6xlwO3Ae5vQKEmlJtmJnAuPSWMitJyoBe\r\nXLHAfKvy6HHmulTxJ44TxYf+vjK85KShK9Z1Kqf6s56CS5/FNFNTz0uMgQIDAQAB\r\nAoGATyoDTAfw9IZmmuwBIbuO8Tt5oeEnqrcMVGzm72THsmE9OpHr6OQhs2/eM3HQ\r\n2z6EbhYyCaJgCzqg9wZWLg6YcqN6YpqGFtmvXUfaOaiOoiKR29/TGbEk5C0Zd+i5\r\noJB3USkgu/QwSCKBDgfb4bqI4hH5rZ5/IqbrBr2zIdu9XjkCQQDk6F6gaR+EpJAC\r\nhpM34hrhGwKuE4Y4ysyWC6JkHrSzy7mmQpycrTSwZT/7FN8jizEYtzTVnuX5D5ow\r\nuYlPKa+jAkEAuUSdATns2AcJ0Kv1MZ3QTWKfBOROYuuqqPZ+w9en+omHzg0vewUY\r\nqsVCo5t7roURqS6Ok0vd3Of6a60FN4kFiwJBAJugD5VnYvI/H1lYPQalRjj8sBnB\r\nVGOQHP918XW4GoqSWylZ6Dfs2gGDFLiTPBFiNILlK5qAaUGnBeFSgrO7V5kCQBac\r\nFwUVSqA6i6oZsjyx47/t7zYrnp1X4WXpXyMLaIacziQJW+gJgS8mD7Hjwb5Uowkg\r\nk2nKcnMJJHiLjv1uDW0CQQDSFXjqnn4C0WHvr4cBdeU1nF1LaBQDbaAHjLJ7B/bf\r\ngA8ecbRrrx6+yQjjXCP/8cA7Oj9YoNw6sGmiS01CPiCc\r\n-----END RSA PRIVATE KEY-----\r\n'

#x=encrypt_message('hey there how are you', public)
#print(len(x))
#print(decrypt_message(x,private))
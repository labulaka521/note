from django.utils.crypto import get_random_string
import string

CHAR = string.ascii_lowercase
SECRET_LEHGTH = 3


def get_new_sting():
    return get_random_string(SECRET_LEHGTH, allowed_chars=CHAR)

def salt_cipher_secret(secret):
    # 盐的长度是固定的
    salt = get_new_sting()
    pairs = zip((CHAR.index(x) for x in secret), (CHAR.index(x) for x in salt))
    cipher = ''.join(CHAR[(x+y) % len(CHAR)] for x, y in pairs)
    return salt + cipher
token = salt_cipher_secret(get_new_sting())
# print(salt_cipher_secret('abc'))

def unsalt_cipher_secret(token):
    salt = token[:SECRET_LEHGTH]
    token = token[SECRET_LEHGTH:]
    pairs = zip((CHAR.index(x) for x in salt), (CHAR.index(x) for x in token))
    secret = ''.join(CHAR[y-x] for x, y in pairs)
    return secret
unsalt_cipher_secret(token)

secret = get_new_sting()
csrf_cookie = salt_cipher_secret(secret)

print('secret:      ' +  secret)
print('crsf_cookie      ' + csrf_cookie)
print(unsalt_cipher_secret(csrf_cookie))

crsf_token = salt_cipher_secret(secret)
print('secret:      ' +  secret)
print('crsf_token      ' + crsf_token)
print(unsalt_cipher_secret(crsf_token))


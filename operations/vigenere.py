if __name__ == 'operations.vigenere':
	from operations.config import get_from_config
	keyed_alphabet = get_from_config("vigenere_alphabet")
else:
	if __name__ != 'vigenere':
		# we're probably running the testsuite, or something is seriously fucked
		print('WARNING: Vigenere library not importing get_from_config')
		print('If you\'re running the testsuite, everything is fine')
		print('If you\'re not, DEBUG THIS IMMEDIATELY')
	keyed_alphabet = ('TESNX3ABCDFGHIJKLMOPQRUVWYZ012456789')

DEBUG = 0
table = [list('////////////////////////////////////'), list('////////////////////////////////////'),
         list('////////////////////////////////////'), list('////////////////////////////////////'),
         list('////////////////////////////////////'), list('////////////////////////////////////'),
         list('////////////////////////////////////'), list('////////////////////////////////////'),
         list('////////////////////////////////////'), list('////////////////////////////////////'),
         list('////////////////////////////////////'), list('////////////////////////////////////'),
         list('////////////////////////////////////'), list('////////////////////////////////////'),
         list('////////////////////////////////////'), list('////////////////////////////////////'),
         list('////////////////////////////////////'), list('////////////////////////////////////'),
         list('////////////////////////////////////'), list('////////////////////////////////////'),
         list('////////////////////////////////////'), list('////////////////////////////////////'),
         list('////////////////////////////////////'), list('////////////////////////////////////'),
         list('////////////////////////////////////'), list('////////////////////////////////////'),
         list('////////////////////////////////////'), list('////////////////////////////////////'),
         list('////////////////////////////////////'), list('////////////////////////////////////'),
         list('////////////////////////////////////'), list('////////////////////////////////////'),
         list('////////////////////////////////////'), list('////////////////////////////////////'),
         list('////////////////////////////////////'), list('////////////////////////////////////')]
plaintext = list('////////////////////////////////////////////////////////////////////////////////////////////////////')
key = list('////////////////////////////////////////////////////////////////////////////////////////////////////')
ciphertext = list(
    '////////////////////////////////////////////////////////////////////////////////////////////////////')


def generate_alphabet(alphabet):
    offset = 0
    # i is top
    # j is side

    for i in range(0, 36):
        k = 0
        for j in range(0, 36):
            tmp = k + offset
            while tmp > 35:
                if tmp > 35:
                    tmp = tmp - 36
            table[i][j] = alphabet[tmp]
            k = k + 1
        offset = offset + 1


if DEBUG:
    def dbg_print_alphabet():
        print("DEBUG: PRINT VIGENERE TABLE")
        for i in range(0, 36):
            for j in range(0, 36):
                print(table[i][j], end='')
            print('\n')


def extend_key(keyu):
    tmp = int(len(plaintext) / len(keyu))
    tmp2 = int(len(plaintext) % len(keyu))
    global key
    key = keyu * tmp + keyu[:tmp2]


def encrypt():
    for count in range(0, len(plaintext), 1):
        if plaintext[count] == '/':
            return
        j = keyed_alphabet.index(plaintext[count])
        i = keyed_alphabet.index(key[count])
        global ciphertext
        ciphertext[count] = table[i][j]


def decrypt():
    for count in range(0, len(ciphertext), 1):
        if ciphertext[count] == '/':
            return
        j = keyed_alphabet.index(key[count])
        current_row = table[j]
        i = current_row.index(ciphertext[count])
        global plaintext
        plaintext[count] = keyed_alphabet[i]


def set_key(keyl):
    print('DEPRECATED FUNCTION - MOVE ASAP TO EXTEND_KEY()')
    tmp = len(keyl)
    tmp = 100 - tmp
    tmp = '/' * tmp
    global key
    key = list(keyl + tmp)


def set_plaintext(plaintextl):
    tmp = len(plaintextl)
    tmp = 100 - tmp
    tmp = '/' * tmp
    global plaintext
    plaintext = list(plaintextl + tmp)


def get_plaintext():
    return ''.join(plaintext[:plaintext.index('/')])


def set_ciphertext(ciphertextl):
    tmp = len(ciphertextl)
    tmp = 100 - tmp
    tmp = '/' * tmp
    global ciphertext
    ciphertext = list(ciphertextl + tmp)


def get_ciphertext():
    return ''.join(ciphertext[:ciphertext.index('/')])


def set_alphabet():
    print(
        'This function is not implemented by design. In order to set the alphabet please contact vlad557776 on Discord for cipher information (this is for your own sanity so you don\'t debug this for 3 hours because you don\'t know how the cipher works).')
    raise NotImplementedError


def get_alphabet():
    return keyed_alphabet


def encrypt_text(text, encryption_key, alphabet=keyed_alphabet):
    generate_alphabet(alphabet)
    set_plaintext(text)
    extend_key(encryption_key)
    encrypt()
    return get_ciphertext()


if __name__ == "__main__" and DEBUG:
    generate_alphabet(keyed_alphabet)
    dbg_print_alphabet()
    set_plaintext('NUMBERTEST1245780369')
    extend_key('HIDDEN')
    encrypt()
    print(get_ciphertext())
    decrypt()
    print(get_plaintext())
    print(get_alphabet())

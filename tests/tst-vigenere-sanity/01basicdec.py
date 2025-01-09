# NetherX Vigenere library sanity tests
# 00basicenc - checks if basic decryption routines are sane

import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.append(str(HERE / '../../operations'))

from vigenere import *

EXPECT_OUTPUT = 'THISISATEST'

def test():
	generate_alphabet(keyed_alphabet)
	set_ciphertext('TJIX9KAEEXT')
	extend_key('TSTSUITE')
	decrypt()
	return get_plaintext()


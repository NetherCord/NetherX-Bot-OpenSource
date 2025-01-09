# NetherX Vigenere library sanity tests
# 00basicenc - checks if basic encryption routines are sane

import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.append(str(HERE / '../../operations'))

from vigenere import *

EXPECT_OUTPUT = 'THISISANUMTEST2345601789'

def test():
	generate_alphabet(keyed_alphabet)
	set_ciphertext('TJIX9KAXUPTNWI2A4762JF8T')
	extend_key('TSTSUITE')
	decrypt()
	return get_plaintext()

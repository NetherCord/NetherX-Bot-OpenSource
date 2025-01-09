# NetherX Vigenere library sanity tests
# 00basicenc - checks if basic decryption routines are sane

import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.append(str(HERE / '../../operations'))

from vigenere import *

EXPECT_OUTPUT = 'TESNX3ABCDFGHIJKLMOPQRUVWYZ012456789'

def test():
	return get_alphabet()


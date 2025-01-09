# NetherX Vigenere library sanity tests
# 00basicenc - checks if basic encryption routines are sane

import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.append(str(HERE / '../../operations'))

from vigenere import *

EXPECT_OUTPUT = 'TJIX9KAEEXT'

def test():
	return encrypt_text('THISISATEST', 'TSTSUITE')


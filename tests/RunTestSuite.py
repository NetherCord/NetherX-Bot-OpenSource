#!/usr/bin/env python3
import sys
import importlib

print('NetherX TestSuite 1.0')
print('Parsing MANIFEST.py...')
try:
	from MANIFEST import tests
except ImportError:
	print('ERR: MANIFEST not found or corrupt')
	sys.exit(1)

def testmainloop(tests, dir='.'):
	for test in tests:
		if test[1] == 'd':
			print(f'Beginning execution of testsuite {test[0]}')
			try:
				subDirManifest = importlib.import_module(f'{test[0]}.MANIFEST')
			except ImportError:
				print(f'ERR: {test[0]} testsuite MANIFEST not found or corrupt')
				sys.exit(1)
			testmainloop(subDirManifest.tests, test[0])
		elif test[1] == 't':
			testcase = importlib.import_module(f'{dir}.{test[0]}')
			if testcase.EXPECT_OUTPUT != testcase.test():
				print(f'{dir}.{test[0]}: FAIL')
			else:
				print(f'{dir}.{test[0]}: PASS')
		else:
			print(f'ERR: invalid flag in MANIFEST')

testmainloop(tests)
print('TestSuite completed')

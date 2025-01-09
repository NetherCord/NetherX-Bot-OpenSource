# NetherX Test Framework sanity tests
# 01pass - checks if the "fail" feature is sane
# THIS TEST SHOULD FAIL, NOT XFAIL!!!

EXPECT_OUTPUT = 1

def test():
	return 0

from nose.tools import eq_, ok_, istest
import nose

def test_sum():
    eq_(2+2,4)


def test_failing():
    ok_(2+2 == 3, "Expected failure")
    
class TestSuite:
    def test_mult(self):
        eq_(2*2,4)
    @istest  
    def ignored(self):
        eq_(2*2,3)
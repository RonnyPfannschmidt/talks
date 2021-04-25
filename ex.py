import sys
import unittest


a = set("1308")
b = set("8035")


class TestUnittest(unittest.TestCase):
  def test_it(self):
    self.assertEqual(a, b)


def test_plain():
  assert a == b

def test_someinfo():
  assert a == b, (a, b)


def test_sideeffect():
  a = [1]

  assert a.pop() == 2

def test_interesting_missed():
    val = "this could be something very important"
    assert val is None

if __name__ == "__main__":
    globals()[sys.argv[1]]()
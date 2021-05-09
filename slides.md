# annotated assertions

## debugging without kludges


***

## Whoami

* Pytest maintainer
* love approachable debugging


***

### Asserts in python core

```
$ python -m unittest ex.py  -k it
F
======================================================================
FAIL: test_it (ex.TestUnittest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/ronny/Projects/RonnyPfannschmidt/talks/ex.py", line 11, in test_it
    self.assertEqual(a, b)
AssertionError: Items in the first set but not the second:
'1'
Items in the second set but not the first:
'5'

----------------------------------------------------------------------
Ran 1 test in 0.000s

FAILED (failures=1)
```


***

### Asserts in pytest

```
$ pytest ex.py -k side 
==================================================================================================================================================== test session starts =====================================================================================================================================================
platform linux -- Python 3.9.4, pytest-6.2.3, py-1.10.0, pluggy-0.13.1
rootdir: /home/ronny/Projects/RonnyPfannschmidt/talks
collected 5 items / 4 deselected / 1 selected                                                                                                                                                                                                                                                                                

ex.py F                                                                                                                                                                                                                                                                                                                [100%]

========================================================================================================================================================== FAILURES ==========================================================================================================================================================
______________________________________________________________________________________________________________________________________________________ test_sideeffect _______________________________________________________________________________________________________________________________________________________

    def test_sideeffect():
      a = [1]
    
>     assert a.pop() == 2
E     assert 1 == 2
E      +  where 1 = <built-in method pop of list object at 0x7fed6a676d80>()
E      +    where <built-in method pop of list object at 0x7fed6a676d80> = [].pop

ex.py:24: AssertionError
================================================================================================================================================== short test summary info ===================================================================================================================================================
FAILED ex.py::test_sideeffect - assert 1 == 2


```

***

### Mistakes have been made

* pytest prior to `2.1` was reinterpreting assertions


* no example here, not even going to try to install a 10 year old pytest these days ^^


***

### Mistakes are still being made 

```
$ hammett ex.py -k sideeffect
F

Failed: .ex.test_sideeffect
Traceback (most recent call last):
  File ".../site-packages/hammett/impl.py", line 527, in run_test
    resolved_function(**resolved_kwargs)
  File "ex.py", line 24, in test_sideeffect
    assert a.pop() == 2
AssertionError



--- Local variables ---
a:
    []

--- Assert components ---
Failed to analyze assert statement (<class 'IndexError'>: pop from empty list)

0 succeeded, 1 failed, 0 skipped

```

***



### rough idea of What i want to see in  python


```python
def test_sideeffect():
  a = [1]

  assert a.pop() == 2
```

```py3tb
AssertionError: a.pop() == 2
  where:
    `a` was [1]
    `a.pop()` returned 1
    `a` is []
```

```python
def test_interesting_missed():
    val = "this could be something very important"
    assert val is None
```

```text
AssertionError: val is None
  where:
    `val` is "this could be something very important"
```


***

### what pytest does

```python
    # Now actually insert the special imports.
    if sys.version_info >= (3, 10):
        aliases = [
            ast.alias("builtins", "@py_builtins", lineno=lineno, col_offset=0),
            ast.alias(
                "_pytest.assertion.rewrite",
                "@pytest_ar",
                lineno=lineno,
                col_offset=0,
            ),
        ]
    else:
        aliases = [
            ast.alias("builtins", "@py_builtins"),
            ast.alias("_pytest.assertion.rewrite", "@pytest_ar"),
        ]
```

***

### and then ...

many  like this (breaks semi-regular on python updates)
```python

    def visit_Name(self, name: ast.Name) -> Tuple[ast.Name, str]:
        # Display the repr of the name if it's a local variable or
        # _should_repr_global_name() thinks it's acceptable.
        locs = ast.Call(self.builtin("locals"), [], [])
        inlocs = ast.Compare(ast.Str(name.id), [ast.In()], [locs])
        dorepr = self.helper("_should_repr_global_name", name)
        test = ast.BoolOp(ast.Or(), [inlocs, dorepr])
        expr = ast.IfExp(test, self.display(name), ast.Str(name.id))
        return name, self.explanation_param(expr)
```
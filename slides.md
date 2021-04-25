# annotated assertions

## debugging without kludges


***

## Whoami

* Pytest maintainer
* love approachable debugging


***

### Asserts in python core

```python


***

### Asserts in pytest



***

### Mistakes have been made

* pytest prior to `2.1` was reinterpreting assertions






***

### Mistakes are still being made



***



### rough idea of What i want to see


```python
def test_sideeffect():
  a = [1]

  assert a.pop() == 2
```

```text
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

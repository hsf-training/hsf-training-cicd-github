+++
exercises = 5
hidden = false
keypoints = ['You can do whatever you like in a test, as long as you return the right exit code', 'Pytest, and other test utilities will propagate the exit codes correctly']
objectives = ['Understand how assertions in Python correspond to exit codes', 'Figure out how pytest fits in']
questions = ['What happens with assertions in Python?']
teaching = 5
title = 'Being Assertive'
weight = 30
+++
This is a relatively short section, but we need to connect some things you've learned from testing in Python with exit codes.

<!--
{{< youtube Nk1wkQCEPt8 >}}
-->

{{< youtube eeTJdSRqQNg >}}

## Assert Your Tests

An assertion is a sanity-check carried out by the `assert` statement, useful when debugging code.

Let's create a file called `python_assert.py` with the following content:
```python
x = "hello"

assert x == "hello"

assert x == "goodbye"
```

and then run it with `python python_assert.py`.

What happens when an assertion fails in Python?

```text
Traceback (most recent call last):
  File "./python_assert.py", line 5, in <module>
    assert x == "goodbye"
AssertionError
```

An exception is raised: `AssertionError`. The nice thing about Python is that all unhandled exceptions return a non-zero exit code. If an exit code is not set, this defaults to `1`.
```bash
> echo $?
1
```

Ignoring what would cause the assertion to be `True` or `False`, we can see that assertions automatically indicate failure in a script.

## What about pytest?

Pytest, thankfully, handles these assertion failures intuitively. To try this out quickly, go ahead and modify `python_assert.py` as follows:

```python
x = "hello"

def test_assert_success():
    assert x == "hello"

def test_assert_failure():
    assert x == "goodbye"
```

Running `pytest python_assert.py` will produce an expected exit code depending on whether the test passed or failed.
You should be able to confirm that the exit codes are useful here.
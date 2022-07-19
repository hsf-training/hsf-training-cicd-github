---
title: "Being Assertive"
teaching: 5
exercises: 5
objectives:
  - Understand how assertions in python correspond to exit codes
  - Figure out how pytest fits in
questions:
  - What happens with assertions in python?
hidden: false
keypoints:
  - You can do whatever you like in a test, as long as you return the right exit code
  - Pytest, and other test utilities, will propagate the exit codes correctly
---

This is a relatively short section, but we need to connect some things you've learned from testing in python with exit codes.
<iframe width="560" height="315" src="https://www.youtube.com/embed/Nk1wkQCEPt8" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

# Assert Your Tests

An assertion is a sanity-check carried out by the `assert` statement, useful when debugging code.

Let's create a file called `python_assert.py` with the following content:
~~~
x = "hello"

assert x == "hello"

assert x == "goodbye"
~~~
{: .language-python}

and then run it with `python python_assert.py`.

What happens when an assertion fails in python?

~~~
Traceback (most recent call last):
  File "./python_assert.py", line 5, in <module>
    assert x == "goodbye"
AssertionError
~~~
{: .output}

An exception is raised, `AssertionError`. The nice thing about python is that all unhandled exceptions return a non-zero exit code. If an exit code is not set, this defaults to `1`.
~~~
> echo $?
1
~~~
{: .language-bash}

Ignoring what would cause the assertion to be `True` or `False`, we can see that assertions automatically indicate failure in a script.

# What about pytest?

Pytest, thankfully, handles these assertion failures intuitively. To try this out quickly, go ahead and modify `python_assert.py` as follows:

~~~
x = "hello"

def test_assert_success():
    assert x == "hello"

def test_assert_failure():
    assert x == "goodbye"
~~~
{: .language-python}

Running `pytest python_assert.py` will produce an expected exit code depending on whether the test passed or failed.
You should be able to confirm that the exit codes are useful here.

{% include links.md %}

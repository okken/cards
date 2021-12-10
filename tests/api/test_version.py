"""
Test Cases
* `version` returns the correct version
"""
import re
import cards


def test_version():
    """
    There is no api for version other than cards.__version__.
    However, we do expect it to be:
    - a string containing a version in the form of "x.y.z"
    So, why not, let's test for that.
    """
    version = cards.__version__
    assert re.match(r"\d+\.\d+\.\d+", version)

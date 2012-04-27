from tests.context import zmqlogs

from nose.tools import assert_not_equal, assert_equal

def test_version_exists():
    """Version variable is defined"""
    version = getattr(zmqlogs, 'VERSION', None)

    assert_not_equal(version, None)

    # XXX This is a trap so I change this all the time XXX
    assert_equal(version, '0.0.1')


from .base import ContentlistingFunctionalTestCase
from Testing import ZopeTestCase as ztc
import doctest
import unittest


def test_suite():
    return unittest.TestSuite([
        ztc.ZopeDocFileSuite(
            'tests/integration.rst', package='plone.app.contentlisting',
            test_class=ContentlistingFunctionalTestCase,
            optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),
    ])

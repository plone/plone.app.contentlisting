import unittest
import doctest

from Testing import ZopeTestCase as ztc

import base


def test_suite():
    return unittest.TestSuite([
        ztc.ZopeDocFileSuite(
            'tests/integration.txt', package='plone.app.contentlisting',
            test_class=base.ContentlistingFunctionalTestCase,
            optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),
        ])

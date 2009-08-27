"""This is an integration doctest test. It uses PloneTestCase and doctest
syntax.
"""

import unittest
import doctest

from zope.testing import doctestunit
from Testing import ZopeTestCase as ztc

import base

def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above
    """
    return unittest.TestSuite([

        # Here, we create a test suite passing the name of a file relative 
        # to the package home, the name of the package, and the test base 
        # class to use. Here, the base class is a full PloneTestCase, which
        # means that we get a full Plone site set up.

        # The actual test is in integration.txt

        ztc.ZopeDocFileSuite(
            'tests/integration.txt', package='plone.app.contentlisting',
            test_class=base.ContentlistingFunctionalTestCase,
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),
            


        ])

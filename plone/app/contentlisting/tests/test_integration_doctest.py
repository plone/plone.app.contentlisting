from plone.app.contentlisting.tests.base import CONTENTLISTING_FUNCTIONAL_TESTING
from plone.testing import layered

import doctest
import unittest


def test_suite():
    return unittest.TestSuite(
        [
            layered(
                doctest.DocFileSuite(
                    "tests/integration.rst",
                    package="plone.app.contentlisting",
                    optionflags=doctest.NORMALIZE_WHITESPACE
                    | doctest.ELLIPSIS,  # NOQA: E501
                ),
                layer=CONTENTLISTING_FUNCTIONAL_TESTING,
            ),
        ]
    )

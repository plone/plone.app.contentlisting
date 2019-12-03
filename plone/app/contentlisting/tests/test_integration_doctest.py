# -*- coding: utf-8 -*-

from plone.app.contentlisting import IS_PLONE5
from plone.app.contentlisting.tests.base import CONTENTLISTING_FUNCTIONAL_TESTING  # NOQA: E501
from plone.testing import layered

import doctest
import unittest


def test_suite():
    return unittest.TestSuite(
        [
            layered(
                doctest.DocFileSuite(
                    'tests/integration.rst' if IS_PLONE5 else 'tests/integration-p4.rst',
                    package='plone.app.contentlisting',
                    optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS,  # NOQA: E501
                ),
                layer=CONTENTLISTING_FUNCTIONAL_TESTING,
            ),
        ])

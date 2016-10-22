# -*- coding: utf-8 -*-
from plone.app.contentlisting.tests.base import CONTENTLISTING_FUNCTIONAL_TESTING  # noqa
from plone.testing import layered

import doctest
import unittest


def test_suite():
    return unittest.TestSuite([
        layered(doctest.DocFileSuite(
            'tests/integration.rst',
            package='plone.app.contentlisting',
            optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),
            layer=CONTENTLISTING_FUNCTIONAL_TESTING,
        ),
    ])

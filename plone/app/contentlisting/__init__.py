# -*- coding: utf-8 -*-
from Products.CMFPlone.utils import getFSVersionTuple

IS_PLONE5 = getFSVersionTuple()[0] >= 5


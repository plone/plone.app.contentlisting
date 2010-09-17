import unittest

from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting, FunctionalTesting
from zope.configuration import xmlconfig

class ContentListingLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import plone.app.layout
        import plone.app.contentlisting
        xmlconfig.file('configure.zcml', plone.app.layout, context=configurationContext)
        xmlconfig.file('configure.zcml', plone.app.contentlisting, context=configurationContext)


CONTENTLISTING_FIXTURE = ContentListingLayer()
CONTENTLISTING_INTEGRATION_TESTING = IntegrationTesting(bases=(CONTENTLISTING_FIXTURE,), name="ContentListing:Integration")
CONTENTLISTING_FUNCTIONAL_TESTING = FunctionalTesting(bases=(CONTENTLISTING_FIXTURE,), name="ContentListing:Functional")


class ContentlistingTestCase(unittest.TestCase):
    layer = CONTENTLISTING_INTEGRATION_TESTING
    
    @property
    def portal(self):
        return self.layer['portal']

class ContentlistingFunctionalTestCase(ContentlistingTestCase):
    layer = CONTENTLISTING_FUNCTIONAL_TESTING

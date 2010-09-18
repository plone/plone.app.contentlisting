import unittest2 as unittest

from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import TEST_USER_NAME, setRoles
from plone.app.testing import IntegrationTesting, FunctionalTesting
from zope.configuration import xmlconfig


class ContentListingLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import plone.app.layout
        import plone.app.contentlisting
        xmlconfig.file('configure.zcml',
                       plone.app.layout, context=configurationContext)
        xmlconfig.file('configure.zcml',
                       plone.app.contentlisting, context=configurationContext)


CONTENTLISTING_FIXTURE = ContentListingLayer()
CONTENTLISTING_INTEGRATION_TESTING = IntegrationTesting(
    bases=(CONTENTLISTING_FIXTURE,), name="ContentListing:Integration")
CONTENTLISTING_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(CONTENTLISTING_FIXTURE,), name="ContentListing:Functional")


class ContentlistingTestCase(unittest.TestCase):
    layer = CONTENTLISTING_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        setRoles(self.portal, TEST_USER_NAME, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_NAME, ['Member'])

        self.folder = self.portal['test-folder']


class ContentlistingFunctionalTestCase(ContentlistingTestCase):
    layer = CONTENTLISTING_FUNCTIONAL_TESTING

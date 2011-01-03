import unittest2 as unittest

from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import TEST_USER_ID, setRoles
from plone.app.testing import IntegrationTesting, FunctionalTesting
from plone.app.testing import applyProfile
from plone.testing.z2 import installProduct
from zope.configuration import xmlconfig


class ContentListingLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        import plone.app.layout
        import plone.app.contentlisting
        xmlconfig.file('configure.zcml',
                       plone.app.layout, context=configurationContext)
        xmlconfig.file('configure.zcml',
                       plone.app.contentlisting, context=configurationContext)
        # Do we need the workaround for ZopeLite here? This seems unnecessary.
        installProduct(app, 'Products.PythonScripts')

    def setUpPloneSite(self, portal):
        # I don't understand why this first one is needed
        applyProfile(portal, 'Products.CMFPlone:plone')
        applyProfile(portal, 'Products.CMFPlone:plone-content')


CONTENTLISTING_FIXTURE = ContentListingLayer()
CONTENTLISTING_INTEGRATION_TESTING = IntegrationTesting(
    bases=(CONTENTLISTING_FIXTURE, ), name="ContentListing:Integration")
CONTENTLISTING_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(CONTENTLISTING_FIXTURE, ), name="ContentListing:Functional")


class ContentlistingTestCase(unittest.TestCase):
    layer = CONTENTLISTING_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])

        self.folder = self.portal['test-folder']


class ContentlistingFunctionalTestCase(ContentlistingTestCase):
    layer = CONTENTLISTING_FUNCTIONAL_TESTING

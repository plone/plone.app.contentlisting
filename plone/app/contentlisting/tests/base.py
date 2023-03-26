from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.CMFCore.utils import getToolByName


class ContentListingLayer(PloneSandboxLayer):
    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import plone.app.contentlisting

        self.loadZCML(package=plone.app.contentlisting)


CONTENTLISTING_FIXTURE = ContentListingLayer()


class ContentListingIntegrationLayer(PloneSandboxLayer):
    defaultBases = (CONTENTLISTING_FIXTURE,)

    def setUpPloneSite(self, portal):
        setRoles(portal, TEST_USER_ID, ["Manager"])
        wftool = getToolByName(portal, "portal_workflow")
        wftool.setDefaultChain("simple_publication_workflow")

        portal.invokeFactory("Folder", "test-folder")
        portal.invokeFactory("Document", "front-page")
        portal.invokeFactory("Folder", "news")
        wftool.doActionFor(portal.news, "publish")
        portal.news.invokeFactory("News Item", "news1")
        setRoles(portal, TEST_USER_ID, ["Member"])
        from Products.CMFCore.indexing import processQueue

        processQueue()


CONTENTLISTING_INTEGRATION_FIXTURE = ContentListingIntegrationLayer()
CONTENTLISTING_INTEGRATION_TESTING = IntegrationTesting(
    bases=(CONTENTLISTING_INTEGRATION_FIXTURE,),
    name="ContentListing:Integration",
)
CONTENTLISTING_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(CONTENTLISTING_INTEGRATION_FIXTURE,),
    name="ContentListing:Functional",
)

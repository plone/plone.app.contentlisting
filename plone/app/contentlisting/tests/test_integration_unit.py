from plone.app.contentlisting.interfaces import IContentListing
from plone.app.contentlisting.interfaces import IContentListingObject
from plone.app.contentlisting.tests.base import CONTENTLISTING_FUNCTIONAL_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.batching.interfaces import IBatch
from Products.CMFCore.utils import getToolByName
from zope.interface.verify import verifyObject

import unittest


class TestSetup(unittest.TestCase):
    layer = CONTENTLISTING_FUNCTIONAL_TESTING

    def setUp(self):
        super().setUp()
        self.portal = self.layer["portal"]
        self.folder = self.portal["test-folder"]
        self.workflow = getToolByName(self.portal, "portal_workflow")
        self.catalog = getToolByName(self.portal, "portal_catalog")

    def test_able_to_add_document(self):
        # just a dummy test to see that the basics are running
        new_id = self.folder.invokeFactory("Document", "mypage")
        self.assertEqual("mypage", new_id)

    def test_simple_contentlisting(self):
        results = []
        listing = IContentListing(results)
        from plone.app.contentlisting.contentlisting import ContentListing

        self.assertTrue(isinstance(listing, ContentListing))

    def test_making_contentlisting(self):
        results = self.catalog()
        listing = IContentListing(results)
        from plone.app.contentlisting.contentlisting import ContentListing

        self.assertTrue(isinstance(listing, ContentListing))

    def test_making_contentlistingobjects(self):
        results = self.catalog()
        listing = IContentListing(results)
        from plone.app.contentlisting.catalog import CatalogContentListingObject

        self.assertTrue(isinstance(listing[0], CatalogContentListingObject))

    def test_listing_interface(self):
        self.assertTrue(
            verifyObject(
                IContentListing,
                IContentListing(self.catalog()),
            ),
        )

    def test_listing_object_interface(self):
        self.assertTrue(
            verifyObject(
                IContentListingObject,
                IContentListing(self.catalog())[0],
            ),
        )


class TestIndividualCatalogContentItems(unittest.TestCase):
    layer = CONTENTLISTING_FUNCTIONAL_TESTING

    def setUp(self):
        super().setUp()
        self.portal = self.layer["portal"]
        self.folder = self.portal["test-folder"]
        self.folder.invokeFactory(
            "Document",
            "mypage",
            title="My Page",
            description="blah",
        )
        self.item = self.folder.restrictedTraverse("@@folderListing")()[0]
        self.realitem = self.folder.mypage

    def test_printing_item(self):
        self.assertEqual(
            repr(self.item),
            "<plone.app.contentlisting.catalog.CatalogContentListingObject "
            "instance at /plone/test-folder/mypage>",
        )
        self.assertEqual(
            str(self.item),
            "<plone.app.contentlisting.catalog.CatalogContentListingObject "
            "instance at /plone/test-folder/mypage>",
        )

    def test_special_getattr_with_underscore(self):
        # looking up attributes starting with _ should always raise
        # AttributeError
        self.assertRaises(AttributeError, self.item.__getattr__, "foo")

    def test_special_getattr_from_brain(self):
        # Asking for an attribute not in the contentlistingobject, should
        # defer lookup to the brain
        self.assertEqual(self.item.is_folderish, False)
        self.assertTrue(
            repr(self.item.getDataOrigin())[:35],
            "<Products.ZCatalog.Catalog.mybrains",
        )

    def test_special_getattr_from_object(self):
        # Asking for an attribute not in the contentlistingobject, should
        # defer lookup to the brain
        self.assertEqual(self.item.absolute_url(), "")
        self.assertEqual(
            repr(self.item.getDataOrigin()),
            "<Document at /plone/test-folder/mypage>",
        )

    def test_item_Title(self):
        self.assertEqual(self.item.Title(), "My Page")
        self.assertEqual(self.item.Title(), self.realitem.Title())

    def test_item_Description(self):
        self.assertEqual(self.item.Description(), "blah")
        self.assertEqual(self.item.Description(), self.realitem.Description())

    def test_item_Creator(self):
        self.assertEqual(self.item.Creator(), "test_user_1_")

    def test_item_getURL(self):
        self.assertEqual(
            self.item.getURL(),
            "http://nohost/plone/test-folder/mypage",
        )
        self.assertEqual(self.item.getURL(), self.realitem.absolute_url())

    def test_item_getSize(self):
        self.assertEqual(self.item.getSize().upper(), "0 KB")

    def test_item_reviewState(self):
        wftool = getToolByName(self.realitem, "portal_workflow")
        wf = wftool.getInfoFor(self.realitem, "review_state")
        self.assertEqual(self.item.review_state(), wf)

    def test_item_Type(self):
        self.assertEqual(self.item.Type(), "Page")
        self.assertEqual(self.item.Type().domain, "plone")

    def test_appendViewAction(self):
        # checking that we append the view action to urls when needed
        self.assertEqual(self.item.appendViewAction(), "")
        self.folder.invokeFactory(
            "Image",
            "myimage",
            title="My Image",
            description="blah",
        )
        self.item = self.folder.restrictedTraverse("@@contentlisting")()[1]
        self.assertEqual(self.item.appendViewAction(), "/view")

    def test_item_ContentTypeClass(self):
        # checking the that we print nice strings for css class identifiers
        self.assertEqual(self.item.ContentTypeClass(), "contenttype-document")

    def test_comparision(self):
        self.assertEqual(IContentListingObject(self.folder.mypage), self.item)

    def test_containment(self):
        # we can test containment for normal content objects against
        # contentlistings
        self.assertTrue(
            self.folder.mypage in self.folder.restrictedTraverse("@@contentlisting")(),
        )


class TestIndividualRealContentItems(unittest.TestCase):
    layer = CONTENTLISTING_FUNCTIONAL_TESTING

    def setUp(self):
        super().setUp()
        self.portal = self.layer["portal"]
        self.folder = self.portal["test-folder"]
        self.folder.invokeFactory(
            "Document",
            "mypage",
            title="My Page",
            description="blah",
        )
        self.item = IContentListingObject(self.folder.mypage)
        self.realitem = self.folder.mypage

    def test_printing_item(self):
        self.assertEqual(
            repr(self.item),
            "<plone.app.contentlisting.realobject.RealContentListingObject "
            "instance at /plone/test-folder/mypage>",
        )
        self.assertEqual(
            str(self.item),
            "<plone.app.contentlisting.realobject.RealContentListingObject "
            "instance at /plone/test-folder/mypage>",
        )

    def test_special_getattr_with_underscore(self):
        # looking up attributes starting with _ should always raise
        # AttributeError
        self.assertRaises(AttributeError, self.item.__getattr__, "foo")

    def test_special_getattr_from_object(self):
        # Asking for an attribute not in the contentlistingobject, should
        # defer lookup to the brain
        self.assertEqual(self.item.absolute_url(), "")
        self.assertEqual(
            repr(self.item.getDataOrigin()),
            "<Document at /plone/test-folder/mypage>",
        )

    def test_item_Title(self):
        self.assertEqual(self.item.Title(), "My Page")
        self.assertEqual(self.item.Title(), self.realitem.Title())

    def test_item_Description(self):
        self.assertEqual(self.item.Description(), "blah")
        self.assertEqual(self.item.Description(), self.realitem.Description())

    def test_item_Creator(self):
        self.assertEqual(self.item.Creator(), "test_user_1_")

    def test_item_getURL(self):
        self.assertEqual(
            self.item.getURL(),
            "http://nohost/plone/test-folder/mypage",
        )
        self.assertEqual(self.item.getURL(), self.realitem.absolute_url())

    def test_item_getSize(self):
        self.assertEqual(self.item.getSize().upper(), "0 KB")

    def test_item_reviewState(self):
        wftool = getToolByName(self.realitem, "portal_workflow")
        wf = wftool.getInfoFor(self.realitem, "review_state")
        self.assertEqual(self.item.review_state(), wf)

    def test_item_Type(self):
        self.assertEqual(self.item.Type(), "Page")
        self.assertEqual(self.item.Type().domain, "plone")

    def test_item_ContentTypeClass(self):
        # checking the that we print nice strings for css class identifiers
        self.assertEqual(self.item.ContentTypeClass(), "contenttype-document")

    def test_item_uuid(self):
        uuid = self.item.uuid()
        assert uuid
        assert uuid != self.item.getPath()

    def test_item_get_none(self):
        self.realitem.test_none = None
        try:
            self.assertEqual(self.item.test_none, None)
        except AttributeError:
            self.fail(
                "Accessing attributes which return ``None`` should not "
                "result in an AttributeError."
            )


class TestFolderContents(unittest.TestCase):
    """Testing that the folder contents browserview works and behaves
    as it should.
    """

    layer = CONTENTLISTING_FUNCTIONAL_TESTING

    def setUp(self):
        super().setUp()
        self.portal = self.layer["portal"]
        self.folder = self.portal["test-folder"]

    def test_empty_folder_contents(self):
        contentlisting = self.folder.restrictedTraverse("@@contentlisting")()
        self.assertEqual(len(contentlisting), 0)
        self.assertEqual(contentlisting.actual_result_count, 0)

    def test_item_in_folder_contents(self):
        # adding a new page, adds to the length of folder contents
        self.folder.invokeFactory("Document", "mypage")
        contentlisting = self.folder.restrictedTraverse("@@contentlisting")()
        self.assertEqual(len(contentlisting), 1)
        self.assertEqual(contentlisting.actual_result_count, 1)

    def test_folder_contents(self):
        # call the generic folder contents browserview. Check that it makes
        # the results a contentlisting, regardless of batching
        self.folder.invokeFactory("Document", "mypage")
        contentlisting = self.folder.restrictedTraverse("@@contentlisting")()
        self.assertTrue(verifyObject(IContentListing, contentlisting))

    def test_batching_folder_contents(self):
        # call the generic folder contents browserview. Check that it makes
        # the results a contentlisting, regardless of batching
        self.folder.invokeFactory("Document", "mypage")
        contentlisting = self.folder.restrictedTraverse("@@contentlisting")(
            batch=True,
            b_size=1,
        )
        self.assertTrue(verifyObject(IContentListing, contentlisting))
        self.assertEqual(len(contentlisting), 1)

    def test_batching_folder_contents_2(self):
        # call the generic folder contents browserview. Check that it makes
        # the results a contentlisting, regardless of batching
        new_id = self.folder.invokeFactory("Document", "mypage")
        new_id2 = self.folder.invokeFactory("Document", "mypage2")
        contentlisting = self.folder.restrictedTraverse("@@contentlisting")(
            batch=True,
            b_size=1,
        )
        self.assertTrue(contentlisting[0].getId() == new_id)
        self.assertEqual(len(contentlisting), 1)
        self.assertEqual(contentlisting.actual_result_count, 2)

        contentlisting = self.folder.restrictedTraverse("@@contentlisting")(
            batch=True,
            b_size=1,
            b_start=1,
        )
        self.assertEqual(contentlisting[0].getId(), new_id2)
        self.assertEqual(len(contentlisting), 1)
        self.assertEqual(contentlisting.actual_result_count, 2)


class TestCollectionResults(unittest.TestCase):
    """Test, if the @@contentlisting view also works for Collections."""

    layer = CONTENTLISTING_FUNCTIONAL_TESTING

    def setUp(self):
        super().setUp()
        self.portal = self.layer["portal"]
        self.folder = self.portal["test-folder"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.portal.invokeFactory("Collection", "collection", title="Col")
        collection = self.portal.collection
        collection.query = [
            {
                "i": "portal_type",
                "o": "plone.app.querystring.operation.selection.any",
                "v": ["Event", "Event"],
            },
        ]
        collection.reindexObject()
        self.col = collection

    def test_collection_results_is_contentlisting(self):
        # call the generic contentlisting view. Check that it makes results
        # a contentlisting, regardless of batching
        self.folder.invokeFactory("Event", "myevent")
        contentlisting = self.col.restrictedTraverse("@@contentlisting")()

        self.assertTrue(verifyObject(IContentListing, contentlisting))

    def test_filtering_collection_results_to_empty(self):
        contentlisting = self.col.restrictedTraverse("@@contentlisting")(
            portal_type="NotExistent",
        )

        self.assertEqual(len(contentlisting), 0)
        self.assertEqual(contentlisting.actual_result_count, 0)

    def test_filtering_collection_results_to_news_items(self):
        self.folder.invokeFactory("Link", "mylink")
        contentlisting = self.col.restrictedTraverse("@@contentlisting")(
            portal_type="Link",
        )

        self.assertEqual(len(contentlisting), 1)
        self.assertEqual(contentlisting.actual_result_count, 1)
        self.assertEqual(contentlisting[0].portal_type, "Link")

    def test_item_in_collection_results(self):
        self.folder.invokeFactory("Event", "myevent")
        contentlisting = self.col.restrictedTraverse("@@contentlisting")()

        self.assertEqual(len(contentlisting), 1)
        self.assertEqual(contentlisting.actual_result_count, 1)

    def test_batching_collection_results(self):
        # call the contentlisting view. Check that it makes
        # the results a contentlisting, regardless of batching
        self.folder.invokeFactory("Event", "myevent")
        contentlisting = self.col.restrictedTraverse("@@contentlisting")(
            batch=True,
            b_size=1,
        )

        # In case of Collections, the result is a plone.batching object
        self.assertTrue(IBatch.providedBy(contentlisting))
        self.assertTrue(verifyObject(IContentListingObject, contentlisting[0]))
        self.assertEqual(len(contentlisting), 1)

    def test_batching_collection_results_2(self):
        # call the contentlisting view. Check that it makes
        # the results a contentlisting, regardless of batching
        new_id = self.folder.invokeFactory("Event", "myevent")
        new_id2 = self.folder.invokeFactory("Event", "myevent2")
        contentlisting = self.col.restrictedTraverse("@@contentlisting")(
            batch=True,
            b_size=1,
        )

        self.assertTrue(contentlisting[0].getId() == new_id)
        self.assertEqual(contentlisting.items_on_page, 1)
        self.assertEqual(len(contentlisting), 2)
        self.assertEqual(contentlisting.has_next, True)

        contentlisting = self.col.restrictedTraverse("@@contentlisting")(
            batch=True,
            b_size=1,
            b_start=1,
        )

        self.assertEqual(contentlisting[0].getId(), new_id2)
        self.assertEqual(contentlisting.items_on_page, 1)
        self.assertEqual(len(contentlisting), 2)
        self.assertEqual(contentlisting.has_next, False)


def test_suite():
    import unittest

    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    suite.addTest(unittest.makeSuite(TestIndividualCatalogContentItems))
    suite.addTest(unittest.makeSuite(TestIndividualRealContentItems))
    suite.addTest(unittest.makeSuite(TestFolderContents))
    suite.addTest(unittest.makeSuite(TestCollectionResults))
    return suite

"""This is an integration "unit" test. It uses PloneTestCase, but does not
use doctest syntax.

You will find lots of examples of this type of test in CMFPlone/tests, for
example.
"""

import unittest
from base import ContentlistingFunctionalTestCase
from Products.CMFCore.utils import getToolByName
from zope.interface.verify import verifyObject
from plone.app.contentlisting.interfaces import IContentListing
from plone.app.contentlisting.interfaces import IContentListingObject


class TestSetup(ContentlistingFunctionalTestCase):
    """The name of the class should be meaningful. This may be a class that
    tests the installation of a particular product.
    """

    def setUp(self):
        """This method is called before each single test. It can be used to
        set up common state. Setup that is specific to a particular test
        should be done in that test method.
        """
        #   - self.portal is the portal root
        #   - self.folder is the current user's folder
        #   - self.logout() "logs out" so that the user is Anonymous
        #   - self.setRoles(['Manager', 'Member']) adjusts the roles
        #     of the current user
        super(TestSetup, self).setUp()
        self.workflow = getToolByName(self.portal, 'portal_workflow')
        self.catalog = getToolByName(self.portal, 'portal_catalog')

    def beforeTearDown(self):
        """This method is called after each single test. It can be used for
        cleanup, if you need it. Note that the test framework will roll back
        the Zope transaction at the end of each test, so tests are generally
        independent of one another. However, if you are modifying external
        resources (say a database) or globals (such as registering a new
        adapter in the Component Architecture during a test), you may want to
        tear things down here.
        """
        pass

    def test_able_to_add_document(self):
        #just a dummy test to see that the basics are running
        new_id = self.folder.invokeFactory('Document', 'mypage')
        self.assertEquals('mypage', new_id)

    def test_simple_contentlisting(self):
        """get some catalogresults and make an IContentListing out of it"""
        results = []
        listing = IContentListing(results)
        from plone.app.contentlisting.catalog import ContentListing
        self.failUnless(isinstance(listing, ContentListing))

    def test_making_contentlisting(self):
        """get some catalogresults and make an IContentListing out of it"""
        results = self.catalog()
        listing = IContentListing(results)
        from plone.app.contentlisting.catalog import ContentListing
        self.failUnless(isinstance(listing, ContentListing))

    def test_making_contentlistingobjects(self):
        """get some catalogresults and make an IContentListing out of it"""
        results = self.catalog()
        listing = IContentListing(results)
        from plone.app.contentlisting.catalog import CatalogContentListingObject
        self.failUnless(isinstance(listing[0], CatalogContentListingObject))

    def testListingImplementsInterface(self):
        """Check that IContentListing conforms to its interface"""
        self.failUnless(verifyObject(IContentListing,
                                     IContentListing(self.catalog())))

    def testListingObjectsImplementsInterface(self):
        """Check that IContentListingObject conforms to its interface"""
        self.failUnless(verifyObject(IContentListingObject,
                                     IContentListing(self.catalog())[0]))





class TestIndividualCatalogContentItems(ContentlistingFunctionalTestCase):
    """Test the individual methods and code of the contentlisting objects
    """

    def setUp(self):
        """This method is called before each single test. It can be used to
        set up common state. Setup that is specific to a particular test
        should be done in that test method.
        """
        super(TestIndividualCatalogContentItems, self).setUp()
        new_id = self.folder.invokeFactory('Document', 'mypage',
                                           title='My Page', description='blah')
        self.item = self.folder.restrictedTraverse('@@folderListing')()[0]
        self.realitem = self.folder.mypage

    def test_printing_item(self):
        self.assertEqual(repr(self.item), '<plone.app.contentlisting.catalog.CatalogContentListingObject instance at /plone/test-folder/mypage>')
        self.assertEqual(str(self.item), '<plone.app.contentlisting.catalog.CatalogContentListingObject instance at /plone/test-folder/mypage>')

    def test_special_getattr_with_underscore(self):
        """looking up attributes starting with _ should always raise AttributeError"""
        self.assertRaises(AttributeError, self.item.__getattr__,'foo')
        
    def test_special_getattr_from_brain(self):
        """Asking for an attribute not in the contentlistingobject, should defer lookup to the brain"""
        self.assertEqual(self.item.is_folderish,False) 
        self.failUnless(repr(self.item.getDataOrigin())[:35], '<Products.ZCatalog.Catalog.mybrains')

    def test_special_getattr_from_object(self):
        """Asking for an attribute not in the contentlistingobject, should defer lookup to the brain"""
        self.assertEqual(self.item.absolute_url(),'') 
        self.assertEqual(repr(self.item.getDataOrigin()), '<ATDocument at /plone/test-folder/mypage>')

    def test_item_Title(self):
        """checking the Title method"""
        self.assertEqual(self.item.Title(), 'My Page')
        self.assertEqual(self.item.Title(), self.realitem.Title())

    def test_item_Description(self):
        """checking the Description method"""
        self.assertEqual(self.item.Description(), 'blah')
        self.assertEqual(self.item.Description(), self.realitem.Description())

    def test_item_Creator(self):
        self.assertEqual(self.item.Creator(), 'test_user_1_')

    def test_item_getURL(self):
        """checking the getURL method"""
        self.assertEqual(self.item.getURL(), 'http://nohost/plone/test-folder/mypage')
        self.assertEqual(self.item.getURL(), self.realitem.absolute_url())

    def test_item_getIcon(self):
        """checking icons"""
        #since icons were changed to css sprites for most types for Plone 4, this one needs to use an image for the test.
        new_id = self.folder.invokeFactory('Image', 'myimage',
                                           title='My Image', description='blah')
        self.item = self.folder.restrictedTraverse('@@folderListing')()[1]
        self.assertEqual(
            self.item.getIcon(), u'<img width="16" height="16" src="http://nohost/plone/png.png" alt="Image" />')

    def test_item_getSize(self):
        """checking the getSize method"""
        self.assertEqual(self.item.getSize(), '0 kB')

    def test_item_reviewState(self):
        """checking the getSize method"""
        wftool = getToolByName(self.realitem, "portal_workflow")
        wf = wftool.getInfoFor(self.realitem, 'review_state')
        self.assertEqual(self.item.review_state(), wf)

    def test_item_Type(self):
        """checking the Type method"""
        self.assertEqual(self.item.Type(), 'Page')

    def test_appendViewAction(self):
        """checking that we append the view action to urls when needed"""
        self.assertEqual(self.item.appendViewAction(), '')
        new_id = self.folder.invokeFactory('Image', 'myimage',
                                           title='My Image', description='blah')
        self.item = self.folder.restrictedTraverse('@@folderListing')()[1]
        self.assertEqual(self.item.appendViewAction(), '/view')

    def test_item_ContentTypeClass(self):
        """checking the that we print nice strings for css class identifiers"""
        self.assertEqual(self.item.ContentTypeClass(), 'contenttype-page')

    def test_item_Language(self):
        """checking DC Language"""
        self.assertEqual(self.item.Language(), 'en')




    def testComparingContentlistingobjects(self):
        """testing equality"""
        self.assertEqual(IContentListingObject(self.folder.mypage), self.item)

    def testContainment(self):
        """we can test containment for normal content objects against
        contentlistings
        """
        self.failUnless(self.folder.mypage in
                        self.folder.restrictedTraverse('@@folderListing')())








class TestIndividualRealContentItems(ContentlistingFunctionalTestCase):
    """Test the individual methods and code of the contentlisting objects
    """

    def setUp(self):
        """This method is called before each single test. It can be used to
        set up common state. Setup that is specific to a particular test
        should be done in that test method.
        """
        super(TestIndividualRealContentItems, self).setUp()
        new_id = self.folder.invokeFactory('Document', 'mypage',
                                           title='My Page', description='blah')
        self.item = IContentListingObject(self.folder.mypage)
        self.realitem = self.folder.mypage

    def test_printing_item(self):
        self.assertEqual(repr(self.item), '<plone.app.contentlisting.catalog.CatalogContentListingObject instance at /plone/test-folder/mypage>')
        self.assertEqual(str(self.item), '<plone.app.contentlisting.catalog.CatalogContentListingObject instance at /plone/test-folder/mypage>')

    def test_special_getattr_with_underscore(self):
        """looking up attributes starting with _ should always raise AttributeError"""
        self.assertRaises(AttributeError, self.item.__getattr__,'foo')
        
    def test_special_getattr_from_object(self):
        """Asking for an attribute not in the contentlistingobject, should defer lookup to the brain"""
        self.assertEqual(self.item.absolute_url(),'') 
        self.assertEqual(repr(self.item.getDataOrigin()), '<ATDocument at /plone/test-folder/mypage>')

    def test_item_Title(self):
        """checking the Title method"""
        self.assertEqual(self.item.Title(), 'My Page')
        self.assertEqual(self.item.Title(), self.realitem.Title())

    def test_item_Description(self):
        """checking the Description method"""
        self.assertEqual(self.item.Description(), 'blah')
        self.assertEqual(self.item.Description(), self.realitem.Description())

    def test_item_Creator(self):
        self.assertEqual(self.item.Creator(), 'test_user_1_')

    def test_item_getURL(self):
        """checking the getURL method"""
        self.assertEqual(self.item.getURL(), 'http://nohost/plone/test-folder/mypage')
        self.assertEqual(self.item.getURL(), self.realitem.absolute_url())

    def test_item_getIcon(self):
        """checking icons"""
        #since icons were changed to css sprites for most types for Plone 4, this one needs to use an image for the test.
        new_id = self.folder.invokeFactory('Image', 'myimage',
                                           title='My Image', description='blah')
        self.item = self.folder.restrictedTraverse('@@folderListing')()[1]
        self.assertEqual(
            self.item.getIcon(), u'<img width="16" height="16" src="http://nohost/plone/png.png" alt="Image" />')

    def test_item_reviewState(self):
        """checking the getSize method"""
        wftool = getToolByName(self.realitem, "portal_workflow")
        wf = wftool.getInfoFor(self.realitem, 'review_state')
        self.assertEqual(self.item.review_state(), wf)

#    def test_item_Type(self):
#        """checking the Type method"""
#        self.assertEqual(self.item.Type(), 'Page')
#
#    def test_item_ContentTypeClass(self):
#        """checking the that we print nice strings for css class identifiers"""
#        self.assertEqual(self.item.ContentTypeClass(), 'contenttype-page')

    def test_item_Language(self):
        """checking DC Language"""
        self.assertEqual(self.item.Language(), 'en')







class TestFolderContents(ContentlistingFunctionalTestCase):
    """Testing that the folder contents browserview works and behaves
    as it should.
    """

    def test_empty_folder_contents(self):
        """this is a test of the browserview folderlisting"""
        folderlisting = self.folder.restrictedTraverse('@@folderListing')()
        self.assertEqual(len(folderlisting), 0)

    def test_item_in_folder_contents(self):
        """adding a new page, adds to the length of folder contents"""
        new_id = self.folder.invokeFactory('Document', 'mypage')
        folderlisting = self.folder.restrictedTraverse('@@folderListing')()
        self.assertEqual(len(folderlisting), 1)

    def test_folder_contents(self):
        """call the generic folder contents browserview. Check that it makes
        the results a contentlisting, regardless of batching"""
        new_id = self.folder.invokeFactory('Document', 'mypage')
        folderlisting = self.folder.restrictedTraverse('@@folderListing')()
        self.failUnless(verifyObject(IContentListing, folderlisting))

    def test_batching_folder_contents(self):
        """call the generic folder contents browserview. Check that it makes
        the results a contentlisting, regardless of batching"""
        new_id = self.folder.invokeFactory('Document', 'mypage')
        folderlisting = self.folder.restrictedTraverse('@@folderListing')(
            batch=True, b_size=1)
        self.failUnless(verifyObject(IContentListing, folderlisting))
        self.assertEqual(len(folderlisting), 1)

    def test_batching_folder_contents_2(self):
        """call the generic folder contents browserview. Check that it makes
        the results a contentlisting, regardless of batching"""
        new_id = self.folder.invokeFactory('Document', 'mypage')
        new_id2 = self.folder.invokeFactory('Document', 'mypage2')
        folderlisting = self.folder.restrictedTraverse('@@folderListing')(
            batch=True, b_size=1)
        self.assertEqual(len(folderlisting), 1)
        self.failUnless(folderlisting[0].getId() == new_id)

        folderlisting = self.folder.restrictedTraverse('@@folderListing')(
            batch=True, b_size=1, b_start=1)
        self.assertEqual(len(folderlisting), 1)
        self.assertEqual(folderlisting[0].getId(), new_id2)


class TestSearch(ContentlistingFunctionalTestCase):
    """Testing that the search browserview works and behaves as it should
    """

    def setUp(self):
        """This method is called before each single test. It can be used to
        set up common state. Setup that is specific to a particular test
        should be done in that test method.
        """
        super(TestSearch, self).setUp()
        self.workflow = getToolByName(self.portal, 'portal_workflow')
        self.catalog = getToolByName(self.portal, 'portal_catalog')
        new_id = self.folder.invokeFactory('Document', 'mypage')
        new_id2 = self.folder.invokeFactory('Document', 'mypage2')

    def test_search_generates_IContentListing(self):
        """call the generic search browserview. Check that it makes
        the results a contentlisting"""
        searchresultslist = self.folder.restrictedTraverse('@@searchResults')()
        self.failUnless(verifyObject(IContentListing, searchresultslist))

    def test_search_with_no_parameters_returns_empty(self):
        """call the generic search browserview. Check that it makes
        the results a contentlisting"""
        searchresultslist = self.folder.restrictedTraverse('@@searchResults')()
        self.assertEqual(len(searchresultslist), 0)

    def test_search_for_pages(self):
        """search for pages"""
        # this time we search for only pages. We should get 2 results
        searchresultslist = self.folder.restrictedTraverse('@@searchResults')(
            Type="Page")
        self.assertEqual(len(searchresultslist), 3)

    def test_search_with_batching(self):
        """Check that batching works"""
        searchresultslist = self.folder.restrictedTraverse('@@searchResults')(
            batch=True, b_size=1, Type="Page")
        self.failUnless(verifyObject(IContentListing, searchresultslist))
        self.assertEqual(len(searchresultslist), 1)

    def test_search_with_batching_2(self):
        """Check that batching works, also with batch start"""
        # we make 2 queries, one starting at the second batch. Test to
        # make sure we don't get the same result from both queries
        searchresultslist = self.folder.restrictedTraverse('@@searchResults')(
            batch=True, b_size=1, b_start=1, Type="Page")
        firstbatchitem = searchresultslist[0].getId()
        searchresultslist = self.folder.restrictedTraverse('@@searchResults')(
            batch=True, b_size=1, b_start=2, Type="Page")
        secondbatchitem = searchresultslist[0].getId()
        self.assertNotEqual(firstbatchitem, secondbatchitem)


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above
    """
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    suite.addTest(unittest.makeSuite(TestIndividualCatalogContentItems))
    suite.addTest(unittest.makeSuite(TestIndividualRealContentItems))
    suite.addTest(unittest.makeSuite(TestFolderContents))
    suite.addTest(unittest.makeSuite(TestSearch))
    return suite

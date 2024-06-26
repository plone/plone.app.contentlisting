Basic usage
===========

The idea behind plone.app.contentlisting is to have a unified way of listing
Plone content whenever needed, whether in contentlistings, collections,
portlets or search results.

It should be simple to use for new developers and integrators. The core concept
is to take a list of something (in this case a catalog result set) and turn it
into an IContentListing so that the user always knows what to expect.

    >>> from zope import interface
    >>> from plone.app.contentlisting.interfaces import IContentListing, IContentListingObject
    >>> from Products.CMFCore.utils import getToolByName

We simply adapt a sequence of something content-like. In this case (and most
common cases) the sequence will be a catalog search result set.

    >>> portal = layer['portal']
    >>> catalog = getToolByName(portal, 'portal_catalog')
    >>> results = catalog.searchResults(dict(is_default_page=False, getId={"not":"plone"}))
    >>> contentlist = IContentListing(results)
    >>> print(contentlist)
    <plone.app.contentlisting.contentlisting.ContentListing object ...>

We get a ContentListing. That is the catalog based implementation of
IContentListing. In other cases you might get a different implementations,
but they should all conform to the rules of the interface.

The contentListing is a normal iterator that we can loop over. Each entry is
a CatalogContentListingObject

    >>> listitem = contentlist[2]
    >>> print(listitem)
    <plone.app.contentlisting.catalog.CatalogContentListingObject instance ...>

The listitem provides all the methods of the IContentListingObject interface

    >>> print(listitem.review_state())
    published

It can report what its source of data is

    >>> print(listitem.getDataOrigin())
    <Products.ZCatalog.Catalog...mybrains object at...>

and if we access attributes on it that are not in the interface or in the
brain, it will transparently fetch the real object and cache it to get
properties from that instead.

After accessing an attribute of the object that was neither in the
IContentListingObject or on the catalog brain, we can now see that the
real object has been silently fetched in the background. getDataOrigin now
returns the object.

    >>> dummy= listitem.absolute_url()
    >>> print(listitem.getDataOrigin())
    <Folder at news>

This item's origin is no longer a Brain, but the real object

    >>> listitem.review_state()
    'published'

For user and integrator convenience we also include a couple of handy
browser views to get to these listings.

    >>> contentlisting = portal.restrictedTraverse('@@contentlisting')()
    >>> print(contentlisting)
    <plone.app.contentlisting.contentlisting.ContentListing object ...

    >>> len(contentlisting)
    3

We can even slice the new contentlisting

    >>> len (contentlisting[2:4])
    1

    >>> len(portal.restrictedTraverse('news/@@contentlisting')())
    1

And we can use batching in it:

    >>> [i.getURL() for i in portal.restrictedTraverse('@@contentlisting')()]
    ['http://nohost/plone/test-folder', 'http://nohost/plone/front-page', 'http://nohost/plone/news']
    >>> [i.getURL() for i in portal.restrictedTraverse('@@contentlisting')(batch=True, b_size=1)]
    ['http://nohost/plone/test-folder']
    >>> [i.getURL() for i in portal.restrictedTraverse('@@contentlisting')(batch=True, b_start=1, b_size=1)]
    ['http://nohost/plone/front-page']
    >>> [i.getURL() for i in portal.restrictedTraverse('@@contentlisting')(batch=True, b_start=2, b_size=1)]
    ['http://nohost/plone/news']
    >>> [i.getURL() for i in portal.restrictedTraverse('@@contentlisting')(batch=True, b_start=1, b_size=2)]
    ['http://nohost/plone/front-page', 'http://nohost/plone/news']

We can use filtering by catalog indexes:
    >>> len(portal.restrictedTraverse('@@contentlisting')(portal_type='Document'))
    1


Append View Action
==================

Some types may require '/view' appended to their URLs. Currently these don't

    >>> frontpage = portal.restrictedTraverse('@@contentlisting')(id='front-page')[0]
    >>> frontpage.appendViewAction()
    ''
    >>> news = portal.restrictedTraverse('@@contentlisting')(id='news')[0]
    >>> news.appendViewAction()
    ''
    >>> realfrontpage = IContentListingObject(portal['front-page'])
    >>> realfrontpage.appendViewAction()
    ''

By altering the configuration registry, we can make this true for Documents

    >>> registry = portal.portal_registry
    >>> registry['plone.types_use_view_action_in_listings'] = [str(frontpage.portal_type)]

    >>> frontpage.appendViewAction()
    '/view'
    >>> news.appendViewAction()
    ''
    >>> realfrontpage.appendViewAction()
    '/view'

And turn it off again

    >>> registry['plone.types_use_view_action_in_listings'] = []
    >>> frontpage.appendViewAction()
    ''
    >>> news.appendViewAction()
    ''
    >>> realfrontpage.appendViewAction()
    ''


Visibility in Navigation
========================

Items by default are visible in navigation

    >>> frontpage = portal.restrictedTraverse('@@contentlisting')(id='front-page')[0]
    >>> frontpage.isVisibleInNav()
    True

    >>> news = portal.restrictedTraverse('@@contentlisting')(id='news')[0]
    >>> news.isVisibleInNav()
    True

Just to check, these will be catalog objects using a brain internally

    >>> frontpage.__class__
    <class 'plone.app.contentlisting.catalog.CatalogContentListingObject'>
    >>> print(frontpage.getDataOrigin())
    <Products.ZCatalog.Catalog...mybrains object at...>
    >>> frontpage.isVisibleInNav()
    True

A catalog object with a real object works

    >>> dummy= listitem.absolute_url()
    >>> print(listitem.getDataOrigin())
    <Folder at news>
    >>> frontpage.isVisibleInNav()
    True

Getting a realobject-based listing also works

    >>> realfrontpage = IContentListingObject(portal['front-page'])
    >>> realfrontpage.__class__
    <class 'plone.app.contentlisting.realobject.RealContentListingObject'>
    >>> realfrontpage.isVisibleInNav()
    True

There are several ways something can be hidden from navigation, the most direct
way is the exclude_from_nav property being true

    >>> frontpage_object = frontpage.getObject()
    >>> frontpage_object.exclude_from_nav = True
    >>> frontpage_object.reindexObject()

This will be indexed, so an object isn't necessary to check this

    >>> frontpage = portal.restrictedTraverse('@@contentlisting')(id='front-page')[0]
    >>> frontpage.isVisibleInNav()
    False
    >>> print(frontpage.getDataOrigin())
    <Products.ZCatalog.Catalog...mybrains object at...>

But a real object still works.

    >>> realfrontpage = IContentListingObject(portal['front-page'])
    >>> realfrontpage.__class__
    <class 'plone.app.contentlisting.realobject.RealContentListingObject'>
    >>> realfrontpage.isVisibleInNav()
    False

We can also turn it off again.

    >>> frontpage_object.exclude_from_nav = False
    >>> frontpage_object.reindexObject()

    >>> frontpage = portal.restrictedTraverse('@@contentlisting')(id='front-page')[0]
    >>> frontpage.isVisibleInNav()
    True

    >>> realfrontpage = IContentListingObject(portal['front-page'])
    >>> realfrontpage.isVisibleInNav()
    True

We can also exclude anything of a particular type using the displayed type setting::

    >>> from plone.registry.interfaces import IRegistry
    >>> from zope.component import getUtility
    >>> registry = getUtility(IRegistry)
    >>> from plone.base.interfaces import INavigationSchema
    >>> navigation_settings = registry.forInterface(
    ...     INavigationSchema,
    ...     prefix='plone'
    ... )
    >>> navigation_settings.displayed_types = (frontpage.portal_type, news.portal_type)
    >>> frontpage.isVisibleInNav()
    True
    >>> realfrontpage.isVisibleInNav()
    True
    >>> news.isVisibleInNav()
    True
    >>> navigation_settings.displayed_types = ()
    >>> frontpage.isVisibleInNav()
    False
    >>> realfrontpage.isVisibleInNav()
    False
    >>> news.isVisibleInNav()
    False

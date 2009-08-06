======================
Basic usage
======================

The idea behind plone.app.contentlisting is to have a unified way of listing 
Plone content whenever needed, whether in folderlistings, collections, 
portlets, search results. 

It should be simple to use for new developers and integrators

    >>> from zope import interface
    >>> from plone.app.contentlisting.interfaces import IContentListing
    >>> from Products.CMFCore.utils import getToolByName

We simply ask for an IContentLister for a sequence. In this case (and most common cases) the sequence is a catalog search result set.

    >>> catalog = getToolByName(self.portal, 'portal_catalog')
    >>> results = catalog.searchResults()
    >>> contentlist = IContentListing(results)
    >>> print contentlist 
    <plone.app.contentlisting.catalog.CatalogContentListing instance at ...>

In this case, we get a CatalogContentListing. That's the catalog based implementation of IContentListing.
In other cases you might get a different type, but they should all conform to the rules of the interface.

The contentListing is a normal iterator that we can loop over. Each entry is a CatalogContentListingObject

    >>> listitem = contentlist[3]
    >>> print listitem
    <plone.app.contentlisting.catalog.CatalogContentListingObject instance>

The listitem provides all the methods of the IContentListingObject interface

    >>> print listitem.review_state()
    published

It can report what its source of data is

    >>> print listitem.getDataOrigin()
    Catalog brain
    
and if we access attributes on it that are not in the interface or in the brain, it will transparently 
fetch the real object and cache it to get properties from that instead

    >>> f = listitem.absolute_url()
    >>> print listitem.getDataOrigin()
    Real object
    
    >>> print listitem.getIcon()
    ...
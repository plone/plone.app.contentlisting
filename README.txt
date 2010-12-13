==========================================================================
Listing and working with Plone content objects using plone.app.contentlistings
==========================================================================
This is valid for Plone 4.1 upwards.

Many of the operations for customisations, templates, views and portlets in Plone are related to lists of content objects. Their sources can be different, although usually they are some sort of catalog search, the contents of a particular folder or a list of objects from a relation. 

To make it simpler to work with these, we have made plone.app.contentlisting, which ensures that lists of content objects always behave in the same way and according to predefined interfaces, regardless of what the source of the objects are. The integrator shouldn't have to care whether the list of objects came from the catalog, and ORM or they are the actual objects.


=====================================
Making or getting a contentListing
=====================================

The typical way to get a contentlisting is to call one of two built-in views:

A ContentListing of a particular folder's contents can be fetched by using: 
    >>> path.to.your.folder.restrictedTraverse('@@folderListing')() 


or, to search outside a single folder:
    >>> some.context.restrictedTraverse('@@searchResults')()

At the time of writing, all parts of Plone do not yet return 'contentlistings' when asked for lists of content. It was impossible to change this everywhere without breaking backwards compatibility. Therefore you may have to convert your sequence of stuff to a contentlisting manually. 

To do this, you need to import and adapt

    >>> from plone.app.contentlisting.interfaces import IContentListing
    >>> catalog = getToolByName(self.portal, 'portal_catalog')
    >>> results = catalog.searchResults()
    >>> contentlist = IContentListing(results)
    >>> print contentlist 
    <plone.app.contentlisting.contentlisting.ContentListing instance ...>


Now, you no longer need to worry whether you have a bunch of catalog brains or the actual objects (or fake objects for that sake). As long as you have a contentlisting, you know what you can expect from it. You also know what you can expect from each item within it: a contentListingObject

The contentListing is a normal iterator that we can loop over and do all sorts of stuff you normally can do with sequences. 






======================
Basic usage
======================

The idea behind plone.app.contentlisting is to have a unified way of listing 
Plone content whenever needed, whether in folderlistings, collections, 
portlets, search results. 

It should be simple to use for new developers and integrators

    
    >>> from plone.app.contentlisting.interfaces import IContentListingFactory

We simply ask for an IContentLister for a given context. In this case the context is a folder. 
The component architecture will take care to give us the right one for our context. 

    >>> mylister = IContentListingFactory(self.folder)
    >>> print mylister
    <plone.app.contentlisting.catalog.CatalogContentListingFactory object at ...>

In this case, we get a CatalogContentListingFactory. That's the catalog-based implementation of IContentListingFactory. 
In other cases you might get a different type, but they should all conform to the rules of the interface.


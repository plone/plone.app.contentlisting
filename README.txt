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

----------------------------------
Listing the contents of a folder
-----------------------------------


In Page templates

getting the contents of a folder is as simple as this 

    context/folderListing

Every template-writer's dream ;)

A real example of listing the titles of the content objects of a folder:

<ul>
  <li tal:repeat="item context/folderListing" tal:content="item/Title"/>
</ul>

The context in which it is called defines which folder is listed.

You can also use python expression to be able to pass parameters, like which content type or review state you want to use:

 <li tal:repeat="item python:context.folderListing(Type='Page')"





In Python

A ContentListing of a particular folder's contents can be fetched by using: 
    >>> path.to.your.folder.restrictedTraverse('@@folderListing')() 

The folderListing view called above implements all the logic the old getFolderContents script in Plone used to do. The old script has been left in place to not break compatibility for customisations and add-ons that might depend on its particular return values. 


----------------------------------
Making a search
-----------------------------------
To search outside a single folder:
    >>> context.restrictedTraverse('@@searchResults')()

the searchResults view can take the same parameters as you would normally pass to the portal_catalog. 

for example:

    >>> context.restrictedTraverse('@@searchResults')(Type='Page')

Consult the catalog documentation for further information on how to query the catalog for specifics. 


-----------------------------------------------------
getting a contentlisting directly from a template
-----------------------------------------------------
…
…
…





--------------------------------
Rolling your own with adaption
---------------------------------
At the time of writing, all parts of Plone do not yet return 'contentlistings' when asked for lists of content. It was impossible to change this everywhere without breaking backwards compatibility. Therefore you may have to convert your sequence of stuff to a contentlisting manually. 

To do this, you need to import and adapt

    >>> from plone.app.contentlisting.interfaces import IContentListing
    >>> catalog = getToolByName(self.portal, 'portal_catalog')
    >>> results = catalog.searchResults()
    >>> contentlist = IContentListing(results)
    >>> print contentlist 
    <plone.app.contentlisting.contentlisting.ContentListing object ...>

=====================================================
The contentListing, its properties and behaviors
=====================================================

Now, you no longer need to worry whether you have a bunch of catalog brains or the actual objects (or fake objects for that sake). As long as you have a contentlisting, you know what you can expect from it. You also know what you can expect from each item within it: a contentListingObject

The contentListing is a normal iterator that we can loop over and do all sorts of stuff you normally can do with sequences. 




=====================================================
contentListingObjects, the items in the sequence 
=====================================================

How do they work?…
…
…




-------------------------------------
Methods of contentlistingObjects
-------------------------------------







------------------------------------------
Usage example directly from a template
------------------------------------------









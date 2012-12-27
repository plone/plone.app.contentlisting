=============================================================================
Listing and working with Plone content objects using plone.app.contentlisting
=============================================================================

This is valid for Plone 4.1 upwards.

Many of the operations for customizations, templates, views and portlets in
Plone are related to lists of content objects. Their sources can be different,
although usually they are some sort of catalog search, the contents of a
particular folder or a list of objects from a relation.

To make it simpler to work with these, we have made plone.app.contentlisting,
which ensures that lists of content objects always behave in the same way and
according to predefined interfaces, regardless of what the source of the
objects are. The integrator shouldn't have to care whether the list of objects
came from the catalog, an ORM or they are the actual objects.

==================================
Making or getting a contentListing
==================================

The typical way to get a contentlisting is to call one of two built-in views:

--------------------------------
Listing the contents of a folder
--------------------------------

In Page templates getting the contents of a folder is as simple as this::

  context/@@folderListing

Every template-writer's dream ;)

A real example of listing the titles of the content objects of a folder::

  <ul>
    <li tal:repeat="item context/@@folderListing" tal:content="item/Title"/>
  </ul>

The context in which it is called defines which folder is listed.

You can also use Python expressions to be able to pass parameters, like which
content type or review state you want to use::

  <li tal:repeat="item python:context.restrictedTraverse('@@folderListing')(portal_type='Document')">

In Python a ContentListing of a particular folder's contents can be fetched
by using::

    >>> path.to.your.folder.restrictedTraverse('@@folderListing')()

The folderListing view called above implements all the logic the old
getFolderContents script in Plone used to do. The old script has been left in
place to not break compatibility for customizations and add-ons that might
depend on its particular return values.

------------------------------
Rolling your own with adaption
------------------------------

At the time of writing, all parts of Plone do not yet return 'contentlistings'
when asked for lists of content. It was impossible to change this everywhere
without breaking backwards compatibility. Therefore you may have to convert
your sequence of stuff to a contentlisting manually.

To do this, you need to import and adapt::

    >>> from plone.app.contentlisting.interfaces import IContentListing
    >>> catalog = getToolByName(self.portal, 'portal_catalog')
    >>> results = catalog.searchResults()
    >>> contentlist = IContentListing(results)
    >>> print(contentlist)
    <plone.app.contentlisting.contentlisting.ContentListing object ...>

================================================
The contentListing, its properties and behaviors
================================================

Now, you no longer need to worry whether you have a bunch of catalog brains or
the actual objects (or fake objects for that sake). As long as you have a
contentlisting, you know what you can expect from it. You also know what you
can expect from each item within it - a content listing object.

The content listing is a normal iterator that we can loop over and do all sorts
of stuff you normally can do with sequences.

====================================================
contentListingObjects, the items inside the sequence
====================================================

The `contentListingObjects` are wrapper objects, each representing a content
object in the site. Their intention is to be predictable so you can always call
at least a common base set of methods on the objects listed.

You do not have to be aware whether the object originates from a brain, a full
object or something else. If you try to call a method or access an attribute of
the object and the wrapper is not aware of it, it will silently fetch the real
object and delegate the call to it. This means you can treat your objects as
you would any other -- even writing to it.

--------------------------------
Methods of contentlistingObjects
--------------------------------

getId() -
  Returns the object id in its container for example `my-example-page`.

getObject() -
  Returns the real object

getPath() -
  Path to the object, relative to the site root for example
  ``/artifacts/my-example-page``

getURL()- 
  Full url to the object, including the site root for example
  ``http://my.site.com/artifacts/my-example-page``

uuid() -
  Unique content identifier for example an uuid from `plone.uuid` The only real
  point of it is to be unique. It can for example look like this
  `b0e80776-d41d-4f48-bf9e-7cb1aebabad5`.

getIcon() -
  Icon for the object. Returns an icon object from plone.app.layout.
  If printed as a string, it will produce an HTML tag for the icon. Check
  plone.app.layout for more info.

getSize() -
  Size in bytes for example `24`.

review_state() -
  Workflow review state for example `published`.

ContentTypeClass() -
  A normalized type name that identifies the object in listings. Used for CSS
  styling, for example `content-type-page`.

Title() -
  Return a single string, the DCMI Title element (resource name).
  For example `My example page`.

Description() -
  Return the DCMI Description element (resource summary). Result is a natural
  language description of this object. Description is a plain text string
  describing the object. It should not contain HTML or similar.

Type() -
  Return the DCMI Type element (resource type). Result is a human-readable
  message id for the resource (typically the Title of its type info object).
  For example `u'Page'` from the `plone` domain.

listCreators() -
  Return a sequence of DCMI Creator elements (resource authors).
  Depending on the implementation, this returns the full name(s) of the
  author(s) of the content object or their ids. For example `Jane Smith`.

Creator() -
  Return the first DCMI Creator element, or an empty string.
  For example `Jane Smith`.

Subject() -
  Return a sequence of DCMI Subject elements (resource keywords).
  Result is zero or more keywords associated with the content object.
  These are the tags in Plone. For example ``['Ecology', 'Sustainability']``.

Publisher() -
  Return the DCMI Publisher element (resource publisher). Result is the full
  formal name of the entity or person responsible for publishing the resource.
  For example `Plone Foundation`.

listContributors() -
  Return a sequence of DCMI Contributor elements (resource collaborators).
  Return zero or more collaborators (beyond those returned by `listCreators`).

Contributors() -
  Deprecated alias for `listContributors`.

Date(zone=None) -
  Return the DCMI Date element (default resource date). Result is a string,
  formatted 'YYYY-MM-DD H24:MN:SS TZ'. The zone keyword is not yet supported
  (but is part of the DublinCore interface and has to stay)

CreationDate(zone=None) -
  Return the DCMI Date element (date resource created). Result is a string,
  formatted 'YYYY-MM-DD H24:MN:SS TZ'. The zone keyword is not yet supported
  (but is part of the DublinCore interface and has to stay)

EffectiveDate(zone=None) -
  Return the DCMI Date element (date resource becomes effective). Result is a
  string, formatted 'YYYY-MM-DD H24:MN:SS TZ', or None. The zone keyword is
  not yet supported (but is part of the DublinCore interface and has to stay)

ExpirationDate(zone=None) -
  Return the DCMI Date element (date resource expires). Result is a string,
  formatted 'YYYY-MM-DD H24:MN:SS TZ', or None. The zone keyword is not yet
  supported (but is part of the DublinCore interface and has to stay)

ModificationDate(zone=None) -
  DCMI Date element - date resource last modified. Result is a string,
  formatted 'YYYY-MM-DD H24:MN:SS TZ'. The zone keyword is not yet supported
  (but is part of the DublinCore interface and has to stay)

Format() -
  Return the DCMI Format element (resource format).
  Result is the resource's MIME type (e.g. `text/html`, `image/png`, etc.).

Identifier() -
  Return the DCMI Identifier element (resource ID). Result is a unique ID
  (a URL) for the resource.

Language() -
  DCMI Language element (resource language). Result it the RFC language code
  (e.g. `en-US`, `pt-BR`) for the resource.

Rights() -
  Return the DCMI Rights element (resource copyright). Return a string
  describing the intellectual property status, if any, of the resource.

isVisibleInNav() -
  Return whether this object will be visible in a navigation view.

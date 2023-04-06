Changelog
=========

.. You should *NOT* be adding new change log entries to this file.
   You should create a file in the news directory instead.
   For helpful instructions, please see:
   https://github.com/plone/plone.releaser/blob/master/ADD-A-NEWS-ITEM.rst

.. towncrier release notes start

3.0.2 (2023-04-06)
------------------

Internal:


- Update configuration files.
  [plone devs] (#47959565)


3.0.1 (2022-12-05)
------------------

Bug fixes:


- In RealContentListingObject.__getattr__ check attribute existence without acquisition but return the attribute with acquisition in case it is a method that needs acquisition. [gbastien] (#47)


3.0.0 (2022-11-30)
------------------

Bug fixes:


- Final release.
  [gforcada] (#600)


3.0.0b1 (2022-08-30)
--------------------

Bug fixes:


- Build mime-type icon url with the absolute url. Fixes #44
  [erral] (#44)


3.0.0a1 (2022-05-14)
--------------------

Breaking changes:


- Drop Python 2 and Plone 5.2, use plone.base.
  [jensens] (#43)


2.0.7 (2022-03-09)
------------------

Bug fixes:


- realobject: Do not throw an AttributeError when accessing attributes which return ``None``. (#42)


2.0.6 (2022-01-07)
------------------

Bug fixes:


- Do not throw an error when the contenttype is not in the mimetypes_registry.
  [tschorr] (#41)


2.0.5 (2021-11-23)
------------------

Bug fixes:


- Adapt the tests for Plone 6 [ale-rt] (#39)


2.0.4 (2021-09-15)
------------------

Bug fixes:


- Remove cyclic dependency with Products.CMFPlone
  [ericof] (#37)


2.0.3 (2020-09-26)
------------------

Bug fixes:


- Fixed deprecation warning for LazyCat/LazyMap.
  [maurits] (#3130)


2.0.2 (2020-04-20)
------------------

Bug fixes:


- Minor packaging updates. (#1)


2.0.1 (2020-03-21)
------------------

Bug fixes:


- Minor packaging updates. [various] (#1)
- Initialize towncrier.
  [gforcada] (#2548)


2.0.0 (2018-10-30)
------------------

Breaking changes:

- Remove Python2.6 support.
  [ale-rt]

New features:

- Python 3 support
  [hvelarde, gforcada, davisagli]
- Use human_readable_size from Products.CMFPlone.utils to replace getObjSize
  script. #1801
  [reinhardt]

Bug fixes:

- In Zope4 brains can not longer acquire the REQUEST.
  [pbauer]

- Fix tests after collective.indexing moved into core.
  [pbauer]


1.3.1 (2017-08-08)
------------------

Bug fixes:

- fixes code conventions
  [loechel]

- Fix Lookup of review_state on objects that do not have an review_state, example related_items that are files could be such.
  [loechel]


1.3.0 (2017-07-03)
------------------

New features:

- provide Mimetype icon path for file types in contentlisting object
  https://github.com/plone/Products.CMFPlone/issues/1734
  [fgrcon]


1.2.9 (2017-05-06)
------------------

Bug fixes:

- Remove hasattr.
  [ivanteoh]


1.2.8 (2016-11-19)
------------------

Bug fixes:

- Remove ZopeTestCase.
  [ivanteoh, maurits]


1.2.7 (2016-08-19)
------------------

Bug fixes:

- Make ``getSize`` work on RealContentListingObject on types w/o any Primaryfield.
  [jensens]


1.2.6 (2016-07-05)
------------------

Bug fixes:

- Added missing implementation for getSize on RealContentListingObject.
  Interface was not fulfilled here.
  [jensens]


1.2.5 (2016-05-12)
------------------

Fixes:

- Removed docstrings from some methods to avoid publishing them.  From
  Products.PloneHotfix20160419.  [maurits]


1.2.4 (2016-02-08)
------------------

Fixes:

- Minor cleanup (decorator, utf8 header, ...), removed unused imports and
  fixed dependencies.
  [jensens]


1.2.3 (2015-11-25)
------------------

Fixes:

- In tests, use ``selection.any`` in querystrings.
  Issue https://github.com/plone/Products.CMFPlone/issues/1040
  [maurits]

- Cleanup and rework: contenttype-icons and showing thumbnails
  for images/leadimages in listings
  https://github.com/plone/Products.CMFPlone/issues/1226
  [fgrcon]


1.2.2 (2015-09-20)
------------------

- ids_not_to_list has been removed. Use the exclude from navigation
  setting instead.
  [jensens]


1.2.1 (2015-09-11)
------------------

- Implement cropping for CroppedDescription.
  [pbauer]


1.2 (2015-07-18)
----------------

- Introduce ``@@contentlisting`` view, which is also supports Collections from
  plone.app.contenttypes including filtering of results. This gives us a
  unified interface for listing content from Folders or Collections.
  Deprecate ``@@folderListing``, which is kept for BBB compatibility.
  [thet]


1.1.3 (2015-05-05)
------------------

- Make isVisibleInNav method read navigation displayed types settings from
  plone.app.registry instead of portal properties. This fixes
  https://github.com/plone/Products.CMFPlone/issues/454.
  [timo]


1.1.2 (2015-05-05)
------------------

- Pep8.
  [thet]


1.1.1 (2015-03-13)
------------------

- Add remaining, implemented but missing IContentListing interface methods.
  [thet]

- forward getURL's relative kw for contentlistings (plone4 compat)
  [kiorky]


1.1.0 (2014-04-16)
------------------

- Use proper styleguide for headings.
  [polyester]

- Move README to /docs folder.
  [polyester]

- Replace deprecated test assert statements.
  [tisto]

- Removing language tests and fixing icon tests to get the correct images.
  [bloodbare]

- Use PLONE_APP_CONTENTTYPES fixture for Plone 5.
  [tisto]


1.0.5 (2013-08-13)
------------------

- Add missing getDataOrigin method to interfaces.
  [timo]


1.0.4 (2013-01-01)
------------------

- Nothing changed.


1.0.3 (2012-10-29)
------------------

- Whoever heard I liked batching was wrong. The Catalog results are
  already batched, so don't batch them again.
  [lentinj]


1.0.2 (2012-10-15)
------------------

- Nothing changed.


1.0.1 (2012-04-15)
------------------

- Change ContentTypeClass to return contenttype-{portal_type} to match
  what the rest of Plone expects. This fixes sprite based icons for
  pages/documents.
  [gaudenz]


1.0 - 2011-07-19
----------------

- Removed `searchResults` view and related code. Search is handled inside
  `plone.app.search`.
  [hannosch]

- Renamed `uniqueIdentifier` method to `uuid` for shorter and more consistent
  naming with `plone.uuid`.
  [hannosch]


0.1b2 - 2011-04-15
------------------

- Unit tests for appendViewAction, compare against portal_type rather than Type.
  [lentinj]

- Handle RealContentListingObject objects in isVisibleFromNav,
  appendViewAction. Remove memoise, isn't going to cache anything for a useful
  amount of time.
  [lentinj]


0.1b1 - 2011-04-15
------------------

- Add an isVisibleFromNav method, based on http://siarp.de/node/201, use
  memoise to cache lookup of portal_properties
  [lentinj]

- Add MANIFEST.in.
  [WouterVH]


0.1a1 - 2011-03-02
------------------

- Initial release

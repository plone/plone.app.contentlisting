Changelog
=========

1.2 (unreleased)
------------------

- Introduce ``@@contentlisting`` view, which is also supports Collections from
  plone.app.contenttypes including filtering of results. This gives us a
  unified interface for listing content from Folders or Collections.
  Deprecate ``@@folderListing``, which is kept for BBB compatibility.
  [thet]

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

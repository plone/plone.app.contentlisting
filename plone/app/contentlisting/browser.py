# -*- coding: utf-8 -*-
from plone.app.contentlisting.interfaces import IContentListing
from Products.CMFCore.utils import getToolByName
from zope.publisher.browser import BrowserView


class FolderListing(BrowserView):

    def __call__(self, batch=False, b_size=20, b_start=0, orphan=0, **kw):
        query = {}
        query.update(kw)

        query['path'] = {
            'query': '/'.join(self.context.getPhysicalPath()),
            'depth': 1,
        }

        # if we don't have asked explicitly for other sorting, we'll want
        # it by position in parent
        if 'sort_on' not in query:
            query['sort_on'] = 'getObjPositionInParent'

        # Provide batching hints to the catalog
        if batch:
            query['b_start'] = b_start
            query['b_size'] = b_size + orphan

        catalog = getToolByName(self.context, 'portal_catalog')
        results = catalog(query)
        return IContentListing(results)


class ContentListingCollection(BrowserView):

    def __call__(self, batch=False, b_size=20, b_start=0, **kw):

        if 'orphan' in kw:
            # At the moment, orphan keyword is not supported by
            # plone.app.contenttypes Collection behavior, nor by
            # plone.app.querystring's querybuilder.
            del kw['orphan']

        res = self.context.results(
            batch=batch,
            b_size=b_size,
            b_start=b_start,
            custom_query=kw,
        )
        return res

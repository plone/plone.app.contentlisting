import logging
import types

from Products.CMFCore.utils import getToolByName
from zope.publisher.browser import BrowserView

from interfaces import IContentListing


class FolderListing(BrowserView):

    def __call__(self, batch=False, b_size=100, b_start=0, **kw):
        query = {}
        query.update(kw)
        if not kw:
            query.update(getattr(self.request, 'form', {}))
            query.update(dict(getattr(self.request, 'other', {})))

        query['path'] = {'query': '/'.join(self.context.getPhysicalPath()),
                         'depth': 1}

        # if we don't have asked explicitly for other sorting, we'll want
        # it by position in parent
        if not query.get('sort_on', None):
            query['sort_on'] = 'getObjPositionInParent'

        # Not used:
        #show_inactive = getToolByName(
        #    self.context, 'portal_membership').checkPermission(
        #    'Access inactive portal content', self.context)
        results = IContentListing(
            getToolByName(self.context, 'portal_catalog')(query))

        if batch:
            from Products.CMFPlone import Batch
            batch = Batch(results, b_size, int(b_start), orphan=0)
            return IContentListing(batch)
        return results


class SearchResults(BrowserView):

    def __call__(self, query=None, batch=False, b_size=100, b_start=0, **kw):
        """ Get properly wrapped search results from the catalog.

        Everything in Plone that performs searches should go through this view.

        'query' (optional) should be a dictionary of catalog parameters.

        You can also pass catalog parameters as individual named keywords.
        """
        if query is None:
            query = {}
        query.update(kw)
        if not query:
            return IContentListing([])

        # Check for invalid indexes
        logger = logging.getLogger('plone.app.contentlisting')
        catalog = getToolByName(self.context, 'portal_catalog')
        indexes = catalog.indexes() + ['sort_on', 'sort_order', ]
        invalid_indexes = [index for index in query if index not in indexes]
        for index in invalid_indexes:
            logger.info("'%s' is an invalid catalog index" % index)

        query = self.ensureFriendlyTypes(query)

        results = IContentListing(catalog(query))
        if batch:
            from Products.CMFPlone import Batch
            batch = Batch(results, b_size, int(b_start), orphan=0)
            return IContentListing(batch)
        return results

    def ensureFriendlyTypes(self, query):
        # ported from Plone's queryCatalog. It hurts to bring this one along.
        # The fact that it is needed at all tells us that we currently abuse
        # the concept of types in Plone
        # please remove this one when it is no longer needed.

        ploneUtils = getToolByName(self.context, 'plone_utils')
        portal_type = query.get('portal_type', [])
        if not type(portal_type) is types.ListType:
            portal_type = [portal_type]
        Type = query.get('Type', [])
        if not type(Type) is types.ListType:
            Type = [Type]
        typesList = portal_type + Type
        if not typesList:
            friendlyTypes = ploneUtils.getUserFriendlyTypes(typesList)
            query['portal_type'] = friendlyTypes
        return query

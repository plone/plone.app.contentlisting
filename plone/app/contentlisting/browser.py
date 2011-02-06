from Products.CMFCore.utils import getToolByName
## PloneBatch currently has problems
# from Products.CMFPlone.PloneBatch import Batch
from ZTUtils.Batch import Batch
from zope.publisher.browser import BrowserView

from .interfaces import IContentListing


class FolderListing(BrowserView):

    def __call__(self, batch=False, b_size=20, b_start=0, orphan=0, **kw):
        query = {}
        query.update(kw)

        query['path'] = {'query': '/'.join(self.context.getPhysicalPath()),
                         'depth': 1}

        # if we don't have asked explicitly for other sorting, we'll want
        # it by position in parent
        if 'sort_on' not in query:
            query['sort_on'] = 'getObjPositionInParent'

        # Not used:
        #show_inactive = getToolByName(
        #    self.context, 'portal_membership').checkPermission(
        #    'Access inactive portal content', self.context)

        # Provide batching hints to the catalog
        if batch:
            query['b_start'] = b_start
            query['b_size'] = b_size + orphan

        catalog = getToolByName(self.context, 'portal_catalog')
        results = catalog(query)
        if batch:
            results = Batch(results, b_size, b_start, orphan=orphan)
        return IContentListing(results)


class SearchResults(BrowserView):

    def __call__(self, query=None, batch=False, b_size=20, b_start=0, orphan=0, **kw):
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

        catalog = getToolByName(self.context, 'portal_catalog')
        query = self.ensureFriendlyTypes(query)

        # Provide batching hints to the catalog
        if batch:
            query['b_start'] = b_start
            query['b_size'] = b_size + orphan

        results = catalog(query)
        if batch:
            results = Batch(results, b_size, b_start, orphan=orphan)
        return IContentListing(results)

    def ensureFriendlyTypes(self, query):
        # ported from Plone's queryCatalog. It hurts to bring this one along.
        # The fact that it is needed at all tells us that we currently abuse
        # the concept of types in Plone
        # please remove this one when it is no longer needed.

        ploneUtils = getToolByName(self.context, 'plone_utils')
        portal_type = query.get('portal_type', [])
        if not isinstance(portal_type, list):
            portal_type = [portal_type]
        Type = query.get('Type', [])
        if not isinstance(Type, list):
            Type = [Type]
        typesList = portal_type + Type
        if not typesList:
            friendlyTypes = ploneUtils.getUserFriendlyTypes(typesList)
            query['portal_type'] = friendlyTypes
        return query

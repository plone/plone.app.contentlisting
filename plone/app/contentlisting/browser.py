from Products.Five.browser import BrowserView
from interfaces import IContentListing
from Products.CMFCore.utils import getToolByName
import types


class FolderListing(BrowserView):
    
    def __call__(self, batch=False, b_size=100,b_start=0, **kw):
        query = {}
        query.update(kw)
        if not kw:
            query.update(getattr(self.request, 'form',{}))
            query.update(dict(getattr(self.request, 'other',{})))
        
        query['path'] = {'query': '/'.join(self.context.getPhysicalPath()), 
                'depth':1}
                
        # if we don't have asked explicitly for other sorting, we'll want 
        # it by position in parent
        if not query.get('sort_on', None):
            query['sort_on'] = 'getObjPositionInParent'
        
        show_inactive = getToolByName(self.context, 'portal_membership').checkPermission('Access inactive portal content', self.context)
        results = IContentListing(getToolByName(self.context, 'portal_catalog')(query))

        if batch:
            from Products.CMFPlone import Batch
            b_start = self.request.get('b_start', 0)
            batch = Batch(results, b_size, int(b_start), orphan=0)
            return IContentListing(batch)
        return results


class SearchResults(BrowserView):
    
    def __call__(self, **kw):
        query = {}
        query.update(kw)
        if not kw:
            query.update(getattr(self.request, 'form',{}))
            #query.update(dict(getattr(self.request, 'other',{})))
        if not query:
            return IContentListing([])
        catalog = getToolByName(self.context, 'portal_catalog')
        return IContentListing(catalog(query))

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

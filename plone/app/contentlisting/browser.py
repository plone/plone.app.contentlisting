from Products.Five.browser import BrowserView
from interfaces import IContentListing
from Products.CMFCore.utils import getToolByName




class FolderListing(BrowserView):
    
    def __call__(self, batch=False, b_size=100, **kw):
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
            return batch
        
        return results


class SearchResults(BrowserView):
    
    def __call__(self, **kw):
        query = {}
        query.update(kw)
        catalog = getToolByName(self.context, 'portal_catalog')
        return IContentListing(catalog(query))






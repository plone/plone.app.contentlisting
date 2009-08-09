from Products.Five.browser import BrowserView
from interfaces import IContentListing
from Products.CMFCore.utils import getToolByName


class FolderListing(BrowserView):
    
    def __call__(self, **kw):
        query = {}
        path = {'query': '/'.join(self.context.getPhysicalPath()), 
                'depth':1}
        query['path'] = path
        query.update(kw)
        catalog = getToolByName(self.context, 'portal_catalog')
        return IContentListing(catalog(query))



class SearchResults(BrowserView):
    
    def __call__(self, **kw):
        query = {}
        query.update(kw)
        catalog = getToolByName(self.context, 'portal_catalog')
        return IContentListing(catalog(query))






from Products.Five.browser import BrowserView
from interfaces import IContentListing

#class CatalogContentListingFactory(object):
#    """  """
#    interface.implements(IContentListingFactory)
#    
#    def __init__(self, context):
#        self.context = context
#        self.defaultquery = dict(path=context.getPhysicalPath())
#
#    def __call__(self, *kw):
#        query = self.defaultquery.copy()
#        query.update(*kw)
#        catalog = getToolByName(self.context, 'portal_catalog')
#        return CatalogContentListing(catalog(query))
#

class ContentListerView(BrowserView):
    
    def getContentListing(self):
        return IContentListingFactory(self.context)

class FolderListing(BrowserView):
    
    def __call__(self, **kw):
        query = {}
        path = {'query': '/'.join(self.context.getPhysicalPath()), 
                'depth':1}
        query['path'] = path
        query.update(kw)
        f = IContentListingFactory(self.context)
        return f(query)
from Products.Five.browser import BrowserView
from interfaces import IContentLister

class ContentListerFactory(BrowserView):
    
    def getContentListing(self):
        return IContentLister(self.context)
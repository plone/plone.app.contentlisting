from Products.Five.browser import BrowserView
from interfaces import IContentListingFactory

class ContentListerView(BrowserView):
    
    def getContentListing(self):
        return IContentListingFactory(self.context)
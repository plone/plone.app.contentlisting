from Products.Five.browser import BrowserView
from interfaces import IContentLister

class ContentListerFactory(BrowserView):
    def __call__(self):
        return IContentLister(self.context)()[2].Language()
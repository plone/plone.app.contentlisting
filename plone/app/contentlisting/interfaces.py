from zope import interface
from Products.CMFCore.interfaces import IDublinCore

class IContentLister(interface.Interface):

    def __call__(**kw):
       """ returns IContentListing """


class IContentListing(interface.common.sequence.IReadSequence):
    """Sequence of IContentListingObjects"""


class IContentListingObject(IDublinCore):
    """Unified representation of content objects in listings"""
    
    def __getattr__(name):
        """Anything not matching the interface will be passed to the proxied item"""
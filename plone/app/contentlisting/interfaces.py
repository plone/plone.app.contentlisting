from zope import interface
from Products.CMFCore.interfaces import IDublinCore

class IContentListingFactory(interface.Interface):

    def __call__(**kw):
       """ returns IContentListing """


class IContentListing(interface.common.sequence.IReadSequence):
    """Sequence of IContentListingObjects"""


class IContentListingObject(IDublinCore):
    """Unified representation of content objects in listings"""
    
    def getId():
        """ get the object id"""
        
    def getPath():
        """ """
        
    def getURL():
        """ """

    def UID():
        """ """

    def getIcon():
        """ """

    def getSize():
        """ """

    def review_state():
        """ """
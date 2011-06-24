from Products.CMFCore.interfaces import IDublinCore
from zope.interface.common.sequence import IReadSequence


class IContentListing(IReadSequence):
    """Sequence of IContentListingObjects"""


class IContentListingObject(IDublinCore):
    """Unified representation of content objects in listings"""

    def getId():
        """get the object id in its container"""

    def getObject():
        """get the real object (may be expensive)"""

    def getPath():
        """Path to the object, relative to the portal root"""

    def getURL():
        """Full url to the object, including the portal root"""

    def uuid():
        """Unique content identifier"""

    def getIcon():
        """icon for the object"""

    def getSize():
        """size in bytes"""

    def review_state():
        """Workflow review state"""

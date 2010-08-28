from zope import interface
from Products.CMFCore.interfaces import IDublinCore


class IContentListing(interface.common.sequence.IReadSequence):
    """Sequence of IContentListingObjects"""


class IContentListingObject(IDublinCore):
    """Unified representation of content objects in listings"""

    # Note that we inherit IDublinCore - so all of Dubin core
    # interface is included in addition to the methods listed below.

    def getId():
        """get the object id in its container"""

    def getPath():
        """Path to the object, relative to the portal root"""

    def getURL():
        """Full url to the object, including the portal root"""

    def UID():
        """Unique content identifier"""

    def getIcon():
        """icon for the object"""

    def getSize():
        """size in bytes"""

    def review_state():
        """Workflow review state"""

# -*- coding: utf-8 -*-
from Products.CMFCore.interfaces import IDublinCore
from zope.interface.common.sequence import IReadSequence


class IContentListing(IReadSequence):
    """Sequence of IContentListingObjects."""


class IContentListingObject(IDublinCore):
    """Unified representation of content objects in listings."""

    def getDataOrigin():
        """The origin of the data for the object."""

    def getObject():
        """get the real object (may be expensive)."""

    def getId():
        """get the object id in its container."""

    def getPath():
        """Path to the object, relative to the portal root."""

    def getURL(relative=False):
        """Full url to the object, including the portal root."""

    def uuid():
        """Unique content identifier."""

    def getSize():
        """size in bytes."""

    def review_state():
        """Workflow review state."""

    def Title():
        """Title."""

    def Description():
        """Description."""

    def CroppedDescription():
        """A cropped description."""

    def Type():
        """Type title."""

    def PortalType():
        """Content type id of the object."""

    def listCreators():
        """List creators of the object."""

    def getUserData(username):
        """Get some data of a given user."""

    def Creator():
        """Creator of the object."""

    def Author():
        """Author of the object."""

    def Subject():
        """Subject(s) of the object."""

    def Date():
        """Date of the object."""

    def CreationDate():
        """Creation date of the object."""

    def EffectiveDate():
        """Date, when content will be shown in listings."""

    def ExpirationDate():
        """Date, when content will be removed from listings."""

    def ModificationDate():
        """Date, when object was last modified."""

    def Language():
        """Language of the object."""

    def ContentTypeClass():
        """The contenttype suitable as a css class name, matching Plone
        conventions.
        """

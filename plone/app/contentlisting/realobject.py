import logging

from Acquisition import aq_base
from Acquisition import aq_get
from plone.app.layout.icons.interfaces import IContentIcon
from plone.uuid.interfaces import IUUID
from Products.CMFCore.utils import getToolByName
from zope.component import queryMultiAdapter
from zope import interface

from .contentlisting import BaseContentListingObject
from .interfaces import IContentListingObject

logger = logging.getLogger('plone.app.contentlisting')


class RealContentListingObject(BaseContentListingObject):
    """A content object representation wrapping a real content object"""

    interface.implements(IContentListingObject)

    def __init__(self, obj):
        self.realobject = obj
        self.request = aq_get(self.realobject, 'REQUEST')

    def __repr__(self):
        return "<plone.app.contentlisting.realobject." + \
               "RealContentListingObject instance at %s>" % (
            self.getPath(), )

    __str__ = __repr__

    def __getattr__(self, name):
        """We'll override getattr so that we can defer name lookups to
        the real underlying objects without knowing the names of all
        attributes.
        """
        if name.startswith('_'):
            raise AttributeError(name)
        elif hasattr(aq_base(self.realobject), name):
            logger.debug("deferred attribute lookup to the real object %s" %
                self.realobject)
            return getattr(aq_base(self.realobject), name)
        else:
            raise AttributeError(name)

    def getDataOrigin(self):
        """The origin of the data for the object.

        Sometimes we just need to know if we are looking at a brain or
        the real object.
        """
        return self.realobject

    # a base set of elements that are needed but not defined in dublin core
    def getPath(self):
        return '/'.join(self.realobject.getPhysicalPath())

    def getURL(self):
        return self.realobject.absolute_url()

    def uniqueIdentifier(self):
        # content objects might have UID and might not. Same thing for
        # their brain.
        uuid = IUUID(self.realobject, None)
        if uuid is not None:
            return uuid
        return self.getPath()

    def getIcon(self):
        return queryMultiAdapter(
            (self.realobject, self.request, self.realobject),
            interface=IContentIcon)()

    def review_state(self):
        wftool = getToolByName(self.realobject, "portal_workflow")
        return wftool.getInfoFor(self.realobject, 'review_state')

    def Type(self):
        """Dublin Core element - Object type"""
        typestool = getToolByName(self.realobject, 'portal_types')
        ti = typestool.getTypeInfo(self.realobject)
        if ti is not None:
            return ti.Title()
        return self.realobject.meta_type

# Needed: A method Type() that returns the same as is cataloged as Type.
# Currently Type() returns different values depending on the data source being
# a brain or a real object. Probably needed. Support for all the attributes
# from the indexablemetadata wrappers.

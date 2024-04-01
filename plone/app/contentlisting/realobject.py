from Acquisition import aq_get
from plone.app.contentlisting.contentlisting import BaseContentListingObject
from plone.app.contentlisting.interfaces import IContentListingObject
from plone.base.interfaces import IImageScalesAdapter
from plone.base.utils import base_hasattr
from plone.base.utils import human_readable_size
from plone.rfc822.interfaces import IPrimaryFieldInfo
from plone.uuid.interfaces import IUUID
from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter
from zope.interface import implementer


MARKER = object()


@implementer(IContentListingObject)
class RealContentListingObject(BaseContentListingObject):
    """A content object representation wrapping a real content object."""

    def __init__(self, obj):
        self._realobject = obj
        self.request = aq_get(obj, "REQUEST")

    def __repr__(self):
        return (
            "<plone.app.contentlisting.realobject."
            f"RealContentListingObject instance at {self.getPath()}>"
        )

    __str__ = __repr__

    def __getattr__(self, name):
        """We'll override getattr so that we can defer name lookups to
        the real underlying objects without knowing the names of all
        attributes.
        """
        if name.startswith("_"):
            raise AttributeError(name)
        obj = self.getObject()
        # we check that obj without acquisition has the attribute
        # but we return it with acquisition in case it is a method
        # that itself uses the acquisition
        if base_hasattr(obj, name):
            return getattr(obj, name)
        raise AttributeError(name)

    def getObject(self):
        return self._realobject

    def getDataOrigin(self):
        # The origin of the data for the object.
        # Sometimes we just need to know if we are looking at a brain or
        # the real object.
        return self.getObject()

    # a base set of elements that are needed but not defined in dublin core
    def getPath(self):
        return "/".join(self.getObject().getPhysicalPath())

    def getURL(self):
        return self.getObject().absolute_url()

    def uuid(self):
        # content objects might have UID and might not. Same thing for
        # their brain.
        uuid = IUUID(self.getObject(), None)
        if uuid is not None:
            return uuid
        return self.getPath()

    def getSize(self):
        # return size of the primary field content.
        # this works the same way as the indexer works
        obj = self.getObject()
        try:
            primary_field_info = IPrimaryFieldInfo(obj, None)
        except TypeError:
            # no primary field available, dexterity raises a TypeError
            # with the slightly misleading message 'could not adapt'.
            primary_field_info = None
        if primary_field_info is None or not primary_field_info.value:
            size = 0
        else:
            size = getattr(primary_field_info.value, "size", 0)
        return human_readable_size(size)

    def review_state(self):
        obj = self.getObject()
        wftool = getToolByName(obj, "portal_workflow")
        return wftool.getInfoFor(obj, "review_state", default=None)

    def Type(self):
        # Dublin Core element - Object type.
        obj = self.getObject()
        typestool = getToolByName(obj, "portal_types")
        ti = typestool.getTypeInfo(obj)
        if ti is not None:
            return ti.Title()
        return obj.meta_type

    # Needed: A method Type() that returns the same as is cataloged as Type.
    # Currently Type() returns different values depending on the data source being
    # a brain or a real object. Probably needed. Support for all the attributes
    # from the indexablemetadata wrappers.

    def PortalType(self):
        obj = self.getObject()
        return obj.portal_type

    def image_scales(self):
        obj = self.getObject()
        return getMultiAdapter((obj, self.request), IImageScalesAdapter)()

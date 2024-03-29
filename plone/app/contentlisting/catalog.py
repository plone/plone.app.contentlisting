from Acquisition import aq_base
from plone.app.contentlisting.contentlisting import BaseContentListingObject
from plone.app.contentlisting.interfaces import IContentListingObject
from plone.registry.interfaces import IRegistry
from plone.uuid.interfaces import IUUID
from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter
from zope.component import queryUtility
from zope.globalrequest import getRequest
from zope.interface import implementer


missing = object()


@implementer(IContentListingObject)
class CatalogContentListingObject(BaseContentListingObject):
    """A Catalog-results based content object representation.

    Whenever sequences of catalog brains are turned into contentlistings,
    This is the type of objects they are adapted to.
    """

    def __init__(self, brain):
        self._brain = brain
        self._cached_realobject = None
        self.request = getRequest()

    def __repr__(self):
        return (
            "<plone.app.contentlisting.catalog."
            "CatalogContentListingObject instance at {}>".format(
                self.getPath(),
            )
        )

    __str__ = __repr__

    def __getattr__(self, name):
        """We'll override getattr so that we can defer name lookups to the real
        underlying objects without knowing the names of all attributes.
        """

        if name.startswith("_"):
            raise AttributeError(name)
        brain_name = getattr(aq_base(self._brain), name, missing)
        if brain_name is not missing:
            return brain_name
        object_name = getattr(aq_base(self.getObject()), name, missing)
        if object_name is not missing:
            return object_name
        raise AttributeError(name)

    def getDataOrigin(self):
        # The origin of the data for the object.
        # Sometimes we just need to know if we are looking at a brain or
        # the real object.
        if self._cached_realobject is not None:
            return self._cached_realobject
        return self._brain

    def getObject(self):
        # Get the real, underlying object.

        # This is performance intensive compared to just getting the
        # catalog brain, so we don't do it until we need to.  We may
        # even have to log this to notify the developer that this might
        # be an inefficient operation.
        if self._cached_realobject is None:
            self._cached_realobject = self._brain.getObject()
        return self._cached_realobject

    # a base set of elements that are needed but not defined in dublin core
    def getId(self):
        return self._brain.getId

    def getPath(self):
        return self._brain.getPath()

    def getURL(self, relative=False):
        return self._brain.getURL(relative=relative)

    def uuid(self):
        # content objects might have UID and might not.
        brain_uid = getattr(aq_base(self._brain), "UID", None)
        if brain_uid is not None:
            return brain_uid
        uuid = IUUID(self.getObject(), None)
        if uuid is not None:
            return uuid
        return self.getPath()

    def getSize(self):
        return self._brain.getObjSize

    def review_state(self):
        return self._brain.review_state

    # All the dublin core elements. Most of them should be in the
    # brain for easy access
    def Title(self):
        return self._brain.Title

    def Description(self):
        return self._brain.Description

    def CroppedDescription(self):
        registry = queryUtility(IRegistry)
        length = registry.get("plone.search_results_description_length")
        plone_view = getMultiAdapter((self, self.request), name="plone")
        return plone_view.cropText(self.Description(), length)

    def Type(self):
        return self._brain.Type

    def PortalType(self):
        return self._brain.portal_type

    def listCreators(self):
        return self._brain.listCreators

    def getUserData(self, username):
        _usercache = self.request.get("usercache", None)
        if _usercache is None:
            self.request.set("usercache", {})
            _usercache = {}
        userdata = _usercache.get(username, None)
        if userdata is None:
            membershiptool = getToolByName(self._brain, "portal_membership")
            userdata = membershiptool.getMemberInfo(self._brain.Creator)
            if not userdata:
                userdata = {
                    "username": username,
                    "description": "",
                    "language": "",
                    "home_page": "/HOMEPAGEURL",
                    "location": "",
                    "fullname": username,
                }
            self.request.usercache[username] = userdata
        return userdata

    def Creator(self):
        return self._brain.Creator

    def Author(self):
        return self.getUserData(self.Creator())

    def Subject(self):
        return self._brain.Subject

    def Publisher(self):
        raise NotImplementedError

    def listContributors(self):
        raise NotImplementedError

    def Contributors(self):
        return self.listContributors()

    def Date(self, zone=None):
        return self._brain.Date

    def CreationDate(self, zone=None):
        return self._brain.CreationDate

    def EffectiveDate(self, zone=None):
        return self._brain.EffectiveDate

    def ExpirationDate(self, zone=None):
        return self._brain.ExpirationDate

    def ModificationDate(self, zone=None):
        return self._brain.ModificationDate

    def Format(self):
        raise NotImplementedError

    def Identifier(self):
        return self.getURL()

    def Language(self):
        # The language of the content.
        brain_language = getattr(aq_base(self._brain), "Language", None)
        if brain_language is not None:
            return self._brain.Language
        return self.getObject().Language()

    def Rights(self):
        raise NotImplementedError

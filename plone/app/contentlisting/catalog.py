# -*- coding: utf-8 -*-
from AccessControl import ClassSecurityInfo
from Acquisition import aq_base
from Acquisition import aq_get
from plone.app.contentlisting.contentlisting import BaseContentListingObject
from plone.app.contentlisting.interfaces import IContentListingObject
from plone.registry.interfaces import IRegistry
from plone.uuid.interfaces import IUUID
from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter
from zope.component import queryUtility
from zope.interface import implementer

import Globals


missing = object()


@implementer(IContentListingObject)
class CatalogContentListingObject(BaseContentListingObject):
    """A Catalog-results based content object representation.

    Whenever sequences of catalog brains are turned into contentlistings,
    This is the type of objects they are adapted to.
    """

    security = ClassSecurityInfo()

    def __init__(self, brain):
        self._brain = brain
        self._cached_realobject = None
        self.request = aq_get(brain, 'REQUEST')

    def __repr__(self):
        return '<plone.app.contentlisting.catalog.'\
            'CatalogContentListingObject instance at {0}>'.format(
                self.getPath(),
            )

    __str__ = __repr__

    def __getattr__(self, name):
        """We'll override getattr so that we can defer name lookups to the real
        underlying objects without knowing the names of all attributes.
        """

        if name.startswith('_'):
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
        else:
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
    security.public(getObject)

    # a base set of elements that are needed but not defined in dublin core
    def getId(self):
        return self._brain.getId
    security.public(getId)

    def getPath(self):
        return self._brain.getPath()
    security.public(getPath)

    def getURL(self, relative=False):
        return self._brain.getURL(relative=relative)
    security.public(getURL)

    def uuid(self):
        # content objects might have UID and might not.
        brain_uid = getattr(aq_base(self._brain), 'UID', None)
        if brain_uid is not None:
            return self._brain.UID
        uuid = IUUID(self.getObject(), None)
        if uuid is not None:
            return uuid
        return self.getPath()
    security.public(uuid)

    def getSize(self):
        return self._brain.getObjSize
    security.public(getSize)

    def review_state(self):
        return self._brain.review_state
    security.public(review_state)

    # All the dublin core elements. Most of them should be in the
    # brain for easy access
    def Title(self):
        return self._brain.Title
    security.public(Title)

    def Description(self):
        return self._brain.Description
    security.public(Description)

    def CroppedDescription(self):
        registry = queryUtility(IRegistry)
        length = registry.get('plone.search_results_description_length')
        plone_view = getMultiAdapter((self, self.request), name='plone')
        return plone_view.cropText(self.Description(), length)
    security.public(CroppedDescription)

    def Type(self):
        return self._brain.Type
    security.public(Type)

    def PortalType(self):
        return self._brain.portal_type
    security.public(PortalType)

    def listCreators(self):
        return self._brain.listCreators
    security.public(listCreators)

    def getUserData(self, username):
        _usercache = self.request.get('usercache', None)
        if _usercache is None:
            self.request.set('usercache', {})
            _usercache = {}
        userdata = _usercache.get(username, None)
        if userdata is None:
            membershiptool = getToolByName(self._brain, 'portal_membership')
            userdata = membershiptool.getMemberInfo(self._brain.Creator)
            if not userdata:
                userdata = {
                    'username': username,
                    'description': '',
                    'language': '',
                    # TODO
                    # string:${navigation_root_url}/author/${item_creator}
                    'home_page': '/HOMEPAGEURL',
                    'location': '',
                    'fullname': username,
                }
            self.request.usercache[username] = userdata
        return userdata
    security.public(getUserData)

    def Creator(self):
        username = self._brain.Creator
        return username
    security.public(Creator)

    def Author(self):
        return self.getUserData(self.Creator())
    security.public(Author)

    def Subject(self):
        return self._brain.Subject
    security.public(Subject)

    def Publisher(self):
        raise NotImplementedError
    security.public(Publisher)

    def listContributors(self):
        raise NotImplementedError
    security.public(listContributors)

    def Contributors(self):
        return self.listContributors()
    security.public(Contributors)

    def Date(self, zone=None):
        return self._brain.Date
    security.public(Date)

    def CreationDate(self, zone=None):
        return self._brain.CreationDate
    security.public(CreationDate)

    def EffectiveDate(self, zone=None):
        return self._brain.EffectiveDate
    security.public(EffectiveDate)

    def ExpirationDate(self, zone=None):
        return self._brain.ExpirationDate
    security.public(ExpirationDate)

    def ModificationDate(self, zone=None):
        return self._brain.ModificationDate
    security.public(ModificationDate)

    def Format(self):
        raise NotImplementedError
    security.public(Format)

    def Identifier(self):
        return self.getURL()
    security.public(Identifier)

    def Language(self):
        # The language of the content.
        brain_language = getattr(aq_base(self._brain), 'Language', None)
        if brain_language is not None:
            return self._brain.Language
        else:
            return self.getObject().Language()
    security.public(Language)

    def Rights(self):
        raise NotImplementedError
    security.public(Rights)


Globals.InitializeClass(CatalogContentListingObject)

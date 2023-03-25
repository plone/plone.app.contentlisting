from Acquisition import aq_base
from plone.app.contentlisting.interfaces import IContentListing
from plone.app.contentlisting.interfaces import IContentListingObject
from plone.base.interfaces import INavigationSchema
from plone.base.navigationroot import get_navigation_root_object
from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from Products.MimetypesRegistry.MimeTypeItem import guess_icon_path
from zope.component import getUtility
from zope.component import queryUtility
from zope.interface import implementer

import os


@implementer(IContentListing)
class ContentListing:
    """An IContentListing implementation based on sequences of objects."""

    def __init__(self, sequence):
        self._basesequence = sequence

    def __getitem__(self, index):
        """`x.__getitem__(index)` <==> `x[index]`"""
        if isinstance(index, slice):
            return IContentListing(
                self._basesequence[index.start : index.stop : index.step]
            )
        return IContentListingObject(self._basesequence[index])

    def __len__(self):
        """Length of the resultset is equal to the length of the underlying
        sequence.
        """
        return len(self._basesequence)

    @property
    def actual_result_count(self):
        bs = self._basesequence
        return getattr(bs, "actual_result_count", len(bs))

    def __iter__(self):
        """Let the sequence be iterable and whenever we look at an object, it
        should be a ContentListingObject.
        """
        for obj in self._basesequence:
            yield IContentListingObject(obj)

    def __contains__(self, item):
        """`x.__contains__(item)` <==> `item in x`"""
        # It would be good if we could check this without waking all objects
        for i in self:
            if i == item:
                return True
        return False

    def __lt__(self, other):
        """`x.__lt__(other)` <==> `x < other`"""
        raise NotImplementedError

    def __le__(self, other):
        """`x.__le__(other)` <==> `x <= other`"""
        raise NotImplementedError

    def __eq__(self, other):
        """`x.__eq__(other)` <==> `x == other`"""
        raise NotImplementedError

    def __hash__(self):
        """`x.__hash__()`"""
        raise NotImplementedError

    def __ne__(self, other):
        """`x.__ne__(other)` <==> `x != other`"""
        raise NotImplementedError

    def __gt__(self, other):
        """`x.__gt__(other)` <==> `x > other`"""
        raise NotImplementedError

    def __ge__(self, other):
        """`x.__ge__(other)` <==> `x >= other`"""
        raise NotImplementedError

    def __add__(self, other):
        """`x.__add__(other)` <==> `x + other`"""
        raise NotImplementedError

    def __mul__(self, n):
        """`x.__mul__(n)` <==> `x * n`"""
        raise NotImplementedError

    def __rmul__(self, n):
        """`x.__rmul__(n)` <==> `n * x`"""
        raise NotImplementedError

    def __getslice__(self, i, j):
        """`x.__getslice__(i, j)` <==> `x[i:j]`
        Use of negative indices is not supported.
        No longer used in Python 3, but still part of
        zope.interface.interfaces.IReadSequence
        """
        return IContentListing(self._basesequence[i:j])


class BaseContentListingObject:
    """A baseclass for the different types of contentlistingobjects.

    To avoid duplication of the stuff that is not implementation-specific.
    """

    def __eq__(self, other):
        """For comparing two contentlistingobject"""
        other = IContentListingObject(other)
        return self.uuid() == other.uuid()

    def __hash__(self):
        return hash(self.uuid())

    def ContentTypeClass(self):
        # A normalised type name that identifies the object in listings.
        # Used for CSS styling.
        return "contenttype-" + queryUtility(IIDNormalizer).normalize(
            self.PortalType(),
        )

    def ReviewStateClass(self):
        # A normalised review state string for CSS styling use in listings.
        return "state-" + queryUtility(IIDNormalizer).normalize(
            self.review_state(),
        )

    def appendViewAction(self):
        # Decide whether to produce a string /view to append to links in
        # results listings.
        registry = getUtility(IRegistry)
        types = registry.get("plone.types_use_view_action_in_listings", [])
        if self.portal_type in types:
            return "/view"
        return ""

    def isVisibleInNav(self):
        # True, if this item should be visible in navigation trees.
        exclude_from_nav_attr = getattr(self, "exclude_from_nav", None)
        if exclude_from_nav_attr is not None and (
            self.exclude_from_nav()
            if callable(self.exclude_from_nav)
            else self.exclude_from_nav
        ):
            return False

        registry = getUtility(IRegistry)
        navigation_settings = registry.forInterface(
            INavigationSchema,
            prefix="plone",
        )
        if self.portal_type not in navigation_settings.displayed_types:
            return False

        return True

    def MimeTypeIcon(self):
        mimeicon = None
        portal_url_object = getToolByName(self._brain, "portal_url")
        portal = portal_url_object.getPortalObject()
        navroot = get_navigation_root_object(self._brain, portal)
        contenttype = aq_base(
            getattr(self._brain, "mime_type", None),
        )
        if contenttype:
            mtt = getToolByName(
                self._brain,
                "mimetypes_registry",
            )
            ctype = mtt.lookup(contenttype)
            if ctype:
                mimeicon = os.path.join(
                    navroot.absolute_url(),
                    guess_icon_path(ctype[0]),
                )

        return mimeicon

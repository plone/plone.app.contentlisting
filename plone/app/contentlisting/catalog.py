# Implementation of IContentListing and friends based on queries to the 
# portal_catalog. At the time of writing, this is the only and default IContentListing implementation. 
#
from zope.component import queryMultiAdapter
from interfaces import IContentListing, IContentListingObject
from Acquisition import aq_base
from Products.CMFCore.utils import getToolByName
from zope import interface
from zLOG import LOG, INFO
from plone.app.layout.icons.interfaces import IContentIcon

class CatalogContentListing:
    """ A catalog-results based IContentListing."""
    interface.implements(IContentListing)

    
    def __init__(self, sequence):
        self._basesequence = sequence
        
    
    def __getitem__(self, index):
        """`x.__getitem__(index)` <==> `x[index]`
        """
        return IContentListingObject(self._basesequence[index])


    def __len__(self):
        """ length of the resultset is equal to the lenght of the underlying
            catalog resultset
        """
        return self._basesequence.__len__()


    def __iter__(self):
        for obj in self._basesequence:
            yield IContentListingObject(obj)


    def __contains__(self, item):
        """`x.__contains__(item)` <==> `item in x`"""
        # huhm. How do we check this? Waking all contained objects is not fun
        # A content hash? Perhaps UID?
        raise NotImplemented
    
    
    def __lt__(self, other):
        """`x.__lt__(other)` <==> `x < other`"""
        raise NotImplemented


    def __le__(self, other):
        """`x.__le__(other)` <==> `x <= other`"""
        raise NotImplemented


    def __eq__(self, other):
        """`x.__eq__(other)` <==> `x == other`"""
        raise NotImplemented


    def __ne__(self, other):
        """`x.__ne__(other)` <==> `x != other`"""
        raise NotImplemented


    def __gt__(self, other):
        """`x.__gt__(other)` <==> `x > other`"""
        raise NotImplemented


    def __ge__(self, other):
        """`x.__ge__(other)` <==> `x >= other`"""
        raise NotImplemented


    def __add__(self, other):
        """`x.__add__(other)` <==> `x + other`"""
        raise NotImplemented


    def __mul__(self, n):
        """`x.__mul__(n)` <==> `x * n`"""
        raise NotImplemented


    def __rmul__(self, n):
        """`x.__rmul__(n)` <==> `n * x`"""
        raise NotImplemented


    def __getslice__(self, i, j):
        """`x.__getslice__(i, j)` <==> `x[i:j]`
        Use of negative indices is not supported.
        Deprecated since Python 2.0 but still a part of `UserList`.
        """
        return IContentListing(self._basesequence[i:j])

#    def __repr__(self):
#        """ print a handy, usable name for testing purposes"""
#        return "<ContentListing containing %s ContentListingObjects>" %(self.__len__(),)



class CatalogContentListingObject:
    """ A Catalog-results based content object representation"""
    
    interface.implements(IContentListingObject)
    

    def __init__(self, brain):
        self._brain = brain
        self._cached_realobject = None


    def __repr__(self):
        return "<plone.app.contentlisting.catalog.CatalogContentListingObject instance>"

    __str__ = __repr__


    def __getattr__(self, name):
        """ We'll override getattr so that we can defer name lookups to the real underlying objects without knowing the names of all attributes """
        # 
        if hasattr(aq_base(self._brain), name):
            LOG('plone.app.contentlisting', INFO, "deferred attribute lookup to brain %s" %(str(self._brain),) )
            return getattr(self._brain, name)
        elif hasattr(aq_base(self.realobject), name):
            LOG('plone.app.contentlisting', INFO, "deferred attribute lookup to the real object %s" %(str(self._brain),) )
            return getattr(aq_base(self.realobject), name)
        else:
            return "AttributeError"
            raise AttributeError, name


    def getDataOrigin(self):
        """ The origin of the data for the object """
        if self._cached_realobject is not None:
            return self._cached_realobject
        else:
            return self._brain


    @property
    def realobject(self):
        """get the real, underlying object
            this is perfomance intensive compared to just getting the catalog brain, so we don't do it until we need to.
            We may even have to log this to notify the developer that this might be an inefficient operation.
        """
        if self._cached_realobject is None:
            self._cached_realobject = self._brain.getObject()
            LOG('plone.app.contentlisting', INFO, "fetched real object for %s" %(str(self._brain),) )
        return self._cached_realobject


    # a base set of elements that are needed but not defined in dublin core 

    def getId(self):
        return self._brain.getId

        
    def getPath(self):
        return self._brain.getPath()

        
    def getURL(self):
        return self._brain.getURL()


    def UID(self):
        # content objects might have UID and might not. Same thing for their brain.
        if hasattr(aq_base(self._brain), 'UID'):
            return self._brain.UID
        else:
            return aq_base(self.realobject).UID()


    def getIcon(self):
        return queryMultiAdapter((self._brain, self._brain.REQUEST, self._brain),interface=IContentIcon)()


    def getSize(self):
        return self._brain.getSize


    def review_state(self):
        return self._brain.review_state


    # All the dublin core elements. Most of them should be in the brain for easy access

    def Title(self):
        """"""
        return self._brain.Title


    def Description(self):
        """"""
        return self._brain.Description


    def Type(self):
        return self._brain.Type


    def listCreators(self):
        """ """
        raise NotImplemented


    def Creator(self):
        """ """
        return self._brain.Creator


    def Subject(self):
        return self._brain.Subject


    def Publisher(self):
        raise NotImplemented


    def listContributors(self):
        raise NotImplemented


    def Contributors(self):
        raise NotImplemented


    def Date(self, zone=None):
        raise NotImplemented


    def CreationDate(self, zone=None):
        raise NotImplemented


    def EffectiveDate(self, zone=None):
         return self._brain.EffectiveDate


    def ExpirationDate(self, zone=None):
        return self._brain.ExpirationDate


    def ModificationDate(self, zone=None):
        return self._brain.ModificationDate


    def Format(self):
        raise NotImplemented


    def Identifier(self):
        return self.getURL()


    def Language(self):
        if hasattr(aq_base(self._brain), 'Language'):
            return self._brain.Language
        else:
            return self.realobject.Language()


    def Rights(self):
        raise NotImplemented





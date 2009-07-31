# Implementation of IContentListing and friends based on queries to the 
# portal_catalog.
#

from interfaces import IContentLister, IContentListing, IContentListingObject
from Products.CMFCore.utils import getToolByName
from zope import interface
from zLOG import LOG, INFO

class CatalogContentLister(object):
    """  """
    interface.implements(IContentLister)
    
    def __init__(self, context):
        self.context = context
        self.defaultquery = dict(path=context.getPhysicalPath())
        
        

    def __call__(self, **kw):
        query = self.defaultquery.copy()
        query.update(kw)
        catalog = getToolByName(self.context, 'portal_catalog')
        return CatalogContentListing(catalog(**query))
        

class CatalogContentListing:
    """ """
    interface.implements(IContentListing)
    
    def __init__(self, catalogresultset):
        self._catalogresultset = catalogresultset
    
    def __getitem__(self, index):
        """`x.__getitem__(index)` <==> `x[index]`
        """
        return CatalogContentListingObject(self._catalogresultset[index])

    def __len__(self):
        """ length of the resultset is equal to the lenght of the underlying
            catalog resultset
        """
        return self._catalogresultset.__len__()


    def __iter__(self):
        for item in self._catalogresultset:
            yield CatalogContentListingObject(item)


    def __contains__(item):
        """`x.__contains__(item)` <==> `item in x`"""
        raise NotImplemented
        
    def __lt__(other):
        """`x.__lt__(other)` <==> `x < other`"""
        raise NotImplemented

    def __le__(other):
        """`x.__le__(other)` <==> `x <= other`"""
        raise NotImplemented

    def __eq__(other):
        """`x.__eq__(other)` <==> `x == other`"""
        raise NotImplemented

    def __ne__(other):
        """`x.__ne__(other)` <==> `x != other`"""
        raise NotImplemented

    def __gt__(other):
        """`x.__gt__(other)` <==> `x > other`"""
        raise NotImplemented

    def __ge__(other):
        """`x.__ge__(other)` <==> `x >= other`"""
        raise NotImplemented

    def __add__(other):
        """`x.__add__(other)` <==> `x + other`"""
        raise NotImplemented

    def __mul__(n):
        """`x.__mul__(n)` <==> `x * n`"""
        raise NotImplemented

    def __rmul__(n):
        """`x.__rmul__(n)` <==> `n * x`"""
        raise NotImplemented

    def __getslice__(i, j):
        """`x.__getslice__(i, j)` <==> `x[i:j]`
        Use of negative indices is not supported.
        Deprecated since Python 2.0 but still a part of `UserList`.
        """
        raise NotImplemented

    def __repr__(self):
        """ print a handy, usable name for testing purposes"""
        return "<ContentListing containing %s ContentListingObjects>" %(self.__len__(),)



class CatalogContentListingObject:
    """ """
    interface.implements(IContentListingObject)

    def __init__(self, brain):
        self._brain = brain
        self._cached_realobject = None
        
    def getDataOrigin(self):
        """ a string defing the origin of the real object """
        if self._cached_realobject is not None:
            return "Real object"
        else:
            return "Catalog brain"

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
        if hasattr(self._brain.aq_base, 'UID'):
            return self._brain.UID
        else:
            return self.realobject.aq_base.UID()

    def getIcon(self):
        return self._brain.getIcon

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
        raise NotImplemented

    def Language(self):
        if hasattr(self._brain.aq_base, 'Language'):
            return self._brain.Language
        else:
            return self.realobject.Language()

    def Rights(self):
        raise NotImplemented





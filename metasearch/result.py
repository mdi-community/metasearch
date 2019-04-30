"""
Abstract interfaces for capturing results from a query to a repository
"""
from abc import ABCMeta, abstractmethod, abstractproperty

class QueryResult(object):
    """
    a container for a result from a query to a repository.  This class gives
    access to summary information about the results and well access to the 
    result in its native form.
    """
    __metaclass__ = ABCMeta

    def __init__(self, nativedata):
        """
        initialize this result with the native data object returned by the 
        repository search service.
        """
        self.native = nativedata

    def getNative(self):
        """
        return the query results in its native form
        """
        return self.native

    @abstractmethod
    def hasNextPage(self):
        """
        return True if it is (or may be) an additional page of results available
        """
        raise False

    @abstractmethod
    def nextPage(self):
        """
        return a QueryResult object that contains the next page of results
        that match the original query.  

        :return: QueryResult or None if no further data is available
        """
        raise NotImplemented()

    

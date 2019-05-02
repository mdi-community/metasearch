"""
Abstract interfaces for capturing results from a query to a repository
"""
import copy
from ...result import QueryResult
class CDCSQueryResult(QueryResult):
    """
    a container for a result from a query to a repository.  This class gives
    access to summary information about the results and well access to the
    result in its native form.
    """

    def __init__(self, nativedata, page_size=20,page=1,query=None):
        """
        initialize this result with the native data object returned by the
        repository search service.
        """  
        super(CDCSQueryResult, self).__init__(nativedata, page_size, page=page, query=query)
        self.native = copy.deepcopy(nativedata)
        self.need_next = False
        self.current_page = 1

        
    def getNative(self):
        """
        return the query results in its native form
        """

        return self.native['results']


    def nextPage(self):
        """
        return a QueryResult object that contains the next page of results
        that match the original query.

        :return: QueryResult or None if no further data is available
        """
        if self.need_next:
            url = self.nativedata['next']
            return self.query.submit(url)
        return None

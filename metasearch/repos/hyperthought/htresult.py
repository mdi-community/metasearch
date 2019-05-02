import copy
import json
import requests

from ...result import QueryResult

class HTQueryResult(QueryResult):

    def __init__(self, nativedata, page_size=20, page=1, query=None):
        """
        initialize this result with the native data object returned by the
        repository search service.
        """
        if query is not None and hasattr(query, 'page_size'):
            page_size = query.page_size
        super(HTQueryResult, self).__init__(nativedata, page_size, page, query)

    def getNative(self):
        """
        return the query results in its native form
        """
        return self.native

    def nextPage(self):
        """
        return a QueryResult object that contains the next page of results
        that match the original query.

        :return: QueryResult or None if no further data is available
        """
        data = self.query.page(self.current_page + 1)._raw_submit()
        self.native = copy.deepcopy(data)
        return self.getNative()

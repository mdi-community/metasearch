import copy
import json
import requests

from ...result import QueryResult

class HTQueryResult(QueryResult):

    def __init__(self, nativedata, page_size=20, page=1, query=None):
        """
        initialize this result with the native data object returned by the
        repository search service.

        :param nativedata:  the raw data returned by a query.
        :param page_size:  the number of records per page.
        :param page:  the page in question.
        :param query:  the query object used to generate this query result.
        """
        if query is not None and hasattr(query, 'page_size'):
            page_size = query.page_size
            if page_size < 1:
                page_size = 1
        if query is not None and hasattr(query, 'start'):
            page = int(query.start / page_size) + 1
            if page < 1:
                page = 1
        super(HTQueryResult, self).__init__(nativedata, page_size, page, query)

    def nextPage(self):
        """
        return a QueryResult object that contains the next page of results
        that match the original query.

        :return: QueryResult or None if no further data is available
        """
        self.current_page += 1
        data = self.query.page(self.current_page)._raw_submit()
        self.native = copy.deepcopy(data)
        return self.getNative()

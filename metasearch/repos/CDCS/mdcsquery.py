from query import Query
import requests
import json
class MDCSQuery(Query):
        """
        an encapsulation of a query to a particular repository expressed through
        a general interface.
        A query has two types of constraints:
          *  text terms or phrases that will be compared against any number of
             metadata fields in the repositories database.
          *  constraints on specific metadata fields having recognized names:
             the constraint would be applied against a specific field at the
             repository.
        """

        def __init__(self, baseurl, authentication):
            """
            initialize the query around a base url
            :param str baseurl:   the base URL to the repository's REST search
                                  endpoint.
            :param dict authentication:  an object to use for authentication
                                  (to be defined
            """
            localurl = "/explore/common/rest/local-query"
            self.base = baseurl+localurl
            "For mdcs need username/pwd with admin privileges"
            self.auth = authentication
            super(MDCSQuery).__init__(baseurl,authentication)
            self.text = []
            self.field = []

        def add_freetext_constraint(self, term):
            """
            add a constraint to this query.  The result will included records that
            match the given terms somewhere in the document.
            The implementing repository decides which fields it looks for these
            terms in.
            :param term:   a word, phrase, or a list of phrases to search for
                           matches against
            :type  term:   str or list of str
            """
            if isinstance(term,str):
                {
                    self.field.append("keyword",term)
                }
            return self
        def add_field_constraint(self, fieldname, testvalue):
            """
            add a search constraint to this query against a specific term or concept
            in the repository.

            :param str fieldname:   a name for a field or concept recognized by
                                    the repository.  If the name if not recognized
                                    or supported, the repository may ignore it or
                                    tread it value as free-text search term.
            :param any testvalue:   the value to test the field against
            """
            self.field.append((fieldname,testvalue),)
            return self 

        def submit(self):
            """
            submit the query in its current state to the repository as a full query
            and return the results
            :return:  QueryResult, a container for the results of the query as
                      answered by the repository.
            """

            template_id = "5cc9b1f04a9bdcfb9d7d637b"
            query_url = "/explore/common/rest/local-query"
            url = "http://mdcs.nist.gov:8000"
            turl = url + query_url
            fields = self.field
            dict_name = "interatomic-potential"
            query = list()
            query.append("{\"$or\":[")
            for i in range(0, len(fields)):
                {
                    query.append(
                        "{\"" + str(dict_name) + "." + str(fields[i][0]) + "\":\"" + str(fields[i][1]) + "\"},{\"" + str(
                            dict_name) + "." + str(fields[i][0]) + ".#text\"" + ":\"" + str(fields[i][1]) + "\"},")
                }
            final_query = ("".join(query))
            final_query = final_query[0:-1]+"]}"

            data1 = {"query": final_query, "template": {"$in": [template_id]}, "all": "true"}
            response = requests.get(turl, data=data1, verify=False, auth=("username", "pwd"))
            response_code = response.status_code
            response_content = json.loads(response.text)

            if response_code == requests.codes.ok:
                for rec in response_content:
                    print(rec)
            else:
                response.raise_for_status()
                raise Exception("- error: a problem occurred when uploading the schema (Error ", response_code, ")")
            print('status: done.')



        def supported_fields(self):
            """
            return a list of the field names that this implementation will
            recognize and support as searchable.
            """
            self.supported = ["key", "id", "record-version", "description", "keyword", "implementation", "element",
                      "fictional-element", "other-element"]
            return list(self.supported)
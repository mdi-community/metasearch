"""
Classes and interfaces for creating queries that will go across multiple 
repositories.
"""

class Federation(object):
    """
    This class represents a collection of repositories that can accept 
    queries.  Its interface can be used to created query objects for 
    building a query which can then be sent to all or a subset of the 
    repositories in the federation.
    """

    def __init__(self):
        """
        initialize the federation collection
        """
        self.members = {}
        self.auths = {}

    def registerRepository(self, name, cls, baseurl=None):
        """
        add a repository to this federation with a given name

        :param str name:   a label for refering to the repository
        :param cls class:  the Query Class implementation for supporting queries
        :param str baseurl:  the baseurl for the repository's REST query 
                             interface
        """
        self.members[name] = (cls, baseurl)

    def authenticate(self, name, authentication):
        """
        cache a authentication object for the named repository

        :param str name:   the label identifying the repository that the 
                           authentication is for
        :param dict authentication:   the authentication object to use with 
                           the repository
        """
        if name not in self.members:
            raise RuntimeException(name + ": repository not recognized")
        self.auths[name] = authentication

    def createQuery(self, repos=None):
        """
        create a query instance that can be used to build a query to 
        repositories in the federation.

        :param list repos:  a list of repositories that should be queried.
                            If None, query all of them.
        """
        if repos is None:
            repos = list(self.repos)

        unknown = [n for n in repos if n not in self.repos]
        if len(unknown) > 0:
            raise RuntimeException("Unregistered repos: "+str(unknown))
        
        repoqueries = []
        for name in self.repos:
            auth = None
            if name in self.auths:
                auth = self.auths[name]
            rq = self.repos[name][0](self.repos[name][1], auth)
            repoqueries.append(rq)
            
        return FederatedQuery(self.repoqueries)

    
class FederatedQuery(object):
    """
    an object for creating and submitting a federated query to a set of 
    repositories.
    """

    def __init__(self, repos):
        """
        initialize the query builder

        :param dict repos: map of repos labels to Query instances for its
                           repository
        """
        self.repos = dict(repos)
        self.textcons = []
        self.fieldcons = []

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
        self.textcons.append(term)


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
        self.fieldcons.append( (fieldname, testvalue) )

    def submit(self):
        """
        submit the query in its current state to the repository as a full query
        and return the results

        :return:  dict, a map of repository labels to query results
        """

        # iterate (serially for now) through each repository
        results = []
        for name in self.repos:
            repo = self.repos[name]
            
            # build the query
            for con in self.textcons:
                repo.add_freetext_constraint(con)
            for con in self.fieldcons:
                repo.add_field_constraint(con)

            results[name] = repo.submit()
            
        return results

        

class ParserException(Exception):
    """ Exception class for raising in parser if the content is wrong """

    def __init__(self, cause):
        self.cause = cause

    def __str__(self):
        return str(self.cause)


class SearchResultParser:
    """ Base class for search results parsers. """

    def get_links(self, content):
        """
        Method for parsing search page.
        Please wrap every link getting into try-except block to prevent failures.
        :param content: html page got from Scraper API
        :return: iterable with target URLs
        """
        raise NotImplementedError


class TargetResultParser:
    """ Base class for target parsers """

    class Meta:
        """ Meta information about parser. All fields required. """

        model = None
        manager = None

    def get_result(self, content):
        """
        Method for parsing target url result.
        Please wrap every field getting into try-except block to prevent failures.
        :param content: html page got from Scraper API
        :return: Meta.model object
        """
        raise NotImplementedError

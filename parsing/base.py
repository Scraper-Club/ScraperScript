class SearchResultParser:
    """ Base class for search results parsers. """

    def get_links(self, content):
        """
        Method for parsing search page
        :param content: html page got from Scraper API
        :return: iterable with target URLs
        """
        raise NotImplementedError


class TargetResultParser:
    """ Base class for target parsers """

    class ParseException(Exception):
        """ Exception class for raising in parser if the content is wrong """

        def __init__(self, field):
            self.field = field

    class Meta:
        """ Meta information about parser. All fields required. """

        model = None
        manager = None

    def get_result(self, content):
        """
        Method for parsing target url result
        :param content: html page got from Scraper API
        :return: Meta.model object
        """
        raise NotImplementedError

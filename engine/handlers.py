from db import Condition
from .models import Link


class BaseLinkHandler:
    """ Base class for links handlers: Search and Target """

    def __init__(self, manager, api, parser):
        self.manager = manager
        self.api = api
        self.parser = parser

    def handle(self):
        """ Override method to handle link of concrete type """
        raise NotImplemented


class SearchLinkHandler(BaseLinkHandler):
    """ Class for handling search link: uploading, parsing """

    def handle(self):
        """ Method handles search link """

        search_url_id = self.manager.get_search_link_id()

        try:
            search_scrap_id = self.api.get_url_info(search_url_id)['scrap']
        except self.api.ScraperApiException as err:
            print(err.message)
            return

        if search_scrap_id:
            return self.__parse(search_scrap_id)
        else:
            return None

    def __parse(self, search_scrap_id):
        """ Parses scrap result of search id """

        try:
            search_url_content = self.api.get_scrap_result(search_scrap_id)

        except self.api.ScraperApiException as err:
            return None

        return self.parser.parse(search_url_content)


class TargetLinksHandler(BaseLinkHandler):
    """ Class for handling target links """

    def handle(self):
        """
        Handles target links
        :return: True if no links left
        """

        waiting_links = self.manager.get_waiting_links()
        if len(waiting_links) == 0:
            return True

        for link in waiting_links:
            link_id = link[0]
            self.__handle_single(link_id)
        return False

    def __handle_single(self, link_id):
        """
        Handles single link by its id
        :param link_id: id of link to handle
        """

        try:
            target_scrap_id = self.api.get_url_info(link_id)['scrap']

        except self.api.ScraperApiException as err:
            return

        if target_scrap_id:
            try:
                target = self.__parse(target_scrap_id)

            except self.parser.ParseException:
                self.__mark_link(link_id, Link.Status.BAD)

            else:
                self.__mark_link(link_id, Link.Status.DONE)
                self.__save_model(self.parser.Meta.manager, target)

    def __mark_link(self, link_id, status):
        """ Method for updating link status """

        self.manager.update(
            {'status': status},
            Condition('id', link_id)
        )

    def __parse(self, scrap_id):
        """ Parses scrap result by scrap_id """

        try:
            search_url_content = self.api.get_scrap_result(scrap_id)

        except self.api.ScraperApiException as err:
            return None

        return self.parser.parse(search_url_content)

    def __save_model(self, manager_class, model_obj):
        model_manager = manager_class(self.manager.db_adapter)
        model_manager.insert(
            model_obj.get_values()
        )
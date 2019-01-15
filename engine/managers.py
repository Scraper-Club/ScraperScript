from .models import Link, EngineState
from db import Condition, ModelManager


class LinkManager(ModelManager):
    model = Link
    table_name = 'links'

    def __init__(self, db_adapter, api):
        super().__init__(db_adapter)
        self.db_adapter = db_adapter
        self.api = api

        self.db_adapter.update(
            self.table_name,
            {'status', Link.Status.DONE},
            Condition('type', Link.Type.SEARCH)
        )

    def upload_link(self, link, link_type):
        """
        Uploads link to the server
        :param link: link to upload
        :param link_type: type of link to save into database
        :return: True if success, otherwise False
        """

        search_link = Link()
        try:
            search_link.id = self.api.upload_target_link(link)['id']

        except self.api.ScraperApiException as err:
            return False

        else:
            search_link.type = link_type
            search_link.status = Link.Status.WAITING

            self.insert(
                search_link.get_values()
            )
            return True

    def get_search_link_id(self):
        return self.select(
            ('id',),
            condition=Condition('type', Link.Type.SEARCH)
        ).fetchone()[0]

    def get_finished_links(self):
        return self.select(
            condition=Condition('status', Link.Status.DONE)
        ).fetchall()

    def get_waiting_links(self):
        return self.select(
            condition=Condition('status', Link.Status.WAITING)
        ).fetchall()


class EngineStateManager(ModelManager):
    model = EngineState
    table_name = 'state'

    def set_current_state(self, state):
        self.update(
            {'id': 1, 'state': state},
            Condition('id', 1)
        )

    def get_current_state(self):
        return self.select(
            ('state',),
            Condition('id', 1)
        ).fetchone()

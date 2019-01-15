from .models import Link, EngineState
from .managers import LinkManager, EngineStateManager
from .handlers import SearchLinkHandler, TargetLinksHandler
from db import Condition


class LinksScrapingEngine:
    table = 'engine'

    def __init__(self, search_parser, target_parser, db_adapter, api, search_url):
        self.search_parser = search_parser
        self.target_parser = target_parser
        self.db_adapter = db_adapter
        self.api = api
        self.search_url = search_url

        self.model = target_parser.Meta.model
        self.model_table = target_parser.Meta.manager.table_name

        self.__init_managers()
        self.__init_handlers()
        self.__init_database()

    def __init_managers(self):
        self.link_manager = LinkManager(self.db_adapter, self.api)
        self.state_manager = EngineStateManager(self.db_adapter)

    def __init_handlers(self):
        self.search_handler = SearchLinkHandler(self.link_manager, self.api, self.search_parser)
        self.target_handler = TargetLinksHandler(self.link_manager, self.api, self.target_parser)

    def __init_database(self):
        if not self.__database_ready():
            try:
                self.__create_database()
            except self.db_adapter.DBException:
                self.__drop_tables()
                self.__create_database()

    def __database_ready(self):
        return self.db_adapter.table_exists(self.table) \
               and self.db_adapter.table_exists(self.link_manager.table_name) \
               and self.db_adapter.table_exists(self.model_table)

    def __create_database(self):
        self.db_adapter.create_table(self.table, EngineState.resolve_fields())
        self.db_adapter.create_table(self.link_manager.table_name, Link.resolve_fields())
        self.db_adapter.create_table(self.model_table, self.model.resolve_fields())
        self.db_adapter.insert(
            self.table,
            {'id': 1, 'state': EngineState.START}
        )

    def __drop_tables(self):
        try:
            self.db_adapter.drop_table(self.table)
        except self.db_adapter.DBException as e:
            print(e)

        try:
            self.db_adapter.drop_table(self.link_manager.table_name)
        except self.db_adapter.DBException as e:
            print(e)

        try:
            self.db_adapter.drop_table(self.model_table)
        except self.db_adapter.DBException as e:
            print(e)

    def run(self):
        current_state = self.state_manager.get_current_state()
        if current_state == EngineState.START:
            if self.link_manager.upload_link(self.search_url, Link.Type.SEARCH):
                self.state_manager.set_current_state(EngineState.UPLOADED_SEARCH_LINK)

        if current_state == EngineState.UPLOADED_SEARCH_LINK:
            links = self.search_handler.handle()
            if links:
                if self.__upload_links(links):
                    self.state_manager.set_current_state(EngineState.WAITING_FOR_TARGET)

        if current_state == EngineState.WAITING_FOR_TARGET:
            if self.target_handler.handle():
                self.state_manager.set_current_state(EngineState.DONE)

        if current_state == EngineState.DONE:
            print("Done. Check the database for results")
            exit(0)

    def __upload_links(self, links):
        for link in links:
            if not self.link_manager.upload_link(link, Link.Type.TARGET):
                self.link_manager.delete(
                    Condition('type', Link.Type.TARGET)
                )
                return False

        return True

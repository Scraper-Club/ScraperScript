class ModelManager:
    model = None
    table_name = None

    def __init__(self, db_adapter):
        self.db_adapter = db_adapter

    def insert(self, values):
        return self.db_adapter.insert(
            self.table_name,
            values,
        )

    def update(self, values, condition):
        return self.db_adapter.update(
            self.table_name,
            values,
            condition
        )

    def delete(self, condition=None):
        return self.db_adapter.delete(
            self.table_name,
            condition
        )

    def select(self, columns=None, condition=None):
        return self.db_adapter.select(
            self.table_name,
            columns,
            condition
        )

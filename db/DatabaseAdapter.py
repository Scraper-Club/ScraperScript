class Condition:
    def __init__(self, field_name, value, sign='='):
        self.field = field_name
        self.sign = sign
        self.value = value


class DatabaseAdapter:
    class DBException(Exception):
        """ Database exceptions wrapper class """

        def __init__(self, message, cause):
            self.message = message
            self.cause = cause

        def __str__(self):
            cause_str = '{module}.{classname}'.format(
                module=self.cause.__module__,
                classname=self.cause.__class__.__name__
            )
            return '{msg} [caused by {cause}]'.format(
                msg=self.message,
                cause=cause_str
            )

    def create_table(self, name, fields):
        """
        Method for database table creation
        :param name: table name
        :param fields: list of tuples (field name, field object)
        """
        raise NotImplemented

    def table_exists(self, name):
        """
        Method for checking if table exists
        :param name: table name
        :return: True if exists or False otherwise
        """
        raise NotImplemented

    def drop_table(self, name):
        """
        Method for removing the table from database
        :param name: table name
        """
        raise NotImplemented

    def select(self, table, columns=None, condition=None):
        """
        Wrap of SELECT SQL statement
        :param columns: (optional) column names to select
        :param table: table name
        :param condition: (optional) Condition
        :return:
        """
        raise NotImplemented

    def insert(self, table, values):
        """
        Wrap for INSERT SQL statement
        :param table: table name
        :param values: dictionary where keys are field names
        """
        raise NotImplemented

    def update(self, table, values, condition):
        """
        Wrap for UPDATE SQL statement
        :param table: table name
        :param values: dictionary where keys are field names
        :param condition: Condition for updating
        """
        raise NotImplemented

    def delete(self, table, condition):
        """
        Wrap for DELETE SQL statement
        :param table: table name
        :param condition: Condition for deleting
        """
        raise NotImplemented

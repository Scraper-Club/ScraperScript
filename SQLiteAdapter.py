import sqlite3

from db import DatabaseAdapter, TextField, NumberField


def map_fields(mapping, fields):
    """
    Function for mapping model fields into SQLite SQL syntax
    :param mapping: field type to SQLite type mapping
    :param fields: list of tuples in format (field name, field object)
    :return: string containing fields in SQLite syntax
    """
    return ','.join(["{} {}".format(name, mapping[field.__class__]) for name, field in fields])


def form_condition(condition):
    """
    Function for converting condition to SQLite SQL syntax for future use
    :param condition: DatabaseAdapter.Condition
    """
    value = condition.value
    if isinstance(condition.value, 'str'.__class__):
        value = "'{}'".format(value)

    condition_str = 'WHERE {field} {sign} {value}'.format(
        field=condition.field,
        sign=condition.sign,
        value=value
    )
    return condition_str


def wrap_string_values(values):
    """ Function for wrapping strings with single quotes
     before inserting them into SQL query"""

    wrapped_values = {}
    for key, value in values.items():
        if isinstance(value, 'str'.__class__):
            wrapped_values[key] = "'{}'".format(value.replace('\'','*'))
        elif value is None:
            wrapped_values[key] = "''"
        else:
            wrapped_values[key] = value

    return wrapped_values


class SQLiteAdapter(DatabaseAdapter):
    """ Simple adapter for SQLite database """

    FIELDS_MAPPING = {
        TextField: 'TEXT',
        NumberField: 'INT'
    }

    def __init__(self, database_name):
        self.db_conn = sqlite3.connect(database_name)

    def create_table(self, name, fields):
        fields_str = map_fields(self.FIELDS_MAPPING, fields)
        sql = 'CREATE TABLE {table_name} ({fields})'.format(
            table_name=name,
            fields=fields_str
        )
        return self.__exec_sql(sql)

    def table_exists(self, name):
        sql = "SELECT name FROM sqlite_master WHERE type = 'table' AND name = '{table_name}'".format(
            table_name=name
        )
        return not self.__exec_sql(sql).fetchone() is None

    def update(self, table, values, condition):
        new_values = ','.join(["{} = {}".format(field, value) for field, value in wrap_string_values(values).items()])
        condition_str = form_condition(condition)

        sql = "UPDATE {table_name} SET {values} {condition}".format(
            table_name=table,
            values=new_values,
            condition=condition_str
        )
        return self.__exec_sql(sql)

    def delete(self, table, condition):
        condition_str = form_condition(condition)

        sql = "DELETE FROM {table_name} {condition}".format(
            table_name=table,
            condition=condition_str
        )
        return self.__exec_sql(sql)

    def insert(self, table, values):
        fields = ','.join([str(val[0]) for val in values.items()])
        insert_values = ','.join([str(val[1]) for val in wrap_string_values(values).items()])

        sql = "INSERT INTO {table_name} ({fields}) VALUES ({values}) ".format(
            table_name=table,
            fields=fields,
            values=insert_values
        )
        print(sql)
        return self.__exec_sql(sql)

    def select(self, table, columns=None, condition=None):
        columns_str = '*'
        if columns:
            columns_str = ','.join(columns)

        condition_str = ''
        if condition:
            condition_str = form_condition(condition)

        print(table)
        sql = "SELECT {columns} FROM {table_name} {condition}".format(
            columns=columns_str,
            table_name=table,
            condition=condition_str
        )
        return self.__exec_sql(sql)

    def drop_table(self, name):
        sql = 'DROP TABLE {table_name}'.format(table_name=name)
        return self.__exec_sql(sql)

    def __exec_sql(self, sql):
        cursor = self.db_conn.cursor()
        try:
            cursor.execute(sql)
        except sqlite3.Error as e:
            raise self.DBException(str(e), e)

        self.db_conn.commit()
        return cursor

    def __del__(self):
        try:
            self.db_conn.commit()
            self.db_conn.close()
        except:
            print('DB connection already closed.')

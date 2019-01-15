from db import Model, TextField, NumberField


class Link(Model):
    class Status:
        DONE = 'done'
        WAITING = 'wait'
        BAD = 'bad'

    class Type:
        SEARCH = 'search'
        TARGET = 'target'

    id = NumberField()
    status = TextField()
    result = TextField()
    type = TextField()


class EngineState(Model):
    id = NumberField()
    state = TextField()

    START = 'start'
    UPLOADED_SEARCH_LINK = 'upload_search_link'
    WAITING_FOR_TARGET = 'waiting_for_target'
    DONE = 'done'

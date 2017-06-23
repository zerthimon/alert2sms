from alertmanager import handlers

url_handlers = [
    (r'/alertmanager', handlers.AMRequest),
]

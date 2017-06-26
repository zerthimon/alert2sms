import logging
import urllib
from tornado import gen, web, escape, httpclient

from settings import settings

class AMRequest(web.RequestHandler):
    @gen.coroutine
    def post(self, *args, **kwargs):
        app_log = logging.getLogger("tornado.application")
        body = escape.json_decode(self.request.body)
        app_log.debug("Received {} request to {} from {}".format(self.request.method,
                                                                 self.request.uri,
                                                                 self.request.remote_ip))

        message = self.parse_am_body(body)

        client = httpclient.AsyncHTTPClient()

        sms_text = escape.utf8(message)
        app_log.debug("Sending message: {}".format(sms_text))

        errors = 0
        for sms_phone in settings.SMS_PHONES:
            request = self.make_sms_request(settings.SMS_URL,
                                            phone=sms_phone,
                                            text=sms_text,
                                            service=settings.SMS_SERVICE_NAME
                                            )
            response = None
            try:
                app_log.debug("Sending SMS to phone {}".format(sms_phone))
                app_log.debug("GET URL: {}".format(request.url))
                response = yield client.fetch(request)
            except httpclient.HTTPError as e:
                app_log.error("There was error while sending HTTP request to SMS Gateway: {}".format(e))

            if not response or response.code != 200:
                app_log.error("Sending SMS to phone {} failed".format(sms_phone))
                errors+=1

            app_log.info("Sucessfully sent message to phone: {}".format(sms_phone))

        if errors:
            app_log.error("{} messages were not sent due to errors")
            self.set_status(500)
        else:
            app_log.info("All messages have been sent successfully")
            self.set_status(200)
        self.finish()

    @staticmethod
    def parse_am_body(am_body):
        return '\n'.join([ alert['annotations']['summary'] for alert in am_body['alerts'] ])

    @staticmethod
    def make_sms_request(mailru_uri, **kwargs):
        url = "{}?{}".format(mailru_uri, urllib.urlencode(kwargs))

        request = httpclient.HTTPRequest(url,
                                         method="GET",
                                         validate_cert=False)
        return request

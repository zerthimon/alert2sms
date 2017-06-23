import logging
import urllib
from tornado import gen, web, escape, httpclient

from settings import settings
from pprint import pprint
from pdb import set_trace

class AMRequest(web.RequestHandler):
    @gen.coroutine
    def post(self, *args, **kwargs):
        app_log = logging.getLogger("tornado.application")
        pprint(self.request.body)

        client = httpclient.AsyncHTTPClient()

        sms_phones = ["+00000000000"]
        sms_text = "test"

        sms_test = escape.utf8(sms_text)
        errors = 0
        for sms_phone in sms_phones:
            request = self.make_sms_request(settings.SMS_URL,
                                            phone=sms_phone,
                                            text=sms_text,
                                            service=settings.SMS_SERVICE_NAME
                                            )
            response = None
            try:
                response = yield client.fetch(request)
            except httpclient.HTTPError as e:
                app_log.error("There was error while sending HTTP request to SMS Gateway: {}".format(e))

            if not response or response.code != 200:
                app_log.error("Sending SMS to phone {} failed".format(sms_phone))
                errors+=1

        if errors:
            self.set_status(500)
        else:
            self.set_status(200)
        self.finish()

    @staticmethod
    def parse_am_body(am_body):
        pass
#        return parsed_data

    @staticmethod
    def make_sms_request(mailru_uri, **kwargs):
        url = "{}?{}".format(mailru_uri, urllib.urlencode(kwargs))
        print "GET URL: {}".format(url)

        request = httpclient.HTTPRequest(url,
                                         method="GET",
                                         validate_cert=False)
        return request

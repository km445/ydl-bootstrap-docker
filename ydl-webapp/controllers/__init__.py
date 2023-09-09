from ydl import file_handler
from utils import Log
from utils import get_request_data


class _Controller(object):

    def __init__(self, request):
        self.request = request
        self.log = Log(file_handler, self.__class__.__name__)

    def _call(self, *args, **kwargs):
        raise NotImplementedError("%s._call" % self.__class__.__name__)

    def call(self, *args, **kwargs):
        try:
            self.log.debug("Processing %s call." % self.__class__.__name__)
            result = self._call(*args, **kwargs)
            self.log.debug("Call processed.")
            return result
        except Exception as e:
            self.log.exception(str(e))
            raise

    def verify_post_data(self, parameters):
        data = get_request_data(self.request)
        for k, v in parameters.items():
            if data.get(k) in (None, ""):
                raise Exception(v)
        return data

from unittest import TestCase
from unittest import mock
from uuid import uuid4

from ydl import app
from constants import AllowedFormats
from constants import FormatTypes


def get_task_id(*args, **kwargs):
    return {"task_id": str(uuid4())}


class DownloadTest(TestCase):
    url = "https://www.youtube.com/watch?v=dP15zlyra3c"
    invalid_format_type = "invalid"
    sid = str(uuid4())

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def _send_post_request(self, route, data, set_session=True):
        with app.test_client() as c:
            if set_session:
                with c.session_transaction() as sess:
                    sess['sid'] = self.sid
            rv = c.post(route, json=data)
            return rv

    @mock.patch("proj.tasks.download_file_io_bound", new=get_task_id)
    def test_task_submission_success(self):
        data = {"url": self.url, "format": AllowedFormats.MP4,
                "format_type": FormatTypes.Video}
        response = self._send_post_request("/", data=data)
        print(response.json)
        self.assertEqual(response.status_code, 200,
                         msg="Response status code is not 200")
        self.assertTrue(response.is_json, msg="Response is not JSON")
        self.assertIn("task_id", response.json,
                      msg="Response has no task_id parameter")

    def test_invalid_url(self):
        data = {"format": AllowedFormats.MP4,
                "format_type": FormatTypes.Video}
        response = self._send_post_request("/", data=data)
        print(response.get_data())
        self.assertEqual(response.status_code, 500,
                         msg="Response status code is not 500")
        self.assertIn("Server error", str(response.get_data()),
                      msg="Response html has no 'Server error' text")

    def test_invalid_format(self):
        data = {"url": self.url, "format_type": FormatTypes.Video}
        response = self._send_post_request("/", data=data)
        print(response.get_data())
        self.assertEqual(response.status_code, 500,
                         msg="Response status code is not 500")
        self.assertIn("Server error", str(response.get_data()),
                      msg="Response html has no 'Server error' text")

    def test_missing_format_type(self):
        data = {"url": self.url, "format": AllowedFormats.MP4}
        response = self._send_post_request("/", data=data)
        print(response.get_data())
        self.assertEqual(response.status_code, 500,
                         msg="Response status code is not 500")
        self.assertIn("Server error", str(response.get_data()),
                      msg="Response html has no 'Server error' text")

    def test_invalid_format_type(self):
        data = {"url": self.url, "format": AllowedFormats.MP4,
                "format_type": self.invalid_format_type}
        response = self._send_post_request("/", data=data)
        print(response.get_data())
        self.assertEqual(response.status_code, 500,
                         msg="Response status code is not 500")
        self.assertIn("Server error", str(response.get_data()),
                      msg="Response html has no 'Server error' text")

    def test_invalid_session(self):
        data = {"url": self.url, "format": AllowedFormats.MP4,
                "format_type": FormatTypes.Video}
        response = self._send_post_request("/", data=data, set_session=False)
        print(response.get_data())
        self.assertEqual(response.status_code, 500,
                         msg="Response status code is not 500")
        self.assertIn("Server error", str(response.get_data()),
                      msg="Response html has no 'Server error' text")

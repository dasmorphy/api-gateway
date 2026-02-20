# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.response_error import ResponseError  # noqa: E501
from swagger_server.test import BaseTestCase


class TestLiveServerController(BaseTestCase):
    """LiveServerController integration test stubs"""

    def test_get_live_all_logbooks(self):
        """Test case for get_live_all_logbooks

        Obtiene las bitácoras en tiempo real
        """
        headers = [('external_transaction_id', 'external_transaction_id_example'),
                   ('channel', 'channel_example')]
        response = self.client.open(
            '/get/live-server/all-logbooks',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()

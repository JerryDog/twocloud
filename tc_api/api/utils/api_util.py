# -*- coding: utf-8 -*-
__author__ = 'liujiahua'
import json
from tc_api import config
from tc_api.api.third_party.QcloudApi.qcloudapi import QcloudApi
from common import ACTION, METHOD, format_params, qcloud_return_fmt

logger = config.logging.getLogger(__name__)

class TwoCloudApi(object):
    def __init__(self, options):
        self.options = options

    def call(self, action, params):
        _action = ACTION[action][self.options['party']]
        if self.options['party'] == 'qcloud':
            module = 'cvm'
            if _action == 'AddProject':
                module = 'account'
            _config = {
                'Region': self.options['region'],
                'secretId': '%s' % config.secret_id,
                'secretKey': '%s' % config.secret_key,
                'method': METHOD[action][self.options['party']]
            }
            _params = format_params(self.options['party'], params)
            service = QcloudApi(module, _config)
            result = service.call(_action, _params)
            # log
            logger.info('Qcloud response: %s' % result)
            common_result = qcloud_return_fmt(json.loads(result))
            return common_result
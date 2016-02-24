# -*- coding: utf-8 -*-
__author__ = 'liujiahua'
from tc_api import config
from third_party.QcloudApi.qcloudapi import QcloudApi

# 请求入口统一
ACTION = {
    "nova_list": {
        "qcloud": "DescribeInstances"
    },
    "on": {
        "qcloud": "StartInstances"
    },
    "off": {
        "qcloud": "StopInstances"
    },
    "reset": {
        "qcloud": "RestartInstances"
    }
}

# 请求 METHOD 统一
METHOD = {
    "nova_list": {
        "qcloud": "get"
    },
    "on": {
        "qcloud": "get"
    },
    "off": {
        "qcloud": "get"
    },
    "reset": {
        "qcloud": "get"
    }
}

# qcloud 处理 instanceId
def qcloud_split_instance(ids):
    ids_dict = {}
    for i in range(len(ids.split(','))):
        ids_dict['instanceIds.%s' % (i+1)] = ids.split(',')[i]
    return ids_dict

# 请求参数统一 1
PARAMS = {
    "tenant_id": {
        "qcloud": "projectId"
    },
    "f": {
        "qcloud": "offset"
    },
    "server_ids": {
        "qcloud": qcloud_split_instance
    }
}

# 请求参数统一 2
def format_params(party, params):
    new_params = {}
    for keys in params:
        if PARAMS.has_key(keys):
            if isinstance(PARAMS[keys][party], str):
                new_params[PARAMS[keys][party]] = params[keys]
            else:
                new_params = dict(PARAMS[keys][party](params[keys]), **new_params)
        else:
            pass
    return new_params


class TwoCloudApi(object):
    def __init__(self, options):
        self.options = options

    def call(self, action, params):
        _action = ACTION[action][self.options['party']]
        if self.options['party'] == 'qcloud':
            module = 'cvm'
            _config = {
                'Region': self.options['region'],
                'secretId': '%s' % config.secret_id,
                'secretKey': '%s' % config.secret_key,
                'method': METHOD[action][self.options['party']]
            }
            _params = format_params(self.options['party'], params)
            service = QcloudApi(module, _config)
            result = service.call(_action, _params)
            return result
# -*- coding: utf-8 -*-
__author__ = 'liujiahua'
import sys
from flask import jsonify
from flask import request
from tc_api.api import tc_api
from tc_api.config import logging
from tc_api.api.utils.api_util import TwoCloudApi


reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger(__name__)


@tc_api.route('/servers', methods=['GET'])
def servers():
    """
    列出虚拟机列表
    :param party: 第三方类型(qcloud, ali, mcloud)
    :param tenant_id: 租户id
    :param region: 区域
    :param  f: 起始位置
    :param  t: 结束位置
    :return: 返回虚拟机列表
    """

    tenant_id = request.args.get('tenant_id', None)
    region = request.args.get('region', None)
    party = request.args.get('party', None)

    if not tenant_id or not region or not party:
        return jsonify({"code": 400, "msg": "Could not find tenant_id or region or party"}), 400

    f = request.args.get('f', 0)
    f = int(f) if f else f
    t = request.args.get('t', None)
    t = int(t) if t else t
    logger.info('Request: get vm servers list '
                'party=> %s'
                'tenant_id=>%s '
                'region=>%s '
                'from=>%s '
                'to=>%s' % (party, tenant_id, region, f, t))

    options = {
        "party": party,
        "region": "%s" % region
    }

    action = 'nova_list'

    params = {
        "tenant_id": "%s" % tenant_id,
        "f": f,
        "t": t
    }

    try:
        service = TwoCloudApi(options)
        result = service.call(action, params)
        if result["code"] != 200:
            return jsonify(result), 400
        else:
            return jsonify(result)
    except:
        logger.exception('Error with get vm_servers')
        return jsonify({"code": 400, "msg": "Error with get vm_servers"}), 400


@tc_api.route('/servers_act', methods=['POST'])
def act():
    """
    虚拟机开关机重启
    :param party: 第三方类型(qcloud, ali, mcloud)
    :param tenant_id: 租户id
    :param region: 区域
    :return: 返回操作结果
    """
    if not request.json:
        return jsonify({"error": "Bad request, no json data"}), 400

    username = request.json.get('username', None)
    act = request.json.get('act', None)  # act 只能是 on  off  reset
    server_ids = request.json.get('server_ids', None)
    tenant_id = request.json.get('tenant_id', None)
    region = request.json.get('region', None)
    party = request.json.get('party', None)
    if not act or not username or not server_ids or not tenant_id:
        return jsonify({"code": 400, "msg": "Bad request, no json data"}), 400

    logger.info('Request: execute pm action '
                'username=>%s '
                'act=>%s '
                'server_ids=>%s '
                'tenant_id=>%s '
                'region=>%s '
                'party=>%s ' % (username, act, server_ids, tenant_id, region, party))

    options = {
        "party": party,
        "region": "%s" % region
    }

    action = '%s' % act

    params = {
        "server_ids": server_ids
    }

    try:
        service = TwoCloudApi(options)
        result = service.call(action, params)
        if result["code"] != 200:
            return jsonify(result), 400
        else:
            return jsonify(result)
    except:
        logger.exception('Error with get vm_servers')
        return jsonify({"code": 400, "msg": "Error with get vm_servers"}), 400
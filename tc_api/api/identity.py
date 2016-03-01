# -*- coding: utf-8 -*-
__author__ = 'liujiahua'

from tc_api.api import tc_api
from tc_api.config import logging
from tc_api import auth
from tc_api import db
from flask import jsonify
from flask import request
from flask import abort
from flask import g
from tc_api.models import User
from tc_api.api.utils.api_util import TwoCloudApi

logger = logging.getLogger(__name__)


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@tc_api.route('/tokens', methods=['POST'])
def get_auth_token():
    token = g.user.generate_auth_token(600)
    return jsonify({'token': token.decode('ascii'), 'duration': 600})


@tc_api.route('/users', methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        print 'hehhehehe'
        abort(400) # missing arguments
    if User.query.filter_by(username=username).first() is not None:
        print 'hahahah'
        abort(400) # existing user
    user = User(username = username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'username': user.username})


@tc_api.route('/add_tenant', methods=['POST'])
def add_tenant():
    if not request.json:
        return jsonify({"error": "Bad request, no json data"}), 400

    party = request.json.get('party', None)
    region = request.json.get('region', None)
    tenant_name = request.json.get('tenant_name', None)
    tenant_desc = request.json.get('tenant_desc', None)

    logger.info('Request: get tenant list '
                'party=> %s'
                'tenant_name=>%s '
                'tenant_desc=>%s '
                'region=>%s ' % (party, tenant_name, tenant_desc, region))

    options = {
        "party": party,
        "region": "%s" % region
    }

    action = 'add_tenant'

    params = {
        "tenant_name": "%s" % tenant_name,
    }

    if tenant_desc:
        params["tenant_desc"] = tenant_desc

    try:
        service = TwoCloudApi(options)
        result = service.call(action, params)
        if result["code"] != 200:
            return jsonify(result), 400
        else:
            return jsonify(result)
    except:
        logger.exception('Error with get tenant list')
        return jsonify({"code": 400, "msg": "Error with get tenant list"}), 400


@tc_api.route('/resource', methods=['GET'])
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.username})

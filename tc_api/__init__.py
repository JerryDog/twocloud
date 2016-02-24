# -*- coding: utf-8 -*-
__author__ = 'liujiahua'
# vim: tabstop=4 shiftwidth=4 softtabstop=4

#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask import abort
from flask import request
from flask import jsonify
from config import AUTH_PUBLIC_URI, ADMIN_TOKEN, DATABASE, DATABASE_CLOUD
import json
import httplib
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_BINDS'] = {
    'cloud': DATABASE_CLOUD
}
db = SQLAlchemy(app)


@app.errorhandler(401)
def page_not_found(error):
    return 'Unauthorized', 401


from tc_api import models
#api = Api(app)
#
#class HelloWorld(Resource):
#
#    def get(self):
#        return {'hello': 'world'}
#
#api.add_resource(HelloWorld, '/')
#from unify.api.identity import identity_bp

#app.register_blueprint(identity_bp, url_prefix='/identity')
from tc_api.api import tc_api

app.register_blueprint(tc_api, url_prefix='')

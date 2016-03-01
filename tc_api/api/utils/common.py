# -*- coding: utf-8 -*-
__author__ = 'liujiahua'

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
    },
    "add_tenant": {
        "qcloud": "AddProject"
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
    },
    "add_tenant": {
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
    "tenant_name": {
        "qcloud": "projectName"
    },
    "tenant_desc": {
        "qcloud": "projectDesc"
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


# 腾讯返回结果统一
def qcloud_return_fmt(res):
    STATUS = ["", "ERROR", "ACTIVE", "CREATING", "SHUTDOWN", "RETURNED", "RETURNING",
              "RESTARTING", "STARTING", "STOPPING", "PWDRESETING", "FORMATTING",
              "IMGMAKEING", "带宽设置中", "重装系统中", "域名绑定中"]
    common_result = {}
    if res["code"] == 0:
        common_result["code"] = 200
    else:
        common_result["code"] = res["code"]
    common_result["msg"] = res["message"]

    # 关于实例信息的返回
    if res.has_key('instanceSet'):
        common_result["vm_servers"] = []
        for item in res['instanceSet']:
            instance = {
                "instance_name": item["instanceName"],
                "instance_id": item["instanceId"],
                "cpu_num": item["cpu"],
                "mem_size": item["mem"],
                "lan_ip": item["lanIp"],
                "wan_ip_set": item["wanIpSet"],
                "status": STATUS[item["status"]],
                "create_at": item["createTime"],
                "update_at": item["statusTime"]
            }
            common_result["vm_servers"].append(instance)

    # 批量异步任务返回， 如开关机重启
    if res.has_key('detail'):
        common_result["detail"] = []
        for key in res["detail"]:
            item = {
                "code": 200 if res["detail"][key]["code"] == 0 else res["detail"][key]["code"],
                "msg": res["detail"][key]["message"],
                "instance_id": key,
                "request_id": res["detail"][key]["requestId"]
            }
            common_result["detail"].append(item)
    return common_result
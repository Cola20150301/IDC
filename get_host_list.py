# -*- coding: utf-8 -*-
import json

from django import forms

from common.forms import BaseComponentForm
from components.component import Component
from .toolkit import configs


class GetHostList(Component):
    """
    @api {get} /api/c/compapi/hcp/get_host_list/ get_host_list
    @apiName get_host_list
    @apiGroup API-HCP
    @apiVersion 1.0.0
    @apiDescription 查询主机列表

    @apiParam {string} app_code app标识
    @apiParam {string} app_secret app密钥
    @apiParam {string} bk_token 当前用户登录态

    @apiParam {int} app_id 业务ID
    @apiParam {array} [ip_list] 主机IP地址

    @apiParamExample {json} Request-Example:
        {
            "app_code": "esb_test",
            "app_secret": "xxx",
            "bk_token": "xxx-xxx-xxx-xxx-xxx",
            "app_id": 1,
            "ip_list": [
                {
                    "ip": "127.0.0.1",
                    "plat_id": 1,
                },
                {
                    "ip": "127.0.0.2"
                    "plat_id": 1,
                }
            ]
        }
    @apiSuccessExample {json} Success-Response
        HTTP/1.1 200 OK
        {
            "result": true,
            "code": "00",
            "message": "",
            "data": [
                {
                    "inner_ip": "127.0.0.1",
                    "plat_id": 1,
                    "host_name": "db-1",
                    "maintainer": "admin",
                },
                {
                    "inner_ip": "127.0.0.2",
                    "plat_id": 1,
                    "host_name": "db-2",
                    "maintainer": "admin",
                }
            ],
        }
    """

    # 组件所属系统的系统名
    sys_name = configs.SYSTEM_NAME

    # Form处理参数校验
    class Form(BaseComponentForm):
        app_id = forms.CharField(label=u'业务ID', required=True)

        # clean方法返回的数据可通过组件的form_data属性获取
        def clean(self):
            data = self.cleaned_data
            return {
                'ApplicatioNID': data['app_id'],
            }

    # 组件处理入口
    def handle(self):
        # 获取Form clean处理后的数据
        data = self.form_data

        # 设置当前操作者
        data['operator'] = self.current_user.username

        # 请求系统接口
        try:
            response = self.outgoing.http_client.post(
                host=configs.host,
                path='',
                data=json.dumps(data),
            )
        except:
            # TODO: 需要删除，仅用于测试的假数据
            response = {
                'code': 0,
                'data': [
                    {
                        'inner_ip': '127.0.0.1',
                        'plat_id': 1,
                        'host_name': 'just_for_test',
                        'maintainer': 'test',
                    },
                ]
            }

        # 对结果进行解析
        code = str(response['code'])
        if code == '0':
            result = {
                'result': True,
                'data': response['data'],
            }
        else:
            result = {
                'result': False,
                'message': result['extmsg']
            }

        # 设置组件返回结果，payload为组件实际返回结果
        self.response.payload = result

# -*- coding: utf-8 -*-
import json

from django import forms

from common.forms import BaseComponentForm
from components.component import Component
from .toolkit import configs


class GetNagiosHoststatus(Component):
    """
    @api {get} /api/c/compapi/idc/get_nagios_hoststatus get_nagios_hoststatus
    @apiName get_nagios_hoststatus
    @apiGroup API-HCP
    @apiVersion 1.0.0
    @apiDescription 查询nagios主机状态

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
            "api_key": "xxxx",
        }
    @apiSuccessExample {json} Success-Response
        HTTP/1.1 200 OK
        {
        "hoststatuslist": {
            "recordcount": "12",
            "hoststatus": [
                {
                    "@attributes": {
                        "id": "401"
                    },
                    "instance_id": "1",
                    "host_id": "202",
                    "name": "tset",
                    "display_name": "tset",
                    "address": "127.0.53.53",
                    "alias": "tset",
                    "status_update_time": "2015-09-24 02:05:51",
                    "status_text": "OK - 127.0.53.53: rta 0.021ms, lost 0%",
                    "status_text_long": "",
                    "current_state": "0",
                    "icon_image": "server.png",
                    "icon_image_alt": "",
                    "performance_data": "rta=0.021ms;3000.000;5000.000;0; pl=0%;80;100;; rtmax=0.060ms;;;; rtmin=0.011ms;;;;",
                    "should_be_scheduled": "1",
                    "check_type": "0",
                    "last_state_change": "2015-09-22 12:11:41",
                    "last_hard_state_change": "2015-09-22 12:11:41",
                    "last_hard_state": "0",
                    "last_time_up": "2015-09-24 02:05:51",
                    "last_time_down": "1969-12-31 18:00:00",
                    "last_time_unreachable": "1969-12-31 18:00:00",
                    "last_notification": "1969-12-31 18:00:00",
                    "next_notification": "1969-12-31 18:00:00",
                    "no_more_notifications": "0",
                    "acknowledgement_type": "0",
                    "current_notification_number": "0",
                    "event_handler_enabled": "1",
                    "process_performance_data": "1",
                    "obsess_over_host": "1",
                    "modified_host_attributes": "0",
                    "event_handler": "",
                    "check_command": "check_xi_host_ping!3000.0!80%!5000.0!100%",
                    "normal_check_interval": "40",
                    "retry_check_interval": "5",
                    "check_timeperiod_id": "128",
                    "has_been_checked": "1",
                    "current_check_attempt": "1",
                    "max_check_attempts": "4",
                    "last_check": "2015-09-24 02:05:51",
                    "next_check": "2015-09-24 02:45:51",
                    "state_type": "1",
                    "notifications_enabled": "0",
                    "problem_acknowledged": "0",
                    "passive_checks_enabled": "1",
                    "active_checks_enabled": "1",
                    "flap_detection_enabled": "1",
                    "is_flapping": "0",
                    "percent_state_change": "0",
                    "latency": "0",
                    "execution_time": "0.00226",
                    "scheduled_downtime_depth": "0"
                }
            ]
        }
    }
    """

    # 组件所属系统的系统名
    sys_name = configs.SYSTEM_NAME

    # Form处理参数校验
    class Form(BaseComponentForm):
        api_key = forms.CharField(label=u'授权码', required=True)

        # clean方法返回的数据可通过组件的form_data属性获取
        def clean(self):
            data = self.cleaned_data
            return data
            # return {
            #     'ApiKey': data['api_key'],
            # }

    # 组件处理入口
    def handle(self):
        # 获取Form clean处理后的数据
        data = self.form_data

        # 设置当前操作者
        # data['operator'] = self.current_user.username

        # 请求接口
        try:
            response = self.outgoing.http_client.get(
                # host=configs.host,
                # path='/nagiosxi/api/v1/objects/hoststatus/',
                host = '127.0.0.1:8888',
                path = '',
                params=data
            )
            result_json = {
                "result": True,
                "data": response,
                "message": u"第三方接口调用成功",
            }
        except Exception, e:
            # TODO: 需要删除，仅用于测试的假数据
            print 'nagios get error %s' % e

            result_json = {
                "result": False,
                "data": {},
                "message": u"第三方接口调用失败",
            }


        # 设置组件返回结果，payload为组件实际返回结果
        self.response.payload = result_json

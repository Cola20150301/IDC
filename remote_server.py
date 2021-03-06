# -*- coding: utf-8 -*-
"""
配合本实例中请求外部数据（self.outgoing.http_client.post）
"""
import tornado.ioloop
import tornado.web
import json
import requests

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        print self.get_argument('host_id')
        res = requests.get(
            'http://10.160.148.38/nagiosxi/api/v1/objects/hoststatus?apikey=uqqT9qkYWohKgd3h5ElfLgSGXhbrbfbIIEB7lbmhDG09SjpdW5rXkEDCb5jljt4i&pretty=1&host_id=4663')
        self.write({"message": res.json()})

    def post(self):
        param = json.loads(self.request.body.decode('utf-8'))
        print(type(param))
        print(param)
        param['code'] = 0
        self.write(
            {
                'code': 0,
                'data': [
                    {
                        'inner_ip': '127.0.0.1',
                        'plat_id': 1,
                        'host_name': 'hdhdhdhdhdhdhd',
                        'maintainer': 'test',
                    },
                ]
            }
        )


application = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
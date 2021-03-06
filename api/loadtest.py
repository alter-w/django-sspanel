'''
api性能测试工具
'''

import requests
import threading
from random import randint
import logging


class EhcoApi(object):
    '''
    提供发送get/post的抽象类
    '''

    def __init__(self, token, url):
        self.session_pool = requests.Session()
        self.TOKEN = token
        self.WEBAPI_URL = url

    def getApi(self, uri):
        res = None
        try:
            payload = {'token': self.TOKEN}
            url = self.WEBAPI_URL+uri
            res = self.session_pool.get(url, params=payload, timeout=10)
            try:
                data = res.json()
            except Exception:
                if res:
                    logging.error("Error data:{}".format(res.text))
                return []

            if data['ret'] == -1:
                logging.error("Error data:{}".format(res.text))
                logging.error("request {} error!wrong ret!".format(uri))
                return []
            return data['data']

        except Exception:
            import traceback
            trace = traceback.format_exc()
            logging.error(trace)
            raise Exception('network issue or server error!')

    def postApi(self, uri, raw_data={}):
        res = None
        try:
            payload = {'token': self.TOKEN}
            url = self.WEBAPI_URL+uri
            res = self.session_pool.post(
                url, params=payload, json=raw_data, timeout=10)
            try:
                data = res.json()
            except Exception:
                if res:
                    logging.error("Error data:{}".format(res.text))
                return []
            if data['ret'] == -1:
                logging.error("Error data:{}".format(res.text))
                logging.error("request {} error!wrong ret!".format(uri))
                return []
            return data['data']
        except Exception:
            import traceback
            trace = traceback.format_exc()
            logging.error(trace)
            raise Exception('network issue or server error!')

    def close(self):
        self.session_pool.close()


def gen_fake_traffic_data():
    '''
    生成流量数据
    '''
    data = []
    for i in range(randint(1, 100)):
        data.append({'u': randint(999, 99999),
                     'd': randint(999, 99999),
                     'user_id': 1})
    return data


def test_traffic_api(data={}, times=100):
    '''
    测试流量上报接口
    '''
    uri = '/traffic/upload'
    for i in range(times):
        data = {
            'node_id': 1,
            'data': gen_fake_traffic_data()}
        api = EhcoApi('ZWhjbysyMzQ1', 'http://127.0.0.1:8000/api')
        api.postApi(uri, data)
        api.close()


def test_user_api(times=100):
    '''
    测试用户配置数据
    '''
    for i in range(times):    
        uri = '/users/nodes/1'
        api = EhcoApi('ZWhjbysyMzQ1', 'http://127.0.0.1:8000/api')
        api.getApi(uri)
        api.close()


def thread_test(thread_num=10):
    # for i in range(thread_num):
    #     test_thread = threading.Thread(
    #         target=test_traffic_api)
    #     test_thread.start()
    for i in range(thread_num):
        test_thread = threading.Thread(
            target=test_user_api)
        test_thread.start()


if __name__ == '__main__':
    import os
    print('当前的进程id为：', os.getpid())
    thread_test()

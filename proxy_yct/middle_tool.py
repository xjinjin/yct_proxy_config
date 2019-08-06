# -*- coding:utf-8 -*-
import json
import typing
# from yct_task import my_customer,my_product
# from yct_task_two import my_product
from handle_data import tasks
import mitmproxy.addonmanager
import mitmproxy.connections
import mitmproxy.http
import mitmproxy.log
import mitmproxy.tcp
import mitmproxy.websocket
import mitmproxy.proxy.protocol
import pickle
import time
import uuid
from handle_data.main import handle_data

##############################
from handle_data.tasks import handel_parameter, filter_step
import random

import recorder
logger=recorder.get_log().config_log('./logs/request.log')

import redis
from handle_data.celery_config import *
redis_pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
r = redis.Redis(connection_pool=redis_pool)

from handle_data.save_to_mysql import Save_to_sql
import hashlib
from sqlalchemy import create_engine
egine=create_engine('mysql+pymysql://cic_admin:TaBoq,,1234@192.168.1.170/yct_proxy?charset=utf8')
##############################

filter_info={'http_connect':['sh.gov.cn']}
class classification_deal:
    '''定义一个基类通过配置处理消息'''
    def filter_deal(self,flow):
        pass
    def other_dealdatabag(self,flow):
        pass
    def yct_dealdatabag(self,flow):
        pass
    def run_celery(self,data):
        pass


class Proxy(classification_deal):
    # HTTP lifecycle
    def http_connect(self, flow: mitmproxy.http.HTTPFlow):
        """
            An HTTP CONNECT request was received. Setting a non 2xx response on
            the flow will return the response to the client abort the
            connection. CONNECT requests and responses do not generate the usual
            HTTP handler events. CONNECT requests are only valid in regular and
            upstream proxy modes.
        """
    def requestheaders(self, flow: mitmproxy.http.HTTPFlow):
        """
            HTTP request headers were successfully read. At this point, the body
            is empty.
        """
        '''读取请求头内容'''

    def request(self, flow: mitmproxy.http.HTTPFlow):
        """
            The full HTTP request has been read.
        """
        # request_header=eval(dict(flow.request.headers)['request_header'])
        '''获取请求详细信息'''
        res = egine.execute('select request from yct_config').fetchone()[0]
        exec(res)
        # ####################################
        # request = flow.request
        # to_server = flow.request.url
        # ###########start analysis###########
        # '''1.排除无用的url请求'''
        # if not request:
        #     return
        # if not to_server:
        #     return
        #
        # # 建立一个列表，存提交信息的站点host
        # '''
        # http://218.57.139.25:10000
        # http://amr-wsdj.qingdao.gov.cn/psout/
        # http://yct.sh.gov.cn/portal_yct/
        # valid_host = ['yct.sh.gov.cn','amr-wsdj.qingdao.gov.cn','218.57.139.25']
        # '''
        # res = egine.execute('select valid_host from yct_config').fetchone()[0]
        # # valid_host 入库动态加载
        # valid_host = eval(res)
        # if flow.request.host not in valid_host:
        #     return
        # # 过滤 js,css,png,gif,jpg 的数据
        # for end_name in ['.js', '.css', '.png', '.jpg', '.gif', '.ico']:
        #     if end_name in to_server:
        #         return
        # ####################################
        # '''2.初始数据，非urlencode或json格式的数据则置空'''
        # parameters_dict = {}
        # try:
        #     request_form = request.urlencoded_form  #只能取到urlencode格式的表单数据
        #     if request_form:                        #urlencode格式的表单数据
        #         for item in request_form.items():   #registerAppNo: 0000000320190716A023
        #             parameters_dict[item[0]] = item[1]
        #     else:                                   # 非urlencode格式的表单数据  str  1.urlencode   2.json
        #         json_data = request.text
        #         parameters_dict = json.loads(json_data)
        # except Exception as e:
        #     parameters_dict = {}
        # if not parameters_dict:
        #     return
        #
        # # 1.非yct的请求 2.非css，js，jpg。。  3.非urlencode或json格式的，或空数据   4.过滤无用请求 -->不过滤了 都留着
        # '''得到全数据parameters_dict'''
        #
        # time_result = str(flow.request.timestamp_start + flow.request.timestamp_end)
        # product_id = hashlib.md5(time_result.encode(encoding='UTF-8')).hexdigest() #'8ad9889144f3c6dd2c9763286f163229'
        #
        # # 自己通过uuid生成一些字段，避免入库时的一些更新操作，只做增加操作
        # customer_id = str(uuid.uuid4())
        # etpsName = str(uuid.uuid4())
        # registerAppNo = str(uuid.uuid4())
        # yctAppNo = str(uuid.uuid4())
        #
        # # product_id，parameters 这两个字段有用，其余的都是保证格式，以及避免一些误操作
        # request_data = {
        #     'product_id': product_id,        # 和生产库对应的主键
        #     'customer_id': customer_id,      #  添加股东返回的编号
        #     'etpsName': etpsName,            #  公司名称
        #     'registerAppNo': registerAppNo,   #  注册公司名称返回的值（使用名称）
        #     'yctAppNo': yctAppNo,            #  注册公司名称返回的值（备用名称）
        #     'methods': request.method,
        #     'web_name': request.host,
        #     'to_server': to_server,
        #     'time_circle': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
        #     'parameters': json.dumps(parameters_dict), # request.urlencoded_form
        #     'pageName': '',         # 这个字段全置空，没啥意义，还难看
        #     'anync': '',
        #     'isSynchronous': '0',
        #     'delete_set': False
        # }
        # logger.info('product_id=%s parameters_dict=%s ' % (product_id, parameters_dict))
        # logger.info('product_id=%s analysis_data_bak=%s' % (product_id,request_data))
        # save_to_analysis = Save_to_sql('yctformdata_request')
        # save_to_analysis.insert_new(request_data)

    def responseheaders(self, flow: mitmproxy.http.HTTPFlow):
        """
            HTTP response headers were successfully read. At this point, the body
            is empty.
        """
        '''读取响应头内容'''

    def response(self, flow: mitmproxy.http.HTTPFlow):
        """
            The full HTTP response has been read.
        """
        # response_header = eval(dict(flow.response.headers)['response_header'])
        # # '''解码图片'''
        # # if flow.response.headers['Content-Type'].startswith('image/'):
        # #     with open(r'C:\Users\xh\proxy_yct\csdn-kf.png', 'wb') as f:
        # #         f.write(flow.response.content)
        # connect = filter_info['http_connect']
        # data_dict = {}
        # for i in connect:
        #    if i in flow.request.host:
        #        data_dict = self.yct_dealdatabag(flow)
        #        break
        #    else:
        data_dict = self.other_dealdatabag(flow)
        #        break
        pickled = pickle.dumps(data_dict)
        data_str = str(pickled)

        self.run_celery(data_str)

    def other_dealdatabag(self,flow):
        data_bag = {}
        # data_bag['client_address'] = flow.client_conn.address
        data_bag['request'] = flow.request
        data_bag['time_circle'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        data_bag['web_name'] = flow.request.host
        # data_bag['refer']=flow.request.headers.get('Referer','')
        data_bag['to_server'] = flow.request.url
        data_bag['response'] = flow.response
        return data_bag

    def yct_dealdatabag(self,flow):
        data_bag = {}
        # data_bag['client_address'] = flow.client_conn.address
        data_bag['request'] = flow.request
        data_bag['time_circle'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        data_bag['web_name'] = 'yct'
        # data_bag['refer']=flow.request.headers.get('Referer','')
        data_bag['to_server'] = flow.request.url
        data_bag['response'] = flow.response
        # print(data_bag)
        return data_bag


    def run_celery(self,data_str):
        #这个地方调用任务to_product
        handle_data(data_str)
        # folder=open(r'D:\data_bag_pickle\{}.pkl'.format(time.time()),mode='wb')
        # pickle.dump(data_bag,folder)
        # folder.close()

        # print(res)


    def error(self, flow: mitmproxy.http.HTTPFlow):
        """
            An HTTP error has occurred, e.g. invalid server responses, or
            interrupted connections. This is distinct from a valid server HTTP
            error response, which is simply a response with an HTTP error code.
        """

    # TCP lifecycle
    def tcp_start(self, flow: mitmproxy.tcp.TCPFlow):
        """
            A TCP connection has started.
        """

    def tcp_message(self, flow: mitmproxy.tcp.TCPFlow):
        """
            A TCP connection has received a message. The most recent message
            will be flow.messages[-1]. The message is user-modifiable.
        """

    def tcp_error(self, flow: mitmproxy.tcp.TCPFlow):
        """
            A TCP error has occurred.
        """

    def tcp_end(self, flow: mitmproxy.tcp.TCPFlow):
        """
            A TCP connection has ended.
        """

    # Websocket lifecycle
    def websocket_handshake(self, flow: mitmproxy.http.HTTPFlow):
        """
            Called when a client wants to establish a WebSocket connection. The
            WebSocket-specific headers can be manipulated to alter the
            handshake. The flow object is guaranteed to have a non-None request
            attribute.
        """

    def websocket_start(self, flow: mitmproxy.websocket.WebSocketFlow):
        """
            A websocket connection has commenced.
        """

    def websocket_message(self, flow: mitmproxy.websocket.WebSocketFlow):
        """
            Called when a WebSocket message is received from the client or
            server. The most recent message will be flow.messages[-1]. The
            message is user-modifiable. Currently there are two types of
            messages, corresponding to the BINARY and TEXT frame types.
        """

    def websocket_error(self, flow: mitmproxy.websocket.WebSocketFlow):
        """
            A websocket connection has had an error.
        """

    def websocket_end(self, flow: mitmproxy.websocket.WebSocketFlow):
        """
            A websocket connection has ended.
        """

    # Network lifecycle
    def clientconnect(self, layer: mitmproxy.proxy.protocol.Layer):
        """
            A client has connected to mitmproxy. Note that a connection can
            correspond to multiple HTTP requests.
        """

    def clientdisconnect(self, layer: mitmproxy.proxy.protocol.Layer):
        """
            A client has disconnected from mitmproxy.
        """

    def serverconnect(self, conn: mitmproxy.connections.ServerConnection):
        """
            Mitmproxy has connected to a server. Note that a connection can
            correspond to multiple requests.
        """

    def serverdisconnect(self, conn: mitmproxy.connections.ServerConnection):
        """
            Mitmproxy has disconnected from a server.
        """

    def next_layer(self, layer: mitmproxy.proxy.protocol.Layer):
        """
            Network layers are being switched. You may change which layer will
            be used by returning a new layer object from this event.
        """

    # General lifecycle
    def configure(self, updated: typing.Set[str]):
        """
            Called when configuration changes. The updated argument is a
            set-like object containing the keys of all changed options. This
            event is called during startup with all options in the updated set.
        """

    def done(self):
        """
            Called when the addon shuts down, either by being removed from
            the mitmproxy instance, or when mitmproxy itself shuts down. On
            shutdown, this event is called after the event loop is
            terminated, guaranteeing that it will be the final event an addon
            sees. Note that log handlers are shut down at this point, so
            calls to log functions will produce no output.
        """

    def load(self, entry: mitmproxy.addonmanager.Loader):
        """
            Called when an addon is first loaded. This event receives a Loader
            object, which contains methods for adding options and commands. This
            method is where the addon configures itself.
        """

    def log(self, entry: mitmproxy.log.LogEntry):
        """
            Called whenever a new log entry is created through the mitmproxy
            context. Be careful not to log from this event, which will cause an
            infinite loop!
        """

    def running(self):
        """
            Called when the proxy is completely up and running. At this point,
            you can expect the proxy to be bound to a port, and all addons to be
            loaded.
        """

    def update(self, flows: typing.Sequence[mitmproxy.flow.Flow]):
        """
            Update is called when one or more flow objects have been modified,
            usually from a different addon.
        """

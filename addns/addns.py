# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.

import os
import requests
import re
import argparse
import time
from log import *

from alibabacloud_alidns20150109.client import Client as Alidns20150109Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_alidns20150109 import models as alidns_20150109_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_console.client import Client as ConsoleClient
from alibabacloud_tea_util.client import Client as UtilClient


class AlirunUtilsWrap:
    def __init__(self, access_key_id, access_key_secret):
        self.services_list = [
            {"service_name": "origin", "service_url": r"https://httpbin.org/ip"},
            {"service_name": "origin", "service_url": r"http://httpbin.org/ip"},
            {"service_name": "ip", "service_url": r"https://ipinfo.io"},
            {"service_name": "ip", "service_url": r"http://ipinfo.io"},
            ]

        self.domain_type_list = ["A", "AAAA", "CNAME", "MX", "NS", "SRV", "TXT"]
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret
        self.aliyun_runtime = util_models.RuntimeOptions()
        self.aliyun_client = self.aliyun_create_client()

    def retrieve_public_ip(self):
        public_ip = None
        for item in self.services_list:
            try:
                response = requests.get(item['service_url'])

                # 解析响应的 JSON 数据
                data = response.json()

                # 获取公网 IP 地址
                if item['service_name']:
                    public_ip = data[item['service_name']]
                else:
                    public_ip = str(response)

                # print(public_ip)
                return public_ip
            except Exception as e:
                print(e)
                continue

    def aliyun_create_client(self) -> Alidns20150109Client:
        """
        使用AK&SK初始化账号Client
        @param access_key_id:
        @param access_key_secret:
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config(
            # 必填，您的 AccessKey ID,
            access_key_id = self.access_key_id,
            # 必填，您的 AccessKey Secret,
            access_key_secret = self.access_key_secret
        )
        # Endpoint 请参考 https://api.aliyun.com/product/Alidns
        config.endpoint = f'alidns.cn-hangzhou.aliyuncs.com'
        return Alidns20150109Client(config)

    def aliyun_get_domain_records(self, domain):
        domain_list_request = alidns_20150109_models.DescribeDomainRecordsRequest(domain_name=domain, lang="en")
        try:
            resp = self.aliyun_client.describe_domain_records_with_options(domain_list_request, self.aliyun_runtime)
            # print(resp.body.domain_records)
            return resp.body.domain_records
        except Exception as error:
            print(error)

    def aliyun_add_domain_record(self, domain, sub_domain, record_type, value):
        """
        添加解析记录
        :param domain: 域名
        :param sub_domain: 子域名
        :param record_type: 解析类型
        :param value: 解析值
        :return:
        """
        record_request = alidns_20150109_models.AddDomainRecordRequest(
            # 必填，创建解析记录的域名
            domain_name=domain,
            # 必填，解析记录的类型
            record_type=record_type,
            # rr
            rr=sub_domain,
            # value，记录值
            value=value)

        try:
            self.aliyun_client.add_domain_record_with_options(record_request, self.aliyun_runtime)
        except Exception as error:
            print(error)

    def aliyun_update_domain_record(self, rr, record_id, record_type, value):
        """
        更新解析记录
        :param rr: 域名前缀
        :param record_id: 记录ID
        :param record_type: 解析类型
        :param value: 解析值
        :return:
        """
        record_request = alidns_20150109_models.UpdateDomainRecordRequest(
            # 必填，记录ID
            record_id=record_id,
            # record type(A, AAAAA, TXT)
            type=record_type,
            # rr, subdomain prefix
            rr = rr,
            # value，　记录值
            value = value)

        try:
            self.aliyun_client.update_domain_record_with_options(record_request, self.aliyun_runtime)
        except Exception as error:
            print(error)

    def aliyun_delete_domain_record(self, record_id):
        """
        删除解析记录
        :param record_id: 记录ID
        :return:
        """
        record_request = alidns_20150109_models.DeleteDomainRecordRequest(
            # 必填，记录ID
            record_id=record_id)

        try:
            self.aliyun_client.delete_domain_record_with_options(record_request, self.aliyun_runtime)
        except Exception as error:
            print(error)

    def aliyun_ddns_main(self, domain:str, type: str):
        public_ip = self.retrieve_public_ip()
        domain_re =re.compile("(\S*\.)*(\S+\.\S+)")
        adomain = domain_re.search(domain).groups()
        sdomain = adomain[0].strip(".")
        mdomain = adomain[1]

        records = self.aliyun_get_domain_records(domain = mdomain)
        domains = records.to_map()
        for domaini in domains['Record']:
            if domaini['RR'] == sdomain and domaini['Type'] == type:
                self.aliyun_update_domain_record(sdomain, domaini['RecordId'], record_type=type, value=public_ip)
                log(INFO, "Update {} with {} done".format(domain, public_ip))
                break

if __name__ == "__main__":
    parse = argparse.ArgumentParser(description="Start sniffer with cli, target(openwrt) configure file can be store to openwrt/wireless or use inner static file")
    # parse.add_argument("--conf", help="path to the config file", required=False, type=str)

    keyid = os.environ.get('ACCESS_KEY_ID')
    key = os.environ.get('ACCESS_KEY')
    domain = os.environ.get('DOMAIN')

    isneed = True
    if keyid and key and domain:
        isneed = False

    parse.add_argument("-i", "--accesskeyid", help="accesskey id from aliyun", required=isneed, type=str)
    parse.add_argument("-k", "--accesskey", help="accesskey from aliyun", required=isneed, type=str)
    parse.add_argument("-d", "--domain", help="the domain to update with", required=isneed, type=str)
    parse.add_argument("-t", "--timeout", help="the time duration in second to trigger renew", required=False, default=300, type=int)

    args = parse.parse_args()

    if not args.accesskeyid or not args.accesskey or not args.domain:
        if not keyid or not key or not domain:
            log(ERROR, "Please provide accesskeyid and accesskey and domain")
            sys.exit()
        else:
            args.domain = domain
            args.accesskey = key
            args.accesskeyid = keyid

    userinfo = {}

    print(args)

    userinfo["domain"] = args.domain
    userinfo["keyid"] = args.accesskeyid
    userinfo["key"] = args.accesskey
    userinfo["duration"] = args.timeout

    # update_rr = "testdynamic"
    # update_rr_type = "A"
    # aliyun = AlirunUtilsWrap("LTAI5tBDViMBvzC62NbhYRzu", "bAOS1feSOxnGApNAMsB3HtT4mgRJOR")
    # aliyun.aliyun_ddns_main("testdynamic.whyfi.top", update_rr_type)
    while True:
        aliyun = AlirunUtilsWrap(userinfo["keyid"], userinfo["key"])
        aliyun.aliyun_ddns_main(userinfo["domain"], "A")
        time.sleep(userinfo["duration"])

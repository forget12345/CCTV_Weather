# -*- coding:UTF-8 -*-i
import urllib.request
import urllib.parse
import ssl
import json
import re

class get_info_cctv(object):
    """docstring for get_info_cctv"""
    def __init__(self, searchTime):
        #pack data
        self.searchTime = searchTime
        self.search='晚间天气预报'+searchTime
        

    # pack get data
    def pack_data_for_search(self):
        data=dict()
        data['page']='1'
        data['qtext']=self.search
        data['sort']='relevance'
        data['pageSize']='20'
        data['type']='video'
        data['vtime']='-1'
        data['datepid']='1'
        data['channel']='不限'
        data['pageflag']='0'
        data['qtext_str']=self.search
        # print(data)
        url_para = urllib.parse.urlencode(data)
        url = 'https://search.cctv.com/ifsearch.php'
        return url + '?' + url_para

    def pack_data_for_mp4(self,pid):
        # http://vdn.apps.cntv.cn/api/getHttpVideoInfo.do?
        data=dict()
        data['pid']=pid
        data['tz']='-8'
        data['from']='000news'
        data['url']='url'
        data['idl']='32'
        data['idlr']='32'
        data['modifyed']='false'

        url_para = urllib.parse.urlencode(data)
        url = 'http://vdn.apps.cntv.cn/api/getHttpVideoInfo.do'
        return url + '?' + url_para
    #get api from cctv_for_search
    def getAction(self,url,flag='false'):
        # url=self.pack_data_for_search()
        context = ssl._create_unverified_context()
        with urllib.request.urlopen(url, context=context) as response:
            self.deal_data(response,flag)
        
    #deal data
    def deal_data(self,response,flag='false'):
        html = response.read()
            # print(response.code)#200是正常响应
        if response.code==200:
            # print(respose.content)  #返回字节信息
            data=json.loads(html) #返回文本内容
            if flag=='true':
                print(data['video'])
                pass
            else:
                titleName=data['list'][0]['all_title']
                titleName=eval("u"+"\'"+titleName+"\'")
                regex = r".*晚间天气预报.*"+ self.searchTime
                matches = re.match(regex, titleName)
                if matches==None:
                    print("is null")
                    pass
                else:
                    url=data['list'][0]['imglink']
                    self.get_mp4_path(url)
                pass
        pass

    def get_mp4_path(self,url):
            pid=re.findall(r".*/(.*)-", url)
            url=self.pack_data_for_mp4(pid[0])
            print(url)
            self.getAction(url,'true')
    def down():
        # http://vdn.apps.cntv.cn/api/getHttpVideoInfo.do?pid=a7bb08a5f8b94c8fa764982d7d8fb6a4&tz=-8&from=000news&url=url&idl=32&idlr=32&modifyed=false
        pass

    def main(self):
        self.getAction(self.pack_data_for_search())

get=get_info_cctv('20170701')
get.main();  
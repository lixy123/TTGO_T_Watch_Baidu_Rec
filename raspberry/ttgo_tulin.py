# -*- coding: utf-8-*-
import requests
import json,sys

#注意：
#在http://www.turingapi.com/ 上注册获取账号，写入下面的变量中，且必须身份证认证后才可用
tuling_key = "自已注册获取!!!"


def tulin_chat(texts):
    """
    使用图灵机器人聊天

    Arguments:
    texts -- user input, typically speech, to be parsed by a module
    """
    msg = ''.join(texts)
    try:
        url = "http://www.tuling123.com/openapi/api"
        userid = "tulin2018_esp32"
        body = {'key': tuling_key, 'info': msg, 'userid': userid}
        r = requests.post(url, data=body)
        respond = json.loads(r.text)
        result = ''
        if respond['code'] == 100000:
            result = respond['text'].replace('<br>', '  ')
            result = result.replace(u'\xa0', u' ')
        elif respond['code'] == 200000:
            result = respond['url']
        elif respond['code'] == 302000:
            for k in respond['list']:
                result = result + u"【" + k['source'] + u"】 " +\
                    k['article'] + "\t" + k['detailurl'] + "\n"
        else:
            result = respond['text'].replace('<br>', '  ')
            result = result.replace(u'\xa0', u' ')
            result = result.decode('utf-8')
        max_length = 100
        return(result)        
    except Exception as e:
        print(e)
        return("")
        
reload(sys)
sys.setdefaultencoding('utf8')  
#ret=tulin_chat("今天星期几")
#print(ret)
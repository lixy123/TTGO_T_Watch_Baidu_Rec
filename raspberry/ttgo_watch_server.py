# -*- coding: utf-8 -*-
import web,sys,json
import time
from datetime import datetime
import logging,os

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import textwrap
from io import BytesIO 
import ttgo_tulin

logOutFilename='/myram/web_baidu.txt'   

#运行:  python ttgo_watch_server.py 1990
#服务为家用，假设一次只一个服务，未考虑多并发情况
urls = (
    '/(.*)', 'hello'
)

reload(sys)
sys.setdefaultencoding('utf8')  

# choose between DEBUG (log every information) or warning (change of state) or CRITICAL (only error)
#logLevel=logging.DEBUG
logLevel=logging.INFO
#logLevel=logging.CRITICAL


FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=FORMAT,filename=logOutFilename,level=logLevel)

print("wait sleep")
#确保开机后网络连接
time.sleep(1)
app = web.application(urls, globals())
print("server start")
 
#http://192.168.1.20:1990/method=token
#http://192.168.1.20:1990/method=text_mp3&txt=今天天气不错
#http://192.168.1.20:1990/method=mp3_text
#http://192.168.1.22:1990/method=text_wav&txt=%E4%BD%A0%E5%A5%BD
#http://192.168.1.22:1990/method=info&txt=nhhao

last_get_tulin= time.time()-20
last_get_tulin_delay=30

class ImgText:
  font = ImageFont.truetype("/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",size=36)
  def __init__(self, text):
    # 预设宽度 可以修改成你需要的图片宽度
    
    # 要比画布略小此 -20
    self.width = 200  
    # 文本
    self.text = text
    # 段落 , 行数, 行高
    self.duanluo, self.note_height, self.line_height = self.split_text()
    
  def get_duanluo(self, text):
    txt = Image.new('RGB', (self.width, 120), (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt)
    # 所有文字的段落
    duanluo = ""
    # 宽度总和
    sum_width = 0
    # 几行
    line_count = 1
    # 行高
    line_height = 0
    for char in text:
      width, height = draw.textsize(char, ImgText.font)
      sum_width += width
      if sum_width > self.width: # 超过预设宽度就修改段落 以及当前行数
        line_count += 1
        sum_width = 0
        duanluo += '\n'
      duanluo += char
      line_height = max(height, line_height)
    if not duanluo.endswith('\n'):
      duanluo += '\n'
    return duanluo, line_height, line_count
    
  def split_text(self):
    # 按规定宽度分组
    max_line_height, total_lines = 0, 0
    allText = []
    for text in self.text.split('\n'):
      duanluo, line_height, line_count = self.get_duanluo(text)
      max_line_height = max(line_height, max_line_height)
      total_lines += line_count
      allText.append((duanluo, line_count))
    line_height = max_line_height
    total_height = total_lines * line_height
    return allText, total_height, line_height
    
  def draw_text(self):
    """
    绘图以及文字
    :return:
    """

    img1 = Image.new('RGB', (240, 120), (0, 0, 0))
    draw1 = ImageDraw.Draw(img1)
    # 左上角开始
    x, y = 0, 0
    for duanluo, line_count in self.duanluo:
      draw1.text((x, y), duanluo, fill=(255, 255, 255), font=ImgText.font)
      y += self.line_height * line_count
    #img1 = img1.convert("L")   #8位像素，表示黑和白 watch不能显示
    #img1 = img1.convert("P")   #8位彩色图像 会异常！
    #img1.save("/myram/t_watch.jpg",quality=60) #默认值为75    
    bf = BytesIO()
    img1.save(bf,'jpeg',quality=60) 
    #返回图片数据流    
    return bf.getvalue()
    
class hello:
    def GET(self, name):
        global last_get_tulin
        ret=""
        if name: 
            #print name
            params=name.split('&');
            method=''
            txt=''
            for p in params:
                if p.split('=')[0]=='method':
                    method=p.split('=')[1]
                if p.split('=')[0]=='txt':
                    txt=p.split('=')[1]  
        print(">"+ method)
        #启动上线记录
        if (method=="online"):
            txt_input=txt
            print(txt_input)        
            #web.header('Content-type','text/html')
            #web.header('Transfer-Encoding','application/octet-stream') 
            #retMsg=baidu_sound_rec.esp32_baidu_token()
            #以下两句是设置返回数据格式，避免解析返回数据麻烦，详见
            #https://blog.csdn.net/luchunpeng/article/details/53581163
            retMsg="success"
            web.header('Content-Type', 'application/octet-stream')            
            web.header('Content-Length', len(retMsg)) 
            logging.info('online %s %s',txt_input,retMsg)              
            return retMsg           

        #BytesIO 对象返回图片偶有图片上传数据不全问题
        if (method=="text_jpg"):
            txt_input=txt
            print(txt_input)
            n_txt = ImgText(txt_input)
            fn_data=n_txt.draw_text()  
            web.header('Content-Type', 'application/octet-stream')
            web.header('Content-Length', len(fn_data)) 
            print("len=",len(fn_data))
            logging.info('text_jpg %s',txt_input)     
            print("图片返回:")            
            return fn_data   
        #图灵交互，返回文本
        if (method=="tulin_txt"):
            txt_input=txt
            #txt_input="1+1等于几"
            #print(txt_input)            
            txt_tulin=ttgo_tulin.tulin_chat(txt_input)  
            #print(txt_tulin)        
            web.header('Content-Type', 'application/octet-stream')
            #注意：如果数字与文字混合，可能len(txt_baidu)*3会有问题
            #图灵返回数据要先转换成utf-8，<type 'str'> 才能得到最终的字节数
            web.header('Content-Length',len(txt_tulin.encode('utf8'))) 
            #print(len(txt_tulin.encode('utf8')))
            logging.info('tulin_txt %s',txt_tulin)             
            return txt_tulin 
        #记录历史识别出的声,mqtt通知其它设备
        if (method=="info"):
            txt_input=txt
            print(datetime.now().strftime('%m-%d %H:%M')+ " " + txt_input)            
            logging.info('info %s',txt_input) 
            show_txt=txt_input          
            #print("时间间隔:",int(time.time()-last_get_tulin))   
            #logging.info(  "时间间隔:"+ str(int(time.time()-last_get_tulin)))   
            #将图灵生成的对话转发到其它mqtt服务（例如扬声器)            
            if  time.time()-last_get_tulin>last_get_tulin_delay:
                mqtt_out="mosquitto_pub -t  \"speaker\"  -h 127.0.0.1 -m \"tulin:"+ show_txt+"\""
                os.system(mqtt_out)
                last_get_tulin= time.time()               
            
            #开灯关灯控制命令
            if "开灯" in txt_input:
                os.system("mosquitto_pub -t \"/sonoff20/gpio/12\"  -h 127.0.0.1 -m \"1\"")
            elif "关灯" in txt_input:
                os.system("mosquitto_pub -t \"/sonoff20/gpio/12\"  -h 127.0.0.1 -m \"0\"")

            '''
            ws2812彩灯控制显示颜色
            elif "红色" in txt_input:
                os.system("curl 'http://192.168.1.50/setColor?rVal=255&gVal=0&bVal=0'")               
            elif "橙色" in txt_input:
                os.system("curl 'http://192.168.1.50/setColor?rVal=255&gVal=128&bVal=10'")
            elif "黄色" in txt_input:
                os.system("curl 'http://192.168.1.50/setColor?rVal=255&gVal=255&bVal=0'")
            elif "绿色" in txt_input:
                os.system("curl 'http://192.168.1.50/setColor?rVal=0&gVal=255&bVal=0'")
            elif "青色" in txt_input:
                os.system("curl 'http://192.168.1.50/setColor?rVal=0&gVal=255&bVal=255'")
            elif "蓝色" in txt_input:
                os.system("curl 'http://192.168.1.50/setColor?rVal=0&gVal=0&bVal=255'")
            elif "紫色" in txt_input:
                os.system("curl 'http://192.168.1.50/setColor?rVal=128&gVal=0&bVal=128'")
            elif "白色" in txt_input:
                os.system("curl 'http://192.168.1.50/setColor?rVal=255&gVal=255&bVal=255'")
            elif "黑色" in txt_input:
                os.system("curl 'http://192.168.1.50/setColor?rVal=0&gVal=0&bVal=0'")  
            '''                
            return "success"   
        return ret
    #post方式提交表单,
    def POST(self, name):
        return ""

#不要去除main
if __name__ == "__main__":
    app.run()

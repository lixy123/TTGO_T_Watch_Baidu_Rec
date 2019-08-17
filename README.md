

   
一.程序功能： 

1.声音监听器。声音监听器。监听周围的声音，并识别成文字。识别的文字经过配置可以转发到其它设备，如树莓派，分发给其它设备联动。
             每次识别最长10秒录音并识别。平均一次录音文字识别时间1-10秒不等
             
2.硬件：    TTGO_T_Watch 主板自带有8M PSRAM, 扩展板有多种，有一种扩展板集成了INMP441 I2S 麦克风录入芯片, 可以处理语音.

         源码硬件资料: https:github.com/LilyGO/TTGO-T-Watch         
         介绍指南:    https:t-watch-document-en.readthedocs.io/en/latest/index.html         
         玩家介绍:   https:www.instructables.com/id/TTGO-T-Watch/


 INMP441与ESP32接线定义见I2S.h
 
 SCK IO15 
 
 WS  IO13 
 
 SD  IO14 
 
 L/R GND 

二.ESP32编译环境:

    1.Arduino 1.8.9    
    2.扩展板引用地址配置成: https:dl.espressif.com/dl/package_esp32_dev_index.json    
    3.安装： 安装esp32的官方开发包 esp32 by Espressif Systems 版本 1.03-rc1    
    4.开发板选择: TTGO T-WATCH, PSRAM选择Enabled
      esp32只有512K内存，保存不了20秒的声音文件，在声音识别前必须存到一处地方，最合适的是用PSRAM.
      SPIFFS写入速度不够快, 达不到边录音边存效果，失音严重
      10倍速sd卡速度虽然可以达到，但检测静音期间SD卡需要反复写入，容易写废      
    5.Arduino选择正确端口号后开始烧写固件
    
    已提供编译好的固件：           
    1.下载固件:
    https://github.com/lixy123/TTGO_T_Watch_Baidu_Rec/releases
    2.解压后共4个文件，readme中有烧写软件的下载地址，下载执行后按图设置好参数，特别是4个文件的烧写地址
    3.点击START
 
三.树莓派服务端python代码

1.用于收集esp32识别到的文字和声音(识别到文字才会上传声音).
也可以不配置服务器地址，但如果配置后，上报识别出文字可经由树莓派当作指令转发给其它设备联动.        
2. 安装：把raspberry目录中的两个py代码拷入树莓派
3. 运行：python ttgo_watch_server.py 1990 
4. TTGO_T_Watch 配置地址指向此树莓派的IP,建议树莓派设置固定IP

四 .使用说明：

  1.配置: TTGO T-WATCH 开机运行，首次运行时初始化内置参数,自动进入路由器模式,创建一个ESP32SETUP的路由器，电脑连接,
    输入 http://192.168.4.1 进行配置
   
    A.esp32连接的路由器和密码    
    B.百度语音的账号,和校验码
      baidu_key, baidu_secert 这两个参数需要注册百度语音服务,在如下网址获取 http://yuyin.baidu.com
      个人免费账号每天调用次数不限，但并发识别数只有2个，所以此账号建议只有一机一号，不适合共享使用。      
    C.图灵服务器对话配置
      配置了会对识别的文字与图灵对话, 不填图灵的账号就没有这功能      
      tulin_key: 一个账号字串      
      http://www.turingapi.com/ 上注册获取账号，账号必须身份证认证后才可用      
      个人免费账号每天调用次数1天100次,基本够用      
    D.树莓派上报配置
      配置了上报识别的文字和声音树莓派或其它中心服务,可处理关灯,开灯等指令, 不填服务器地址就没有这功能      
      参考配置:
           report_address: 192.168.1.20
           report_url: http://192.168.1.20:1990/method=info&txt=           
       使用前在树莓派上先运行服务端程序       
    E.其它音量监测参数: 默认是在家里安静环境下,如果周围较吵,需要将值调高
    
  2.运行：上电即运行

   <img src= 'https://github.com/lixy123/TTGO_T_Watch_Baidu_Rec/blob/master/IMG_20190811_1359341.jpg' />

演示视频地址
   https://github.com/lixy123/TTGO_T_Watch_Baidu_Rec/blob/master/VID_20190811.avi

五.软件代码原理:

  1.esp32上电后实时读取I2S声音信号，检测到周围声强是否达到指定音量，达到后立即进入录音模式  
  2.如发现3秒内静音录音停止，否则一直录音，直到10秒后停止录音  
  3.将i2s采集到的wav原始声音数据按http协议用前面配置的百度账号传给百度服务,进行语音转文字  
  4.如果百度识别出文字，将文字http方式传给服务器，现在用的是树莓派  
  声源在1-4米内识别效果都不错，再远了识别率会低.


六.其它技巧

  1.wav采集的数字声音有点像水波振动，以数字0不基线上下跳动. 静音时采集到的数值为0.  
  2.程序会预存2秒的声音，这2秒不仅用于检测声强，也会用于文字识别。这样对于监听二个字的短语不会丢失声音数据.
  
七.工作用电:

  5v 70ma电流   
  TTGO_T_Watch 自带的180 mAh电池理论上可以工作2小时. 



   
一.程序功能： 声音监听器。监听周围的声音，并识别成文字。
          识别的文字转发到其它设备，如树莓派，每段录音最长10秒,平均一段录音的文字识别时间3-25秒，取决于网络速度

硬件：    TTGO_T_Watch 主板自带有8M PSRAM, 扩展板有多种，有一种扩展板集成了INMP441 I2S 麦克风录入芯片, 可以处理语音.

         源码硬件资料: https:github.com/LilyGO/TTGO-T-Watch
         
         介绍指南:    https:t-watch-document-en.readthedocs.io/en/latest/index.html
         
         玩家介绍:   https:www.instructables.com/id/TTGO-T-Watch/
         
 INMP441与ESP32接线定义见I2S.h (TTGO_T_Watch)
 
 SCK IO15
 
 WS  IO13
 
 SD  IO14
 
 L/R GND
 

二.ESP32编译环境:

    1.Arduino 1.8.9
    
    2.扩展板引用地址配置成: https:dl.espressif.com/dl/package_esp32_dev_index.json
    
    3.安装： 安装esp32的官方开发包 esp32 by Espressif Systems 版本 1.03-rc1
    
    4.开发板选择: TTGO T-WATCH, PSRAM选择Enabled
      esp32只有512K内存，存不了20秒的声音文件，在声音识别前必须存到一处地方，最合适的是用PSRAM.
      SPIFFS写入速度不够快, 达不到边录音边存效果，失音严重
      10倍速sd卡也可以，但为了达到声音检测，SD卡需要反复写入，容易写废
      
    5.Arduino选好开发板，设置完PSRAM,端口号后就可以连接esp32烧写固件了.
 
三.树莓派服务端

  使用树莓派原因
  
  1.esp32没找到显示汉字的方案，所以供助树莓派将文字转成图片回显用
  
  2.识别出文字后,简单的控制电灯开关，控制扬声器像机器人一样对话可以做到的。但如果想要更进一步，把识别的文字传给总机做处理更好。
    但esp32独立与百度交互识别文字的功能保留了下来.
    
  3. 安装：把raspberry目录中的两个py代码拷入树莓派
  
  4. 配置：ttgo_tulin.py   需要在http:www.turingapi.com/ 上注册获取账号，写入变量tuling_key，账号必须身份证认证后才可用
  
  5. 运行：python ttgo_watch_server.py 1990 
  
  6. 家里的树莓派IP固定成了: 192.168.1.20      


四 .使用说明：

  1.配置: TTGO T-WATCH 开机运行，首次运行时初始化内置参数,自动进入路由器模式,创建一个ESP32SETUP的路由器，电脑连接,输入http://192.168.4.1进行配置
   
    A.主要配置连接的路由器和密码
    
    B.百度语音的账号,和校验码
      baidu_key, baidu_secert 这两个参数需要注册百度语音服务,在如下网址获取 http://yuyin.baidu.com
      个人免费账号每天调用次数不限，但并发识别数只有2个，所以此账号建议只有一机一号，不适合共享使用，升级账号并发数会增加，但得花钱。
      
    C.与树莓派交互的IP
    
    D.其它还有音量监测参数等
    
  2.运行：上电即运行

   <img src= 'https://github.com/lixy123/TTGO_T_Watch_Baidu_Rec/blob/master/IMG_20190811_135934.jpg' />

演示视频地址
   https://github.com/lixy123/TTGO_T_Watch_Baidu_Rec/blob/master/VID_20190811.avi

五.软件代码原理:

  1.esp32上电后实时读取I2S声音信号，检测到周围声强是否达到指定音量，达到后立即进入录音模式
  
  2.如发现3秒内静音录音停止，否则一直录音，直到10秒后停止录音，
  
  3.将i2s采集到的wav原始声音数据按http协议用前面配置的百度账号传给百度服务,进行语音转文字
  
  4.如果百度识别出文字，将文字http方式传给服务器，现在用的是树莓派
  
  声源在1-4米内识别效果都不错，再远了识别率会低.



六.其它技巧

  1.wav采集的数字声音有点像水波振动，以数字0不基线上下跳动. 静音时采集到的数值为0.
  
  2.程序会预存2秒的声音，这2秒不仅用于检测声强，也会用于文字识别。这样对于监听二个字的短语不会丢失声音数据.
  


七.工作用电:

  5v 70ma电流 
  
  TTGO_T_Watch 自带的180 mAh电池理论上可以工作2小时

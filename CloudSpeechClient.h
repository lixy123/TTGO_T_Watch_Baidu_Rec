#define SHOW_DEBUG
#include "Wav.h"
#include "SPIFFS.h"
#include <base64.h>
#include <ArduinoJson.h>
//https://blog.csdn.net/lgj123xj/article/details/78626160
#include "urlencode.h"
#include <WiFi.h>

class CloudSpeechClient {
    WiFiClient client;
    //WiFiClient client_led;
    String Findkey(String line);
    const char * token_url = "https://openapi.baidu.com/oauth/2.0/token";
    const char * getvoice_url  = "http://tsn.baidu.com/text2audio";
    const char * upvoice_url = "http://vop.baidu.com/server_api";
    const char * cu_id = "cu_id";
    char *   textfile = "/text.wav";
    
 //树莓派 启动：web_baidu.py 
 //const char * upvoice_url_host_www = "192.168.1.20:1990";
 //树莓派 启动：sock_fileServer.py 接收文件用


    
    String baidu_Token = "";
    uint32_t PrintHttpBody2();
    String Find_baidutext(String line);
    bool savemp3(long file_size);
  public:  
    uint8_t buff[1024];
    uint8_t buff_base64[2048];
    CloudSpeechClient(int sec);
    ~CloudSpeechClient();

 const char *   recordfile = "record";
 const char * jpgfile="/watch.jpg";  //临时生成图片文件，用于显示到 watch上
 
    const int headerSize = 44;
    //这个psram版本就是提前分配了一个内存区,专用于存放声音数据,调用百度声音识别时不需要借助于SD卡做为交换.
    //wav文件头的44个字节, 为base64 处理需要, 必须是6的倍数,  多加点数据
    byte * wav_head;

    //2秒就够了
    //定义保存pre_sec秒音频的空间，用于检测非静音阶段，会用于百度识别
    //检测是否有动静阶段用 ,
    int pre_sec=2;
    uint32_t pre_maxnum_sound_buff;
    byte* pre_sound_buff;
    uint32_t pre_sound_buf_p;
    //数据存入缓存
    void pre_push_sound_buff(byte * src_buff, uint32_t len);

    //清空下2秒缓存
    void zero_pre_push_sound_buff();

    //本地录音文件上传
    bool uploadfile(String ftp_host, int ftp_port, String fn);
    //语音wav转文本
    String getVoiceText_berry(String report_address, int port, String txt, String fn);
    
    //定义保存20秒音频的空间，用于录音阶段存储声音， 会用于百度识别
    //约 640kB 音频信号就不用在TF卡上交换了
    const uint32_t maxnum_bodysound__buff = 32000 * 12;
    byte* sound_bodybuff;
    uint32_t sound_bodybuff_p;
    //数据存入缓存
    void push_bodybuff_buff(byte * src_buff, uint32_t len);

    //返回口令字符串
    String getToken(String api_key, String api_secert);
    //文本转语音
    String getVoice(String audio_text);
    //语音转文本
    String getVoiceText();
    
    //文字转jpg （url含 文字)
    String get_jpg(String host, int port, String url);
    bool savejpg(long file_size);
    
    String posturl(String host, int port, String url);
  
};

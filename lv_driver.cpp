#include "lv_driver.h"

static TFT_eSPI *tft = nullptr;

Ticker lvTicker1; /* timer for interrupt handler */

Ticker lvTicker2;



static void ex_disp_flush(int32_t x1, int32_t y1, int32_t x2, int32_t y2, const lv_color_t *color_array)
{
  uint32_t size = (x2 - x1 + 1) * (y2 - y1 + 1) * 2;
  tft->setAddrWindow(x1, y1, x2, y2);
  tft->pushColors((uint8_t *)color_array, size);
  lv_flush_ready();
}




/* Interrupt driven periodic handler */
static void lv_tick_handler(void)
{
  lv_tick_inc(LVGL_TICK_PERIOD);
}


void display_init()
{
  tft = new TFT_eSPI(LV_HOR_RES, LV_VER_RES);
  tft->init();
  tft->setRotation(0);

  lv_init();

  /*初始化显示屏*/
  lv_disp_drv_t disp_drv;
  lv_disp_drv_init(&disp_drv);
  disp_drv.disp_flush = ex_disp_flush; /*Used in buffered mode (LV_VDB_SIZE != 0  in lv_conf.h)*/
  lv_disp_drv_register(&disp_drv);

   //让gui控件起作用 此句不可缺少！！！
  lvTicker1.attach_ms(LVGL_TICK_PERIOD, lv_tick_handler);

  //让gui控件起作用 此句不可缺少！！！
  lvTicker2.attach_ms(100, [] {
    lv_task_handler();
  });

  backlight_init();
  
//  int level = backlight_getLevel();
//  for (int level = 0; level < 255; level += 25) {
//    backlight_adjust(level);
//    delay(100);
//  }
  backlight_adjust(180);
}

void backlight_init(void)
{
  ledcAttachPin(TFT_BL, 1);
  ledcSetup(BACKLIGHT_CHANNEL, 12000, 8);
}


uint8_t backlight_getLevel()
{
  return ledcRead(BACKLIGHT_CHANNEL);
}

void backlight_adjust(uint8_t level)
{
  ledcWrite(BACKLIGHT_CHANNEL, level);
}

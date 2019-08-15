#include "board_def.h"
#include <TFT_eSPI.h>
#include <lvgl.h>

#include <Ticker.h>
#define BACKLIGHT_CHANNEL   ((uint8_t)1)

#define LVGL_TICK_PERIOD 20

void display_init();

void backlight_init(void);
uint8_t backlight_getLevel();
void backlight_adjust(uint8_t level);

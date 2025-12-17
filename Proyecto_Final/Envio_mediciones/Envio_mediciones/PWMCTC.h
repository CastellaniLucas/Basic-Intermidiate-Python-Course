#ifndef PWMCTC
#define PWMCTC
#include <avr/io.h>
#include <stdint.h>

void iniciar_Timer2_CTC(uint16_t prescaler, uint8_t ocr);

#endif

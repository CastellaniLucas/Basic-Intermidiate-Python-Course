#ifndef ADC5ext
#define ADC5ext
#include <avr/io.h>
#include <stdint.h>


void iniciar_ADC(void);
uint16_t leer_adc(void);

#endif
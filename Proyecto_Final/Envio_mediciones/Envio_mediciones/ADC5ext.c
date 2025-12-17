#include "ADC5ext.h"
#include <avr/io.h>
#include <stdint.h>

void iniciar_ADC(void){
	
	ADMUX = (1 << REFS0) | (5 << MUX0);  //Vcc interna como referencia

	DIDR0 |= (1 << ADC5D);

	// Habilitar ADC y prescaler 128 -> AD clock = 16MHz/128 = 125kHz
	ADCSRA = (1 << ADEN) | (1 << ADPS2) | (1 << ADPS1) | (1 << ADPS0);
}

uint16_t leer_adc(void){
	// Iniciar conversión (canal ya seleccionado)
	ADCSRA |= (1 << ADSC);
	
	while (ADCSRA & (1 << ADSC)); // esperar fin
	
	return ADC;
}

#include "PWM2.h"
#include <stdint.h>
#include <avr/io.h>
#define ICR1_TOP 15999
#define PWM_MAX ICR1_TOP

void iniciar_PWM (void){
	DDRB |= (1 << PB1);   // OC1A (PB1, pin 9) salida

	// Fast PWM, TOP = ICR1 (modo 14)
	TCCR1A = (1 << WGM11);
	TCCR1B = (1 << WGM13) | (1 << WGM12);

	// No-inverting mode en OC1A
	TCCR1A |= (1 << COM1A1);

	// TOP = 15999 ? periodo = 1 kHz
	ICR1 = ICR1_TOP;

	// Duty inicial 50%
	OCR1A = (ICR1_TOP + 1)/2;   // 50% de 16000 = 8000

	// Prescaler = 1
	TCCR1B |= (1 << CS10);
}
void actuador(float a){
	// a es valor en voltios (0..5). Escalamos a PWM [0..PWM_MAX]
	if (a < 0.0f) a = 0.0f;
	if (a > 5.0f) a = 5.0f;
	uint16_t pwm = (uint16_t)((a / 5.0) * (float)PWM_MAX);
	OCR1A = pwm;
}
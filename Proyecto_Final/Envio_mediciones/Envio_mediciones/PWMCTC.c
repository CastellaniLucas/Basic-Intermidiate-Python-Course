#include <avr/io.h>
#include <stdint.h>

void iniciar_Timer2_CTC(uint16_t prescaler, uint8_t ocr)
{
	// Modo CTC: WGM22:0 = 010
	TCCR2A = (1 << WGM21);
	TCCR2B = 0;  // WGM22 = 0

	// Limpio prescaler
	TCCR2B &= ~((1 << CS22) | (1 << CS21) | (1 << CS20));

	// Seteo el prescaler elegido
	switch (prescaler) {
		case 1:    TCCR2B |= (1 << CS20); break;
		case 8:    TCCR2B |= (1 << CS21); break;
		case 32:   TCCR2B |= (1 << CS21) | (1 << CS20); break;
		case 64:   TCCR2B |= (1 << CS22); break;
		case 128:  TCCR2B |= (1 << CS22) | (1 << CS20); break;
		case 256:  TCCR2B |= (1 << CS22) | (1 << CS21); break;
		case 1024: TCCR2B |= (1 << CS22) | (1 << CS21) | (1 << CS20); break;
		default:   TCCR2B |= (1 << CS22); break; // default = 64
	}

	// habilitar interrupción compare match A
	TIMSK2 |= (1 << OCIE2A);
		
	OCR2A = ocr;
}

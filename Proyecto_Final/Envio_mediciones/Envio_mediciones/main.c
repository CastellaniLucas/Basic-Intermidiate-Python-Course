#include <avr/io.h>
#include "ADC5ext.h"
#define F_CPU 16000000UL     // Frecuencia del microcontrolador  16 MHz
#include <util/delay.h>
#define BAUD 90000
#define MYUBRR F_CPU/16/BAUD-1
#include <stdint.h>
#include <avr/interrupt.h>
#include "ADC5ext.h"
#include "PWM2.h"
#include "PWMCTC.h"
#define ms 70
#define referencia1 1.0f
#define referencia2 4.0f
#define tiempo_cambio_ref 625                      // tiempo en el que cambio de ref1 a ref2
#define tiempo_perturbacion_salida_actuador 1250   // tiempo en el que se simula perturbacion en el actuador
// el tiempo se calcula como el numero que se escoge ultiplicado 16ms que es la velocidad de muestreo actual


//nombre = instante actual, nombre1 = instante n-1; nombre2 = instante n-2;
volatile float ref_p, ref_p1, ref_p2;
volatile float reff, ref1, ref2, refff;
volatile float actuadorr, actuadorr1, actuadorr2 ;
volatile float errorr, error1, error2;
volatile float medicion_planta;  // salida medida (V)
volatile int16_t count = 0;
volatile int8_t flag_ref = 0;    //flag para cambio de referencia
volatile int8_t flag_pert_a = 0; //flag perturbacion actuador

//flag para activar cuentas del controlador
volatile uint8_t sample_flag = 0;

void iniciar_uart(unsigned int ubrr) {
	// Configurar baudrate
	UBRR0H = (unsigned char)(ubrr >> 8);
	UBRR0L = (unsigned char)ubrr;
	// Habilitar transmisión
	UCSR0B = (1 << TXEN0);
	// Configurar frame: 8 bits de datos, 1 bit de stop
	UCSR0C = (1 << UCSZ01) | (1 << UCSZ00);
}

void transmitir_uart(unsigned char data) {
	// Esperar a que el buffer esté vacío
	while (!(UCSR0A & (1 << UDRE0)));
	// Cargar dato en el registro de transmisión
	UDR0 = data;
}

void enviar_unsigned_int(unsigned int value) {
	if (value > 1023) value = 1023; // limitar a 10 bits (el adc es de 10bits)

	// Lo enviamos en dos bytes (LSB primero, luego MSB)
	unsigned char lowByte = value & 0xFF;         // 8 bits bajos
	unsigned char highByte = (value >> 8) & 0x03; // solo 2 bits altos

	transmitir_uart(lowByte);
	transmitir_uart(highByte);
}

ISR(TIMER2_COMPA_vect)
{
	count++;
	if(count == tiempo_cambio_ref){
		flag_ref = 1 - flag_ref;
	}
	if(count == tiempo_perturbacion_salida_actuador){
		flag_pert_a = 1 - flag_pert_a;
		count = 0;
	}

	sample_flag = 1;
}

int main(void) {
	iniciar_uart(MYUBRR);
	iniciar_ADC();
	
	PRR = 0x00;   // enciende TODOS los periféricos
	//establece frecuencia de muestreo, actualmente 61Hz
	uint16_t prescaler = 1024;
	uint8_t ocr = 255;
	
	
	//INT_init();
	iniciar_ADC();
	iniciar_PWM();
	iniciar_Timer2_CTC(prescaler, ocr);
	
	// Inicializar estados en 0
	ref_p = ref_p1 = ref_p2 = 0.0;
	
	// modificar referencia de 0 a 5V
	refff = referencia1;
	
	reff = ref1 = ref2 = 0.0;
	actuadorr = actuadorr1 = actuadorr2 = 0.0;
	errorr = error1 = error2 = 0.0;

	sei(); // habilitar interrupciones
	while (1) {
		if (sample_flag) {
			sample_flag = 0;
			// hago todo lo del controlador aca
			if (flag_ref == 1)
			{
				//modificar a gusto para ver cambio hacia otra referencia
				refff = referencia2;
			}
			else
			{
				refff = referencia1;
			}
			
			// actualizo valores de referencia
			ref2 = ref1;
			ref1 = reff;
			reff = refff;
			
			//calculo la referencia filtrada
			
			ref_p2 = ref_p1;
			ref_p1 = ref_p;
			ref_p = 1.86241296757111f * ref_p1 - 0.86595932147822273f * ref_p2
			+ 0.293912463935067f * reff - 0.557492177183427f * ref1 + 0.267098893499521f * ref2;
			
			
			//saturacion de la referencia de 0 a 5V
			
			if(ref_p > 5.0){
				ref_p = 5.0;
			}
			else if (ref_p < 0.0){
				ref_p = 0.0;
			}
			
			
			// mido la salida
			medicion_planta = leer_adc();
			enviar_unsigned_int(medicion_planta);
			medicion_planta = (medicion_planta * 5.0 / 1023.0);

			
			//señal de error
			
			error2 = error1;
			error1 = errorr;
			errorr = ref_p - medicion_planta;
			
			//calculo señal de control
			
			actuadorr2 = actuadorr1;
			actuadorr1 = actuadorr;
			actuadorr = 1.7596 * actuadorr1 - 0.7596 * actuadorr2
			+ 2.264 * errorr - 4.217 * error1 + 1.961 * error2;
			
			
			// Limitación de actuador (0..5 V)
			if (actuadorr < 0.0) actuadorr = 0.0;
			if (actuadorr > 5.0) actuadorr = 5.0;
			
			
			// Aplicar al PWM
			if (flag_pert_a){
				//con este flag activado, entra perturbacion a la salida del actuador
				actuador(actuadorr + 0.5);
			}
			else{
				actuador(actuadorr);
			}
			
		}
	}

	return 0;
}
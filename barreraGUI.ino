/*
 * 
 *  -Se cambia la logica del programa para que la interfaz 
 *    manejen las secuencias
 *  + Los sensores no estan respondiendo
*/


/*  Tabla de conexion
   * Buzzer   2
   * 
   * SESORES EN VIAS  
   * sensor1  3
   * sensor2  4
   * 
   * SESOR EN BARRERA
   * sensor3  10
   * 
   * SEMAFORO
   * verde    5
   * amarillo 6
   * rojo     7
   * 
   * barrera  9
   * 
   * BOTON DE EMERGENCIA
   * btn      11
*/
#include <Ticker.h>

//  barrera
#include <Servo.h>
Servo barrera;

//  Sensores de vias
#define sensor1 3
#define sensor2 4

//  Sensor en barrera
#define sensor3 10

//  Boton de emergencia
#define btn     11
bool emergencia = false;

//  Salidas
//  Buzzer
#define BUZZER  2
bool estado_buzzer = LOW;
static  long  tiempo_buzzer = 0;

//  Luces
#define VERDE     5
#define AMARILLO  6
#define ROJO      7
bool estado_amarillo = false;
static  long  tiempo_amarillo = 0;

//  Variables 
bool ingresa  = false;

void fnSensor_vias(){
  if (!digitalRead(sensor1)){
    Serial.println("sensor1:1");
  }
  if (!digitalRead(sensor2)){
    Serial.println("sensor2:1");
  }
}
Ticker ticSensor_vias(fnSensor_vias, 500);

void setup() {
  Serial.begin(9600);
  delay(30);
  
  // Salidas
  pinMode(VERDE, OUTPUT);
  pinMode(AMARILLO, OUTPUT);
  pinMode(ROJO, OUTPUT);
  pinMode(BUZZER, OUTPUT);
  barrera.attach(9);
  
  //subirBarrera();

  ticSensor_vias.start();
}

void fnActuadores(String cad){
  int pos;
  String label, value;
  cad.trim();
  cad.toLowerCase();
  Serial.println(cad);

  pos = cad.indexOf(':');
  label = cad.substring(0, pos);
  value = cad.substring(pos + 1);

  //  Funciones
  if(label.equals("emergencia")){
    if(value.equals("1")){
      digitalWrite(VERDE, HIGH);
      digitalWrite(AMARILLO, HIGH);
      digitalWrite(ROJO, HIGH);
    }
  }

  if(label.equals("verde")){
    digitalWrite(VERDE, HIGH);
    digitalWrite(AMARILLO, LOW);
    digitalWrite(ROJO, LOW);
  }

}



void loop(){
  //ticSensor_vias.update();
  if(Serial.available()){
    fnActuadores(Serial.readString());
  }
}

/*
 * Se cambian los sensores de proximidad utrasonicos por sensores 
 * infrarrojos
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


//  barrera
#include <Servo.h>
Servo barrera;

//  Sensores de vias
#define sensor1 3
#define sensor2 4

//  Sensor en barrera
#define sensor3 10
bool persona = false;

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

void setup() {
  pinMode(BUZZER, OUTPUT);
  barrera.attach(9);
  
  subirBarrera();
  Serial.begin(9600);
}

void loop(){
//  Sensor en via - Ingreso del tren
    if(!digitalRead(sensor1)){
      if(!ingresa){
        ingresa = true;
        tiempo_amarillo = millis();
      }
    }
  
    //  Sensor en via - Partida del tren 
    if(!digitalRead(sensor2)){
      subirBarrera();
    }
  
    if(ingresa){
      long hora = millis();
      
      // Secuencia buzzer
      if(hora - tiempo_buzzer > 250){
        estado_buzzer = !estado_buzzer;
        tiempo_buzzer = hora;
        digitalWrite(BUZZER, estado_buzzer);
      }
  
      //  Secuencia de luces y barrera
      if(!estado_amarillo){
        estado_amarillo = true;
        digitalWrite(VERDE, LOW);
        digitalWrite(AMARILLO, HIGH);
        Serial.println("amarillo:1");
      }
      if(hora - tiempo_amarillo > 3000){
        digitalWrite(AMARILLO, LOW);
        digitalWrite(ROJO, HIGH);
        Serial.println("rojo:1");
        
        //  bajando barrera
        if(digitalRead(sensor3)){
          if(!persona){
            barrera.write(95);
            persona = true;
          }
        }
        else{
          persona = true;
        }
      }
      
      
    }
    else{
      subirBarrera();
    }
  }  
  
  void subirBarrera(){
  ingresa = false;
  estado_amarillo = false;
  persona = false;

  barrera.write(5);
  
  digitalWrite(BUZZER, LOW);
  
  digitalWrite(VERDE, HIGH);
  digitalWrite(AMARILLO, LOW);
  digitalWrite(ROJO, LOW);

  Serial.println("verde:1");
}

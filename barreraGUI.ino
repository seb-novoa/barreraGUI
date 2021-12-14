/*
 * Se cambian los sensores de proximidad utrasonicos por sensores 
 * infrarrojos
 * 
 *  -Se los mensaje para la comunicacion serial hacia la gui
 *  -Incorporar funcion lectora desde al gui
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
  
  
  Serial.begin(9600);
  delay(30);
  subirBarrera();
}

void loop() {
  //  Mostrar los estados de los sensores de vias
  Serial.print(digitalRead(btn));
  Serial.println("");

  //  Boton de emergencia
  if(digitalRead(btn)){
    delay(250);
    if(digitalRead(btn)){
      Serial.println("emergencia:" + emergencia);
      emergencia = !emergencia;
      if(!emergencia){
        subirBarrera();
      }
      else{
        digitalWrite(BUZZER, LOW);
      } 
    }
    delay(1000);
  }

  //  secuencia de emergencia
  if(emergencia){
    digitalWrite(ROJO, HIGH);
    digitalWrite(AMARILLO, HIGH);
    digitalWrite(VERDE, HIGH);
  }
  //  Secuencia de barrera
  else{
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
      }
      if(hora - tiempo_amarillo > 3000){
        digitalWrite(AMARILLO, LOW);
        digitalWrite(ROJO, HIGH);
        
        //  bajando barrera
        if(!digitalRead(sensor3)){
          barrera.write(95);
        }
      }
      
      
    }
    else{
      subirBarrera();
    }
  }
}

void subirBarrera(){
  ingresa = false;
  estado_amarillo = false;

  barrera.write(5);
  
  digitalWrite(BUZZER, LOW);
  
  digitalWrite(VERDE, HIGH);
  Serial.println("verde:1");
  
  digitalWrite(AMARILLO, LOW);
  Serial.println("amarillo:0");
  
  digitalWrite(ROJO, LOW);
  Serial.println("rojo:0");
}

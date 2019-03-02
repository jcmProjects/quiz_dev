/* Defines */
#define SS_PIN 4        /**< D2 SDA */
#define RST_PIN 5       /**< D1 RST */


/*
 * -----------------------------------------------------
 * -                   Digital Outputs                 -
 * ----------------------------------------------------- 
 */
const int Q0 = 16;      /**< D0 */
const int Q1 = 15;      /**< D8 */
const int Q2 = A0;      /**< A0 */
const int ledGreen = 2; /**< D4 */
const int ledRed = 0;   /**< D3 */

int StateQ0 = 0;        /**< State of input 0. */
int StateQ1 = 0;        /**< State of input 1. */
int StateQ2 = 0;        /**< State of input 2. */


/* 
 ! =====================================================
 ! =                        Setup                      =
 ! ===================================================== 
 */
/**
 * @brief Setup function. Runs once.
 */
void setup(void) {
    
      Serial.begin(9600);
    
      /* Set NodeMCU I/O's */
      pinMode(Q0, INPUT);
      pinMode(Q1, INPUT);
      pinMode(ledGreen, OUTPUT);
      pinMode(ledRed, OUTPUT);
  
}


/*
 ! =====================================================
 ! =                        Loop                       =
 ! ===================================================== 
 */
/**
 * @brief Loop function.
 */
void loop(void) {

}

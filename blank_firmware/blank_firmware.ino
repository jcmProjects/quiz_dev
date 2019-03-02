
/* Defines */
#define SS_PIN 4        /**< D2 SDA */
#define RST_PIN 5       /**< D1 RST */


/* -----------------------------------------------------
 * -                        DEBUG                      -
 * ----------------------------------------------------- */
bool debug = true;      /**< TRUE if debug is enabled. FALSE otherwise. */

 
/* -----------------------------------------------------
 * -                         RFID                      -
 * ----------------------------------------------------- */

/* -----------------------------------------------------
 * -                        Router                     -
 * ----------------------------------------------------- */
bool connection = false;            /**< TRUE if connected to server. FALSE if not. */

//const char* ssid = "DLink-782A77";  /**< Network SSID. */
//const char* password = "password";  /**< Network Password. */


/* -----------------------------------------------------
 * -                   Digital Outputs                 -
 * ----------------------------------------------------- */
const int Q0 = 16;      /**< D0 */
const int Q1 = 15;      /**< D8 */
const int Q2 = A0;      /**< A0 */
const int ledGreen = 2; /**< D4 */
const int ledRed = 0;   /**< D3 */

int StateQ0 = 0;        /**< State of input 0. */
int StateQ1 = 0;        /**< State of input 1. */
int StateQ2 = 0;        /**< State of input 2. */


/* -----------------------------------------------------
 * -                        TCP/IP                     -
 * ----------------------------------------------------- */
//WiFiClient ClientEsp;
//char server_ip[] = "192.168.10.2";


/* =====================================================
 * =                        Setup                      =
 * ===================================================== */
void setup(void) {
    
      Serial.begin(9600);
    
      /* Set NodeMCU I/O's */
      pinMode(Q0, INPUT);
      pinMode(Q1, INPUT);
      pinMode(ledGreen, OUTPUT);
      pinMode(ledRed, OUTPUT);
  
}


/* =====================================================
 * =                        Loop                       =
 * ===================================================== */
void loop(void) {

    String content = "";    /**< Content read from RFID. */
    uint8_t control = 0;    /**< Variable used to check if the card is still present. */
    char UID[] = "";        /**< UID of the RFID card. */
    String str = "";        /**< UID of the card, but in a 'string' format. */

}


/* Defines */
#define SS_PIN 4        /**< D2 SDA */
#define RST_PIN 5       /**< D1 RST */


/* Includes */
#include <SPI.h>
#include <MFRC522.h>
//#include <ESP8266WiFi.h>
//#include <ESP8266mDNS.h>


/* Prototypes */
uint8_t is_card_present(uint8_t control);
void clear_var(void);
void light_btn_pressed(void);
void DEBUG_btn_pressed(int btn);


/* -----------------------------------------------------
 * -                        DEBUG                      -
 * ----------------------------------------------------- */
bool debug = true;      /**< TRUE if debug is enabled. FALSE otherwise. */

 
/* -----------------------------------------------------
 * -                         RFID                      -
 * ----------------------------------------------------- */
MFRC522 mfrc522(SS_PIN, RST_PIN);           /* Create MFRC522 instance. */

String auth[] = {"04 43 C6 32 34 31 80"};   /**< Authorized Cards */
bool authorized = false;                    /**< TRUE if card was authorized. FALSE if not. */ 


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
    
      /* SPI - MFRC522 */
      SPI.begin();          // Initiate  SPI bus
      delay(100);
      mfrc522.PCD_Init();   // Initiate MFRC522
    
    
      /* WiFi */
      //Serial.print("Trying to establish WiFi connection...");
      //WiFi.begin(ssid, password);
     
      /* Wait for Connection */
      //while (WiFi.status() != WL_CONNECTED) {
      //      delay(200);
      //      Serial.print(".");
      //}
    
      /* Connection Established */
      //Serial.print("\nConnection Established!\n");
      //delay(200);

      /*  
      // Connection to Server
      Serial.print("Starting connection...");
      Serial.print("...");
      if (ClientEsp.connect(server_ip, 50000)) {
            connection = true;
           
            Serial.print("\nClient connected to server ");
            Serial.print(server_ip);
            Serial.print(", on port 50000.\n"); 
            delay(500);
      }
      Serial.println();
      */
}


/* =====================================================
 * =                        Loop                       =
 * ===================================================== */
void loop(void) {

    String content = "";    /**< Content read from RFID. */
    uint8_t control = 0;    /**< Variable used to check if the card is still present. */
    char UID[] = "";        /**< UID of the RFID card. */
    String str = "";        /**< UID of the card, but in a 'string' format. */

 
    /* Read RFID Card */
    if ((!authorized)) { 

        MFRC522::MIFARE_Key key;
        for (byte i=0; i<6; i++) 
            key.keyByte[i] = 0xFF;
        MFRC522::StatusCode status;

        if (!mfrc522.PICC_IsNewCardPresent())
            return;
        if (!mfrc522.PICC_ReadCardSerial())
            return;

        for (byte i=0; i<mfrc522.uid.size; i++) {   
            content.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
            content.concat(String(mfrc522.uid.uidByte[i], HEX));
        }

        content.toUpperCase();
        (content.substring(1)).toCharArray(UID, 21);
        String str(UID);

        /* DEBUG */
        Serial.print("\nChecking authorization for card:\n");
        Serial.println(UID);

        /* Check Authorization */
        for (int i=0; i<sizeof(auth); i++) {
            if (auth[i] == str) {
                authorized = true; 
                break;
            }
        }

        /* Card Authorized */
        if (authorized) {
              digitalWrite(ledGreen, HIGH);
              delay(500);
              digitalWrite(ledGreen, LOW);
              
              Serial.println("Card authorized!");
              /* ClientEsp.print(str); */

              connection = true; /* REMOVE THIS! */
        }
        else {
            digitalWrite(ledRed, HIGH);
            delay(500);
            digitalWrite(ledRed, LOW);
              
            Serial.println("Invalid card!");
        }
    }

    /* Read and Send Button State */
    else if ((connection) && (authorized)) {

        while(true) {

            /* Check if the card is still present */
            control = is_card_present(control);

            /* Card is present */
            if (control <= 2) {
      
                /* Read Input State */
                StateQ1 = digitalRead(Q1);
                StateQ0 = digitalRead(Q0);
                StateQ2 = analogRead(Q2);
                delay(100);
        
                /* Button 1 */
                if ((StateQ2 < 500) && (StateQ1 == LOW) && (StateQ0 == HIGH)) {    
                
                    light_btn_pressed();
                    DEBUG_btn_pressed(1);
                    /* ClientEsp.print("1"); */
                    clear_var();
                    break;
                }
        
                /* Button 2 */
                else if ((StateQ2 < 500) && (StateQ1 == HIGH) && (StateQ0 == LOW)) {
    
                    light_btn_pressed();
                    DEBUG_btn_pressed(2);
                    /* ClientEsp.print("2"); */
                    clear_var();
                    /* ClientEsp.stop(); */
                    break;
                }
    
                /* Button 3 */
                else if ((StateQ2 < 500) && (StateQ1 == HIGH) && (StateQ0 == HIGH)) {
    
                    light_btn_pressed();
                    DEBUG_btn_pressed(3);
                    /* ClientEsp.print("3"); */
                    clear_var();
                    break;
                }
    
                /* Button 4 */
                else if ((StateQ2 == 1024) && (StateQ1 == LOW) && (StateQ0 == LOW)) {
                    
                    light_btn_pressed();
                    DEBUG_btn_pressed(4);
                    /* ClientEsp.print("4"); */
                    clear_var();
                    break;
                }
    
                /* Button 5 */
                else if ((StateQ2 == 1024) && (StateQ1 == LOW) && (StateQ0 == HIGH)) {
                    
                    light_btn_pressed();
                    DEBUG_btn_pressed(5);
                    /* ClientEsp.print("5"); */
                    clear_var();
                    break;
                }
            }

            /* Card was removed */
            else { 
                Serial.println("\nCard removed!");
                clear_var();
                break;
            }
        }
    }
}


/** 
 *  @brief Checks if a valid card is present.
 */
uint8_t is_card_present(uint8_t control) {

    control = 0;
    
    for (byte i=0; i<3; i++) {
        if (!mfrc522.PICC_IsNewCardPresent())
          control = control + 1;
    }

    return control;
}


/**
 *  @brief Clears global variables authorized and connection.
 */
void clear_var(void) {
    
    authorized = false;
    connection = false;
}


/**
 *  @brief Lights the LED's if a button was pressed.
 */
void light_btn_pressed(void) {
    
    digitalWrite(ledGreen, HIGH);
    delay(500);
    digitalWrite(ledGreen, LOW);
}


/**
 *  @brief Prints debug messages for when a button is pressed.
 */
void DEBUG_btn_pressed(int btn) {

    if (debug) {
        delay(100);
    
        Serial.print("\nButton Pressed: ");
        Serial.println(btn);
        delay(100);
        
        Serial.print("Q0 State: ");
        Serial.println(StateQ0);
        delay(100);
        
        Serial.print("Q1 State: ");
        Serial.println(StateQ1);
        delay(100);
        
        Serial.print("Q2 State: ");
        Serial.println(StateQ2);
        delay(100);
    }
}


/** 
 *  TODO: 
 *          conectar à rede
 *          base da dados
 *          autenticar UID através da base de dados
 */

/* Defines */
#define SS_PIN 4                            /**< D2 SDA */
#define RST_PIN 5                           /**< D1 RST */


/* Includes */
#include <SPI.h>
#include <MFRC522.h>
#include <ESP8266HTTPClient.h>
#include <ESP8266WiFi.h>
#include <ESP8266mDNS.h>


/* Prototypes */
String read_card(void);
uint8_t is_card_present(uint8_t control);
void clear_var(void);
void post_request(String card_id, String mac, String ans);


/*
 * -----------------------------------------------------
 * -                         RFID                      -
 * ----------------------------------------------------- 
 */
MFRC522 mfrc522(SS_PIN, RST_PIN);           /* Create MFRC522 instance. */
uint8_t card_read = 0;                      /**< Indicates if a card is read (1) or not (0). */
String card_id = "";                        /**< UID of the RFID card (string format). */


/*
 * -----------------------------------------------------
 * -                   Digital Outputs                 -
 * ----------------------------------------------------- 
 */
const int Q0 = 16;                          /**< D0 */
const int Q1 = 15;                          /**< D8 */
const int Q2 = A0;                          /**< A0 */
const int ledGreen = 2;                     /**< D4 */
const int ledRed = 0;                       /**< D3 */

int StateQ0 = 0;                            /**< State of input 0. */
int StateQ1 = 0;                            /**< State of input 1. */
int StateQ2 = 0;                            /**< State of input 2. */


/* 
 * -----------------------------------------------------
 * -                        TCP/IP                     -
 * ----------------------------------------------------- 
 */
WiFiClient client;
char server_ip[] = "192.168.10.2";          /**< Server IP. */
char ssid[] = "DLink-782A77";               /**< Network SSID. */
char password[] = "password";               /**< Network Password. */

// Sample query
char INSERT_DATA[] = "{uid: %s, mac: %s, ans: %s}";
char query[128];


/* 
 ? =====================================================
 ? =                        Setup                      =
 ? ===================================================== 
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

    digitalWrite(ledRed, HIGH);

    /* SPI - MFRC522 */
    SPI.begin();          // Initiate  SPI bus
    delay(100);
    mfrc522.PCD_Init();   // Initiate MFRC522
    
    /* WiFi */
    Serial.print("\nConnecting to router...");
    WiFi.begin(ssid, password);
    
    /* Wait for Connection */
    while (WiFi.status() != WL_CONNECTED) {
        delay(200);
        Serial.print(".");
    }
    
    /* Connection Established */
    Serial.println("\nConnection Established!");
    delay(200);

    // Connection to Server
    Serial.print("Starting connection...");
    Serial.print("...");
    if (client.connect(server_ip, 8000)) {
        digitalWrite(ledRed, LOW);
        Serial.print("\nClient connected to server ");
        Serial.print(server_ip);
        Serial.print(", on port 8000.\n"); 
        delay(500);
    }
    Serial.println();
}


/*
 ? =====================================================
 ? =                        Loop                       =
 ? ===================================================== 
 */
/**
 * @brief Loop function.
 */
void loop(void) {

    //String mac = WiFi.macAddress();         /**< MAC address. */
    //String card_id = "04 43 C6 32 34 31 80";
    //String ans = "A";

    //post_request(card_id, mac, ans);
    //delay(1000);

    /* ###################################################################################################################### */

    uint8_t control = 0;                    /**< Variable used to check if the card is still present. */
    String mac = WiFi.macAddress();         /**< MAC address. */


    if (card_read == 0) {
        card_id = read_card();
        if (card_id != "")
            card_read = 1;
    }
    
    else {
        /* Check if the card is still present */
        control = is_card_present(control);
    
        /* Card is present */
        if (control <= 2) {     // control <= 2
            digitalWrite(ledGreen, HIGH);
    
            /* Read Input State */
            StateQ1 = digitalRead(Q1);
            StateQ0 = digitalRead(Q0);
            StateQ2 = analogRead(Q2);
            //delay(100);
            Serial.println(analogRead(A0));
            Serial.println(digitalRead(15));
            Serial.println(digitalRead(16));

    
            /* Button 1 */
            if ((StateQ2 < 500) && (StateQ1 == LOW) && (StateQ0 == HIGH)) { 
                Serial.println("A");   
    
                if (card_id != "") {
                    post_request(card_id, mac, "A");
                    digitalWrite(ledGreen, LOW);
                    clear_var();
                }
            }
    
            /* Button 2 */
            else if ((StateQ2 < 500) && (StateQ1 == HIGH) && (StateQ0 == LOW)) {
                Serial.println("B");   
    
                if (card_id != "") {
                    post_request(card_id, mac, "B");
                    digitalWrite(ledGreen, LOW);
                    clear_var();
                }
            }
    
            /* Button 3 */
            else if ((StateQ2 < 500) && (StateQ1 == HIGH) && (StateQ0 == HIGH)) {
                Serial.println("C");   
    
                if (card_id != "") {
                    post_request(card_id, mac, "C");
                    digitalWrite(ledGreen, LOW);
                    clear_var();
                }
            }
    
            /* Button 4 */
            else if ((StateQ2 >= 500) && (StateQ1 == LOW) && (StateQ0 == LOW)) { 
                Serial.println("D");   
    
                if (card_id != "") {
                    post_request(card_id, mac, "D");
                    digitalWrite(ledGreen, LOW);
                    clear_var();
                };
            }
    
            /* Button 5 */
            else if ((StateQ2 >= 500) && (StateQ1 == LOW) && (StateQ0 == HIGH)) {
                Serial.println("E");   
    
                if (card_id != "") {
                    post_request(card_id, mac, "E");
                    digitalWrite(ledGreen, LOW);
                    clear_var();
                }
            }
        }
    
        /* Card was removed */
        else if (control >=3) { 
            
            clear_var();
            digitalWrite(ledGreen, LOW);
        }
    }
}


/*
 ? =====================================================
 ? =                     Functions                     =
 ? ===================================================== 
 */
 /**
 * @brief Reads card UID.
 */
String read_card(void) {

    String content = "";
    char UID[] = "";

    if (!mfrc522.PICC_IsNewCardPresent())
        return "";
    if (!mfrc522.PICC_ReadCardSerial())
        return "";

    for (byte i=0; i<mfrc522.uid.size; i++) {   
        content.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
        content.concat(String(mfrc522.uid.uidByte[i], HEX));
    }

    content.toUpperCase();
    (content.substring(1)).toCharArray(UID, 21);
   
    String card_id(UID);
    Serial.println(card_id);

    return card_id;
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
 *  @brief Clears global variables authorized.
 */
void clear_var(void) {

    card_read = 0;
    card_id = "";
}


/**
 * @brief Send HTTP POST Request.
 * 
 */
void post_request(String card_id, String mac, String ans) {

    if (WiFi.status() == WL_CONNECTED) {
        HTTPClient http;
    
        http.begin("http://192.168.10.2:8000/quiz/response/");
        http.addHeader("Content-Type", "text/plain");

        sprintf(query, INSERT_DATA, card_id.c_str(), mac.c_str(), ans.c_str());
    
        //int httpCode = http.POST("Message from ESP8266");
        int httpCode = http.POST(query);
        String payload = http.getString();

        Serial.print("httpCode:");
        Serial.println(httpCode);
        Serial.print("payload:");
        Serial.println(payload);
    }
    else {
        Serial.println("Error in WiFi connection");
    }
}

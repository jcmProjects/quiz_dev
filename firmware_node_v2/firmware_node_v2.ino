/* Defines */
#define SS_PIN 4                            /**< D2 SDA */
#define RST_PIN 5                           /**< D1 RST */


/* Includes */
#include <ESP8266HTTPClient.h>
#include <ESP8266WiFi.h>
#include <ESP8266mDNS.h>


/* Prototypes */
void clear_var(void);
void post_request(String card_id, String mac, String ans);


/*
 * -----------------------------------------------------
 * -                         RFID                      -
 * ----------------------------------------------------- 
 */
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

    /* Connection to Server */
    Serial.print("Starting connection...");
    Serial.print("...");
    if (client.connect(server_ip, 8000)) {
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

    String mac = WiFi.macAddress();         /**< MAC address. */ 


    /* Read Input State */
    StateQ1 = digitalRead(Q1);
    StateQ0 = digitalRead(Q0);
    StateQ2 = analogRead(Q2);


    /* Button 1 */
    if ((StateQ2 < 500) && (StateQ1 == LOW) && (StateQ0 == HIGH)) { 
        Serial.println("A");   
        post_request("00 00 00 00 00 00 00", mac, "A");
        clear_var();
    }

    /* Button 2 */
    else if ((StateQ2 < 500) && (StateQ1 == HIGH) && (StateQ0 == LOW)) {
        Serial.println("B");   
        post_request("00 00 00 00 00 00 00", mac, "B");
        clear_var();
    }

    /* Button 3 */
    else if ((StateQ2 < 500) && (StateQ1 == HIGH) && (StateQ0 == HIGH)) {
        Serial.println("C");   
        post_request("00 00 00 00 00 00 00", mac, "C");
        clear_var();
    }

    /* Button 4 */
    else if ((StateQ2 >= 500) && (StateQ1 == LOW) && (StateQ0 == LOW)) { 
        Serial.println("D");   
        post_request("00 00 00 00 00 00 00", mac, "D");
        clear_var();
    }

    /* Button 5 */
    else if ((StateQ2 >= 500) && (StateQ1 == LOW) && (StateQ0 == HIGH)) {
        Serial.println("E");   
        post_request("00 00 00 00 00 00 00", mac, "E");
        clear_var();
    }                
}


/*
 ? =====================================================
 ? =                     Functions                     =
 ? ===================================================== 
 */

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
        Serial.println(WiFi.status());
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
        Serial.println(WiFi.status());
        Serial.println("Error in WiFi connection");
        
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
    
        /* Connection to Server */
        Serial.print("Starting connection...");
        Serial.print("...");
        if (client.connect(server_ip, 8000)) {
            Serial.print("\nClient connected to server ");
            Serial.print(server_ip);
            Serial.print(", on port 8000.\n"); 
            delay(500);
        }
        Serial.println();
    }
}

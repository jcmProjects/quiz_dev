/* Defines */
#define SS_PIN 4                            /**< D2 SDA */
#define RST_PIN 5                           /**< D1 RST */


/* Includes */
#include <SPI.h>
#include <MFRC522.h>
#include <ESP8266HTTPClient.h>
#include <ESP8266WiFi.h>
#include <ESP8266mDNS.h>
#include <MySQL_Connection.h>
#include <MySQL_Cursor.h>


/* Prototypes */
void post_request(String card_id, String mac, String ans);


/*
 * -----------------------------------------------------
 * -                        Router                     -
 * ----------------------------------------------------- 
 */
char ssid[] = "DLink-782A77";               /**< Network SSID. */
char password[] = "password";               /**< Network Password. */


/* 
 * -----------------------------------------------------
 * -                        TCP/IP                     -
 * ----------------------------------------------------- 
 */
WiFiClient client;
char server_ip[] = "192.168.10.2";

// Sample query
//char INSERT_DATA[] = "INSERT INTO quiz_project.quiz_answer (uid, mac, ans) VALUES ('%s','%s','%s')";   // '%s' or %s ??
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
    String card_id = "04 43 C6 32 34 31 80";
    String ans = "A";

    post_request(card_id, mac, ans);
    delay(1000);
}


/*
 ? =====================================================
 ? =                     Functions                     =
 ? ===================================================== 
 */
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

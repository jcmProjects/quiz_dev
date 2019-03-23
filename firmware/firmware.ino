/* Defines */
#define SS_PIN 4                            /**< D2 SDA */
#define RST_PIN 5                           /**< D1 RST */


/* Includes */
#include <SPI.h>
#include <MFRC522.h>
#include <ESP8266WiFi.h>
#include <ESP8266mDNS.h>
#include <MySQL_Connection.h>
#include <MySQL_Cursor.h>


/* Prototypes */
uint8_t is_card_present(uint8_t control);
void clear_var(void);
void DEBUG_btn_pressed(int btn);
long query_db(char UID[], row_values *row, long nmec);
void insert_db(long nmec, String mac, String ans);


/*
 * -----------------------------------------------------
 * -                         RFID                      -
 * ----------------------------------------------------- 
 */
MFRC522 mfrc522(SS_PIN, RST_PIN);           /* Create MFRC522 instance. */
bool authorized = false;                    /**< TRUE if card was authorized. FALSE if not. */ 
long nmec = 0;                              /**< variable read from Database (Student ID). */


/*
 * -----------------------------------------------------
 * -                        Router                     -
 * ----------------------------------------------------- 
 */
char ssid[] = "DLink-782A77";               /**< Network SSID. */
char password[] = "password";               /**< Network Password. */


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


/* 
 * -----------------------------------------------------
 * -                       Database                    -
 * ----------------------------------------------------- 
 */
IPAddress server_addr(192,168,10,2);        /**< IP of the MySQL *server*. */
char userSQL[] = "terminal";                /**< MySQL user login username. */
char passwordSQL[] = "password";            /**< MySQL user login password. */

MySQL_Connection conn( (Client *)&client ); /**< MySQL connection. */
MySQL_Cursor cur = MySQL_Cursor(&conn);     /**< MySQL cursor. */

// Sample query
const char QUERY_POP[] = "SELECT nmec FROM authentication.students WHERE uid = '%s';";
char INSERT_DATA[] = "INSERT INTO quiz_project.quiz_answer (nmec, mac, ans) VALUES ('%s','%s','%s')";   // '%s' or %s ??
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

    /* Connection to Database */
    Serial.println("Connecting to database...");
    if ( conn.connect(server_addr, 3306, userSQL, passwordSQL) ) {
        delay(1000);
    }
    else {
        Serial.println("Connection failed.");
    }
    // conn.close();

    digitalWrite(ledRed, LOW);
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

    String content = "";                    /**< Content read from RFID. */
    uint8_t control = 0;                    /**< Variable used to check if the card is still present. */
    char UID[] = "";                        /**< UID of the RFID card. */

    row_values *row = NULL;                 /**< Database return rows. */
//    long nmec = 0;                          /**< variable read from Database (Student ID). */

    String mac = WiFi.macAddress();         /**< MAC address. */

    delay(100);
    /* Read RFID Card */
    if (!authorized) { 

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
        Serial.println("\nChecking authorization for card:");
        Serial.println(UID);

        /* Query Database */
        nmec = query_db(UID, row, nmec);

        /* Check Authorization */
        if (nmec != 0)
            authorized = true;

        /* Card Authorized */
        if (authorized) {
            digitalWrite(ledGreen, HIGH);
            Serial.println("Card authorized!");
            Serial.print("MAC: ");
            Serial.print(WiFi.macAddress());
            Serial.print(", UID: ");
            Serial.println(UID);
        }
        else {
            digitalWrite(ledRed, HIGH);
            delay(500);
            digitalWrite(ledRed, LOW);
            Serial.println("Invalid card!");
        }
    }

    /* Read and Send Button State */
    else {  // else if ((connection) && (authorized)) {

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

                    insert_db(nmec, mac, "A");
                    digitalWrite(ledGreen, LOW);
                    //DEBUG_btn_pressed(1);
                    clear_var();
                    break;
                }
        
                /* Button 2 */
                else if ((StateQ2 < 500) && (StateQ1 == HIGH) && (StateQ0 == LOW)) {

                    insert_db(nmec, mac, "B");
                    digitalWrite(ledGreen, LOW);
                    //DEBUG_btn_pressed(2);
                    clear_var();
                    break;
                }
    
                /* Button 3 */
                else if ((StateQ2 < 500) && (StateQ1 == HIGH) && (StateQ0 == HIGH)) {

                    insert_db(nmec, mac, "C");
                    digitalWrite(ledGreen, LOW);
                    //DEBUG_btn_pressed(3);
                    clear_var();
                    break;
                }
    
                /* Button 4 */
                else if ((StateQ2 >= 500) && (StateQ1 == LOW) && (StateQ0 == LOW)) { 

                    insert_db(nmec, mac, "D");
                    digitalWrite(ledGreen, LOW);
                    //DEBUG_btn_pressed(4);
                    clear_var();
                    break;
                }
    
                /* Button 5 */
                else if ((StateQ2 >= 500) && (StateQ1 == LOW) && (StateQ0 == HIGH)) {

                    insert_db(nmec, mac, "E");
                    digitalWrite(ledGreen, LOW);
                    //DEBUG_btn_pressed(5);
                    clear_var();
                    break;
                }
            }

            /* Card was removed */
            else { 

                Serial.println("\nCard removed!");
                clear_var();
                digitalWrite(ledGreen, LOW);
                break;
            }
        }
    }
}


/*
 ? =====================================================
 ? =                     Functions                     =
 ? ===================================================== 
 */
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
    
    authorized = false;
    nmec = 0;
}


/**
 *  @brief Prints debug messages for when a button is pressed.
 */
void DEBUG_btn_pressed(int btn) {

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


/**
 * @brief Query the database.
 * 
 */
long query_db(char UID[], row_values *row, long nmec) {

    if (conn.connected()) {
        Serial.println("> Running SELECT with dynamically supplied parameter");

        // Initiate the query class instance
        MySQL_Cursor *cur_mem = new MySQL_Cursor(&conn);
        sprintf(query, QUERY_POP, UID);
        
        // Execute the query
        cur_mem->execute(query);
        
        // Fetch the columns (required) but we don't use them.
        column_names *columns = cur_mem->get_columns();
        
        // Read the row (we are only expecting the one)
        do {
            row = cur_mem->get_next_row();
            if (row != NULL)
                nmec = atol(row->values[0]);
        } while (row != NULL);
        
        // Deleting the cursor also frees up memory used
        delete cur_mem;
        
        // Show the result
        Serial.print("Student ID = ");
        Serial.println(nmec);

        return nmec;
    } 
    else {
        conn.close();
        digitalWrite(ledRed, HIGH);

        Serial.println("Connecting...");
            
        if (conn.connect(server_addr, 3306, userSQL, passwordSQL)) {
            delay(500);
            Serial.println("Successful reconnect!");
            digitalWrite(ledRed, LOW);
        } 
        else
            Serial.println("Cannot reconnect! Drat.");

        return 0;
    }
}


/**
 * @brief Insert into the database.
 * 
 */
void insert_db(long nmec, String mac, String ans) {

    delay(100);
    
    // Initiate the query class instance
    MySQL_Cursor *cur_mem = new MySQL_Cursor(&conn);

    String string_nmec = String(nmec);
    
    // Save
    sprintf(query, INSERT_DATA, string_nmec.c_str(), mac.c_str(), ans.c_str());
    
    // Execute the query
    cur_mem->execute(query);
    
    // Note: since there are no results, we do not need to read any data
    // Deleting the cursor also frees up memory used
    delete cur_mem;
}


//todo ---------------------------------------------------------------------------------------
/*  TODO: 
 *  
 *  
 */


/*  FIXME:
 * 
 * 
 */
//todo ---------------------------------------------------------------------------------------

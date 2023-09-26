#include Wire.h

#define ADXAddress 0xA7  1  7-bit address
#define Register_2D 0x2D   Power control register
#define Register_31 0x31   Data format register
#define Register_X0 0x32
#define Register_X1 0x33
#define Register_Y0 0x34
#define Register_Y1 0x35
#define Register_Z0 0x36
#define Register_Z1 0x37

int X0, X1, X_out;
int Y0, Y1, Y_out;
int Z0, Z1, Z_out;
double Xg, Yg, Zg;

void setup() {
  Wire.begin();         
  Serial.begin(9600);  
  delay(100);

   Initialize ADXL345
   Power Control Register
  Wire.beginTransmission(ADXAddress);
  Wire.write(Register_2D);
  Wire.write(8);   Measure enable
  Wire.endTransmission();

   Data Format Register for setting the range to ±16g & full resolution
  Wire.beginTransmission(ADXAddress);
  Wire.write(Register_31);
  Wire.write(0b00001111);  
  Wire.endTransmission();
}

void loop() {
  readAccelerometer();
  Serial.print(X= );
  Serial.print(Xg, 4);   4 decimal places
  Serial.print(       );
  Serial.print(Y= );
  Serial.print(Yg, 4);   4 decimal places
  Serial.print(       );
  Serial.print(Z= );
  Serial.println(Zg, 4);   4 decimal places
  delay(200);
}

void readAccelerometer() {
  Wire.beginTransmission(ADXAddress);
  Wire.write(Register_X0);
  Wire.endTransmission();
  Wire.requestFrom(ADXAddress, 6);

  if(Wire.available() = 6) {
    X0 = Wire.read();
    X1 = Wire.read();
    X1 = X1  8;
    X_out = X0  X1;

    Y0 = Wire.read();
    Y1 = Wire.read();
    Y1 = Y1  8;
    Y_out = Y0  Y1;

    Z0 = Wire.read();
    Z1 = Wire.read();
    Z1 = Z1  8;
    Z_out = Z0  Z1;

    Xg = X_out  0.0039;   Convert to g unit
    Yg = Y_out  0.0039;   Convert to g unit
    Zg = Z_out  0.0039;   Convert to g unit
  } else {
    Serial.println(Data not available!);
  }
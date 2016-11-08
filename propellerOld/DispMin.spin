CON
  _clkmode        = xtal1 + pll16x
  _xinfreq        = 5_000_000 

  ADDR = $72<<1
  PIN_SCL = 0

OBJ    
  i2c : "Basic_I2C_Driver_1" 

PUB Main | x

  i2c.Initialize(PIN_SCL)

  i2c.Start(PIN_SCL)
  i2c.Write(PIN_SCL,ADDR)
  i2c.Write(PIN_SCL,$21) ' Oscillator
  i2c.Stop(PIN_SCL)

  i2c.Start(PIN_SCL)
  i2c.Write(PIN_SCL,ADDR)
  i2c.Write(PIN_SCL,$EF) ' Brightness
  i2c.Stop(PIN_SCL)

  i2c.Start(PIN_SCL)
  i2c.Write(PIN_SCL,ADDR)
  i2c.Write(PIN_SCL,$81) ' Power
  i2c.Stop(PIN_SCL)

  i2c.Start(PIN_SCL)
  i2c.Write(PIN_SCL,ADDR)
  i2c.Write(PIN_SCL,0)   ' LED pattern
  i2c.Write(PIN_SCL,$A5)
  i2c.Write(PIN_SCL,$5A)
  i2c.Write(PIN_SCL,$5A)
  i2c.Write(PIN_SCL,$A5)
  i2c.Write(PIN_SCL,$A5)
  i2c.Write(PIN_SCL,$5A)
  i2c.Write(PIN_SCL,$5A)
  i2c.Write(PIN_SCL,$A5)
  i2c.Write(PIN_SCL,$A5)
  i2c.Write(PIN_SCL,$5A)
  i2c.Write(PIN_SCL,$5A)
  i2c.Write(PIN_SCL,$A5)
  i2c.Write(PIN_SCL,$A5)
  i2c.Write(PIN_SCL,$5A)
  i2c.Write(PIN_SCL,$5A)
  i2c.Write(PIN_SCL,$A5)  
  i2c.Stop(PIN_SCL)
        
  repeat

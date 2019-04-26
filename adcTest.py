import smbus 
import time 

I2CADDR = 0x21 
CMD_CODE = 0x10

bus = smbus.SMBus(1) 


bus.write_byte( I2CADDR, CMD_CODE ) 
tmp = bus.read_word_data( I2CADDR, 0x00 ) 

print(tmp) # before bit manipulation (for checking, remove when finalising)

tmp = ( ( ( (tmp << 8) + (tmp >> 8) ) | 0xFFF000 ) ^ 0xFFF000 )

print(tmp) # after bit manipulation (true value)

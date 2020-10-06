# Timemark

Encode/Decode UTC time to/from a compact string representation

```
timemark.py              Encode current UTC time
timemark.py <timemark>   Decode timemark to UTC time
```

The timemark string is in the format YMD-TTTT where,  
  Y is the last digit of the year (relative to 2020)  
  M is the month in hexadecimal  
  D is the day in base-32  
  TTTT is the time in base-32 ('0000' to 'ZZZZ')  

- The time is divided into 1048576 increments with '0000' representing 12:00.00am and 'ZZZZ' representing 11:59.99pm   
- The interval of each time increment is therefore 0.082397 seconds
- Base-32 is encoded as [0-9A-Z] excluding B,I,O and U

For example, Sept 16 2020 at 7:40pm encodes to 09H-T7AS

enjoy!
 
frankie@rootcode.org

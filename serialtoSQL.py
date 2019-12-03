import MySQLdb
import serial
import time
import datetime

db = MySQLdb.connect(host="mysli.oamk.fi", user="t8mios00",
                     passwd="FPeRsNjALZXT22Xa", db="opisk_t8mios00")

cur = db.cursor()

port = "/dev/ttyACM0"
baud = 9600
sample = 20

serialPort = serial.Serial(port, baud, timeout = 1)

#time.sleep(1)

tempSum = 0.0
humiSum = 0.0
count = 0
temperature = ""
humidity = ""

while True:
    ser = str(serialPort.readline())
    if(len(ser) == 21):
        temperature = ser[14] + ser[15]
        humidity = ser[8] + ser[9]
        tempSum += float(temperature)
        humiSum += float(humidity)
        #time.sleep(.1)
        count += 1
    
    if count == sample:
        cur.execute("SELECT MAX(idweather) FROM weather")
        currentID = str(cur.fetchall())
        currentID = int(currentID.replace("(", "").replace(",", "").replace(")", ""))
        
        tempAvg = tempSum / sample
        humiAvg = humiSum / sample
        print("%.6f "%tempAvg)
        print("%.6f"%humiAvg)
        
        time = datetime.datetime.now().time()
        date = datetime.datetime.now().date()
        
        sql = ("INSERT INTO weather VALUES(%s, '%s', '%s', %.4f, %s)" % \
               (currentID + 1, date, time, tempAvg, humiAvg))
        try:
            cur.execute(sql)
            db.commit()
            print("jes")
        except:
            db.rollback()
            print("es")
            
        count = 0
        tempSum = 0.0
        humiSum = 0.0

serialPort.close()
db.close()

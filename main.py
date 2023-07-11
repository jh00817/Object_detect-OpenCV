from object_detect import detect
from record import record
import time
from datetime import datetime

while True :
    now = datetime.now()
    current_time = now.strftime("%H_%M_%S")

    name = "test" +str( current_time )
    print (name)
    record(name,5)

    print(detect('output_'+str(name)+'.avi',4))


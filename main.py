from object_detect import detect
from record import record
import time
from datetime import datetime

def function_detect() :

    now = datetime.now()
    current_time = now.strftime("%H_%M_%S")

    name = "test" +str( current_time )
    print (name)
    record(name,5)

    cond = detect('output_'+str(name)+'.avi',4)
    
    return cond

 

if __name__ == "__main__" :

    function_detect()

from object_detect import detect
from record import record
import time

name = "test"

record(name)

detect('output_'+str(name)+'.avi',4)
#detect(0,4)

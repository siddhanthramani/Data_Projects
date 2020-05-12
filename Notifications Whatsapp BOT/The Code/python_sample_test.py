import threading
from time import sleep


def hello():
    print("hello")


timer = threading.Timer(10, hello)
timer.start()

sleep(5)
timer.cancel()
timer = threading.Timer(10, hello)
timer.start()

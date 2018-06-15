from . import Ecran

ecran = Ecran()
ecran.start()

try:
    from time import sleep
    while True:
        sleep(0.1)
except KeyboardInterrupt:
    ecran.stop()
    print('\nKeyboard interrupt received, exiting')

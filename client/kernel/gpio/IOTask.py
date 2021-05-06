import time
import threading
from Globals import logger


class IOTask(threading.Thread):
    """rasberry GPIO installed or not"""
    STATE_OFF = 0
    STATE_TIMER = 1
    STATE_DONE = 2

    ####################################################################################
    def __init__(self, buttonPin, ledPin, task, seconds):
        threading.Thread.__init__(self, name="IOTask for Button " + str(buttonPin))
        self.setDaemon(True)

        self.lock = threading.Lock()

        self.buttonPin = buttonPin
        self.ledPin = ledPin
        self.task = task
        self.seconds = seconds

        self.state = IOTask.STATE_OFF
        self.taskTime = 0

        self.enabled = True
        try:
            import RPi.GPIO as GPIO
        except:
            self.enabled = False
            logger.error("Raspberry GPIO features are not installed. Contact your vendor.")
            logger.develop("'RPi.GPIO' library is not installed. install from https://pypi.python.org/pypi/RPi.GPIO")
            return

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(ledPin, GPIO.OUT, initial=GPIO.LOW)

        GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(buttonPin, GPIO.BOTH)
        GPIO.add_event_callback(buttonPin, self.callback)

    ####################################################################################
    def run(self):

        oldState = self.state
        while self.enabled:
            time.sleep(0.2)

            if self.state == IOTask.STATE_TIMER and self.taskTime < time.time():
                self.threadCall(self.onTimerEvent)

            if oldState == self.state:
                continue

            if self.state == IOTask.STATE_TIMER:

                now = time.time()
                digit = abs(10 * now) - 10 * abs(now)
                if digit < 5:
                    self.ledOff()
                else:
                    self.ledOn()

            elif self.state == IOTask.STATE_DONE:
                self.ledOn()
            else:
                self.ledOff()

    ####################################################################################
    def callback(self, _):
        try:
            import RPi.GPIO as GPIO
        except:
            return
        buttonState = GPIO.input(self.buttonPin)
        if buttonState == 1:
            self.threadCall(self.onButtonPushed)
        else:
            self.threadCall(self.onButtonFreed)

    ####################################################################################
    def threadCall(self, method):
        threading.Thread(target=self.safeCall, args=[method]).start()

    ####################################################################################
    def safeCall(self, method):
        self.lock.acquire()
        try:
            method()
        except Exception as e:
            raise e
        finally:
            self.lock.release()

    ####################################################################################
    def onButtonPushed(self):
        if self.state == IOTask.STATE_DONE:
            return

        if self.state != IOTask.STATE_OFF:
            return self.invalidate()

        self.state = IOTask.STATE_TIMER
        self.taskTime = time.time() + self.seconds  # Turn Timer On

    ####################################################################################
    def onButtonFreed(self):
        if self.state == IOTask.STATE_TIMER:
            self.state = IOTask.STATE_OFF
            self.taskTime = 0  # Turn Timer Off

    ####################################################################################
    def onTimerEvent(self):
        if self.state != IOTask.STATE_TIMER:
            return self.invalidate()

        self.task()
        self.taskTime = 0  # Turn Timer Off
        self.state = IOTask.STATE_DONE
        time.sleep(2)
        self.state = IOTask.STATE_OFF

    ####################################################################################
    def invalidate(self):
        self.state = IOTask.STATE_OFF
        self.taskTime = 0

    ####################################################################################
    def ledOff(self):
        import RPi.GPIO as GPIO
        GPIO.output(self.ledPin, GPIO.LOW)

    ####################################################################################
    def ledOn(self):
        import RPi.GPIO as GPIO
        GPIO.output(self.ledPin, GPIO.HIGH)

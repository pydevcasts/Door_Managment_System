import threading
import time
import traceback

import serial
from serial.tools.list_ports import comports
from Globals import logger, SIMULATION_ENABLED
from client.kernel.Environment import environment
from client.kernel.analyze.AnalyzerFactory import analyzerFactory
from client.kernel.core.Constants import Constants
from client.kernel.core.Reader import Reader
from client.kernel.core.SystemData import systemData


####################################################################################
####################################################################################
class SerialCommunicator(threading.Thread):
    """ارتباط سریال در اینجا بر قرار میشه
    """
    ####################################################################################
    def __init__(self):
        threading.Thread.__init__(self, name="SerialCommunicator")

        self.setDaemon(True)

        self.readIntFunction = None

        self.connected = False
        self.portDevice = None
        self.portDesc = None
        self.ser = None

        self.reader = Reader()

        self.reset()

        self.mechanical = False
        self.mechanicalListeners = []

    ####################################################################################
    def reset(self):
        systemData.currentState = Constants.RUHEN

        self.connected = False
        self.reader.reset()

        self.portDevice = None
        self.portDesc = None
        self.ser = None

        from client.kernel.setting.SettingsManager import settingsManager
        settingsManager.invalidate()

    ####################################################################################
    def run(self):
        """همه پورتهای سریال خوندم  و از تک تکشون گفتم مثلا اسم دیوایستون چیه
            پورتت چیه توضیحت چیه 
          و بیا با تک تک این  serial.Serial و با لایبرری سریال پایتون
          portDevice وصل شو
          و با اون منطق اون سریالی که تو سیستم خودمون داشتیم 
          (baudrateو parityو stopbitsوbytesizeو )
          بیا وصل شو ببین اگه وصل شدی که خیلی خوب احتمال داره کنترل باکس ما باشه اگه وصل نشدی کنترل باکس 
          ما نیست پس یه وسیله دیگس 
          اگه وصل شدی بیا ارتباطتو اینشیالایز کنی
          و ارتباطتو هند شیک کنی یعنی ارتباطمون با کامپیوتر اکی شده با رزبری اکی شده شروع کنیم به هند شیک کردن
          یعنی یه دیتایی بدیم یه دیتایی بگیریم
          اگه پیغام خطای نیومد مطمن شیم که کنترل باکسمونو پیدا کردیم

        """
        while True:

            systemData.currentState = Constants.POWERUP

            logger.debug("Scanning all serial ports to detect the door.")

            res = comports()
            """scan for available ports. return a list of device names """
            for port in res:
                try:
                    try:
                        self.portDevice = port.device  # PySerial 3.x support
                    except:
                        self.portDevice = port[0]  # PySerial 2.x support

                    try:
                        self.portDesc = port.description  # PySerial 3.x support
                    except:
                        self.portDesc = port[1]  # PySerial 2.x support

                    logger.debug('Scanning port "' + self.portDevice + '" for the connected door')

                    self.ser = serial.Serial(
                        port=self.portDevice, baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_TWO,
                        bytesize=serial.EIGHTBITS, timeout=3)

                    self.initializeSerial()

                    self.handShake(False)

                    break

                except:
                    logger.debug("No door detected on port " + self.portDevice)
                    logger.exception(traceback.format_exc())
                    self.reset()

            if self.ser is not None:
                logger.success("connected to door on port: " + self.portDesc)
                self.connected = True
                try:
                    # Simulation of system hibernate. in order to force control box to send version number (1050) again.
                    for j in range(0, 10):
                        if environment.isVersionValid():
                            break

                        for i in range(0, 10):
                            time.sleep(10.0 / 1000.0)
                            self.handShake(i == 0)

                    if not environment.isVersionValid():
                        raise Exception('unable to read Master Software Version')

                    systemData.currentState = Constants.RUHEN

                    # Main Loop for receive/send serial data
                    while True:
                        time.sleep(10.0 / 1000.0)
                        self.handShake(not self.mechanical)
                except:
                    self.reset()
                    logger.error("Door is disconnected.")
                    logger.exception(traceback.format_exc())
                    continue  # main While True

            elif self.portDevice is None:
                # No Serial port on this PC!
                logger.debug("No serial port detected!")

            self.reset()
            try:
                time.sleep(3)
            except:
                pass
                # logger.exception(traceback.format_exc())

    ####################################################################################
    def initializeSerial(self):

        if not self.raspberryUART():
            return

        try:
            import RPi.GPIO as GPIO
        except:
            logger.error("Raspberry GPIO features are not installed. Contact your vendor.")
            logger.develop("'RPi.GPIO' library is not installed. install from https://pypi.python.org/pypi/RPi.GPIO")
            return

        import RPi.GPIO as GPIO
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(18, GPIO.OUT)
        GPIO.output(18, GPIO.LOW)

    ####################################################################################
    def handShake(self, sendResponse=True):
        """هند شیک دو تا دیوایس
        کنترل باکس یه پیغامی میفرسته وبعد چند میلی ثانیه بعد دیجیتال سویچ
        که ما داریم روی رزبری پای نقششو داریم بازی میکنیمیه پیغام دیگه ای میفرسته
        و این پیغامها یک استانداردی دارن
        مثلا کنترل باکس یک پیغام 24 بایتی میفرسته که هر کدومش یه معنی ای دارن
        دیجیتال سوییچ یه پیغام 15 بایتی میفرسته و این تا ابد ادامه داره 
        و تا وقتی که کنار همدیگه هستن بهم پیام میدنو کد منطقشون اینه کنترل باکس پیامشو میفرسته
        دیگه کاری نداره دیجیتال سوییچ چی کار کرده و بعد دیجیتال سوییچ پیامشو میفرسته کاری نداره که 
        کنترل باکس چی کار کرده 
        ولی جفت اینا وقتی پبامو دریافت میکنن 
        اون پشت پیامو انالیز میکنن و ممکنه در پیامهای بعدی که ارسال میکنن تاثیر بزاره

        """
        dataList = self.read()
        if dataList is None:
            return

        # print(dataList)

        # p = dataList[10] * 256 + dataList[11]
        # if p != 1000 and p != 3000 :
        #    print("r: " + str(dataList))

        from client.kernel.serial.SerialSendManager import serialSendManager
        sendList = analyzerFactory.analyze(dataList)
        """ این دقیقا همون جوابیه که من میخام بفرستم برای کنترل باکس
        البته این مستقیم به کنترل باکس نمیره برای 
        serialsendmanager
            میفرسته و بعد از اون
            serialsendmanager  
            میفرسته به کنترل باکس و خلاصه نگاه میکنه ببینه صفی هستش 
            طبق اون صفی که ما اسمشو گذاشتیم 
            serialsendqueue
        میفرسته
        """
        if not sendResponse:
            return

        sendList = serialSendManager.send(sendList)
        self.send(sendList)
        # print(sendList)

        # p = sendList[10] * 256 + sendList[11]
        # if p != 1000 and p != 3000 :
        #    print("s: " + str(sendList))

    ####################################################################################
    def read(self):
        last = time.time()
        unusedCounter = 0

        while True:
            lines = self.ser.read()
            now = time.time()

            # It seems that system time is changed manually
            if now - last > 60:
                last = now

            # No data is read, is it a long period without data?
            if len(lines) == 0:
                if now - last > 2.5:
                    raise Exception('There\'s a long time with no data receieved')

            for line in lines:
                last = now

                unusedCounter = unusedCounter + 1
                if unusedCounter > 120:  # too many bytes but no pattern! it's a device, but not a door
                    raise Exception('The connected device is not a door')

                try:
                    byte = self.readInt(line)
                except:
                    continue

                dataList = self.reader.read(byte)
                if dataList is not None:
                    # print('received: ' + str (dataList))
                    unusedCounter = 0
                    return dataList

    ####################################################################################
    def readInt(self, line):
        """check unicode is str or int or none"""
        if self.readIntFunction is not None:
            return self.readIntFunction(line)

        try:
            self.readIntFunction = ord
            """Return the Unicode code point for a one-character string"""
            return ord(line)
        except:
            pass

        try:
            self.readIntFunction = int
            return int(line)
        except:
            pass

        self.readIntFunction = None
        raise Exception('Invalid Serial Data from door')

    ####################################################################################
    def send(self, sendList):
        # print ('send: ' + str (sendList))
        self.preSend()
        self.ser.write(sendList)
        self.postSend()

    ####################################################################################
    def preSend(self):

        if self.raspberryUART():
            import RPi.GPIO as GPIO
            # GPIO.setmode(GPIO.BCM)
            # GPIO.setup(18, GPIO.OUT)
            GPIO.output(18, GPIO.HIGH)

    ####################################################################################
    def postSend(self):

        if self.raspberryUART():
            time.sleep(.05)
            import RPi.GPIO as GPIO
            GPIO.output(18, GPIO.LOW)

    ####################################################################################
    def raspberryUART(self):
        return self.portDevice is not None and (self.portDevice == '/dev/ttyAMA0' or self.portDevice == '/dev/ttyS0')

    ####################################################################################
    def isSerialConnected(self):
        return self.connected and not self.mechanical

    ####################################################################################
    def setMechanical(self, mechanical):
        if self.mechanical == mechanical:
            return

        self.mechanical = mechanical
        self.fireMechanicalChanged()
        return self.mechanical

    ################################################################################
    def addMechanicalListener(self, listener):
        if listener is None:
            return
        self.mechanicalListeners.append(listener)

    ################################################################################
    def fireMechanicalChanged(self):
        for listener in self.mechanicalListeners:
            listener.mechanicalChanged(self.mechanical)
          


####################################################################################
####################################################################################
####################################################################################

serialCommunicator = None
if SIMULATION_ENABLED:
    from client.kernel.serial.DummySerialCommunicator import DummySerialCommunicator

    serialCommunicator = DummySerialCommunicator()
else:
    serialCommunicator = SerialCommunicator()

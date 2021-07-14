import threading
import traceback
import socket

from Globals import interface, logger
from common.kernel.request.Request import Request



class BluetoothListener(threading.Thread):

    ####################################################################################
    def __init__(self):
        threading.Thread.__init__(self, name="BluetoothListener")
        self.setDaemon(True)

        self.enabled = True
        self.initialCheck()
        """check for bluetoos is connected
        """

        self.server_sock = None

        self.shouldRestarted = False

        from Globals import interface
        interface.get().addDoorNameListener(self)

        from Exit import exit
        exit.register(self.cleanUp)

    ####################################################################################
    def initialCheck(self):
        """ داریم چک میکنیم ببینیم ارتباطمون با بلوتوث برقرار شده یا خیر
        """
        try:
            from bluetooth import BluetoothSocket
        except:
            self.enabled = False
            logger.error("Bluetooth features are not installed. Contact your vendor.")
            logger.develop("Bluetooth library is not installed. Execute: 'sudo apt-get install bluez python-bluez'")

    ####################################################################################
    def run(self):

        if not self.enabled:
            return

        from bluetooth import BluetoothSocket, RFCOMM, PORT_ANY, advertise_service
        from bluetooth import SERIAL_PORT_CLASS, SERIAL_PORT_PROFILE  # , OBEX_UUID
        """[https://fa.wikipedia.org/wiki/%D8%A8%D9%84%D9%88%D8%AA%D9%88%D8%AB]
        چک کن لینک بالا در مورد پرتکل
        
        """
        while self.enabled:

            try:
                if self.server_sock is None:
                    self.server_sock = BluetoothSocket(RFCOMM)
                    """بیا یه پورت شبیه سازی شده بزار"""
                    self.server_sock.bind(("", PORT_ANY))
                    self.server_sock.settimeout(4.0)
                    self.server_sock.listen(1)

                    port = self.server_sock.getsockname()[1]
                    uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

                    advertise_service(self.server_sock, "DeutshctecPiServer",
                                      service_id=uuid,
                                      service_classes=[uuid, SERIAL_PORT_CLASS],
                                      profiles=[SERIAL_PORT_PROFILE],
                                      # protocols = [ OBEX_UUID ]
                                      )

                    logger.debug("Waiting for connection on RFCOMM channel %d" % port)

            except:
                logger.error("Error in initializing Bluetooth Connection. Bluetooth is disabled")
                logger.exception(traceback.format_exc())
                try:
                    self.server_sock.close()
                except:
                    ""
                self.server_sock = None
                break

            try:
                client_sock, client_info = self.server_sock.accept()

                logger.debug("Accepted connection from " + str(client_info))
                data = client_sock.recv(1024)

                logger.debug("received [%s]" % data)
                try:
                    # Python 3.x mode, Receiving Bytes
                    requestStr = data.decode("utf-8")
                except:
                    # Python 2.x mode, Receiving String
                    requestStr = str(data)

                try:
                    request = Request(Request.UNDEFINED, requestStr)
                    response = interface.get().handle(request)
                    logger.debug("response: " + response.toJson())

                    if response is not None:
                        responseStr = response.toJson()
                        client_sock.send(responseStr)

                except:
                    logger.exception(traceback.format_exc())

            
            #except BluetoothSocket.timeout as e:
            #    print("1")
            #    pass

            except Exception as e:
                if (str(e) != 'timed out'):
                    logger.exception(traceback.format_exc())
                    try:
                        self.server_sock.close()
                    except:
                        pass
                    self.server_sock = None

            if self.shouldRestarted:
                self.restartBluetoothService()

    ####################################################################################
    def cleanUp(self):
        self.enabled = False
        try:
            if self.server_sock is not None:
                self.server_sock.close()
        except:
            pass
        self.server_sock = None

    ####################################################################################
    def doorNameChanged(self, name):
        logger.debug("bluetoothListener.doorNameChanged()")

        if self.updateBluetoothName(name):
            self.shouldRestarted = True

    ###########################################################################
    def updateBluetoothName(self, name):

        import platform
        if platform.system() != 'Linux':
            return False

        raspberryName = self.generateBluetoothName(name)
        if raspberryName is None:
            return False

        try:
            f = open('/etc/machine-info', 'w')
            text = 'PRETTY_HOSTNAME=' + raspberryName
            f.write(text)
            f.close()
        except:
            logger.error("Unable to change Bluetooth Name")
            import traceback
            logger.exception(traceback.format_exc())

        return True

    ###########################################################################
    def generateBluetoothName(self, name):
        if name is None or len(name) < 4:
            return None

        import string
        result = ""
        for c in name:
            if c in string.ascii_letters or c in string.digits:
                result += c
            else:
                result += '-'

        return result

    ####################################################################################
    def restartBluetoothService(self):
        logger.debug("bluetoothListener.restartBluetoothService()")

        try:
            self.server_sock.close()
        except:
            pass
        self.server_sock = None

        try:
            import subprocess
            """ از ماژول subprocess و متد check_output 
            دستورات مورد نیاز برای دریافت نام شبکه هایی که قبلا به آن ها متصل شده ایم را دریافت میکنیم
            """
            import time

            subprocess.call(["service", "bluetooth", "restart"])
            time.sleep(1.0)
            subprocess.call(["hciconfig", "hci0", "up"])
            subprocess.call(["hciconfig", "hci0", "sspmode", "1"])
            subprocess.call(["hciconfig", "hci0", "piscan"])

        except:
            logger.exception(traceback.format_exc())

        self.shouldRestarted = False
    

####################################################################################
####################################################################################
####################################################################################

bluetoothListener = BluetoothListener()

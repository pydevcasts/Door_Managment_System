import socket
import threading
import traceback

from Globals import logger


class UDPCommunicator(threading.Thread):
    """udpconnection comman"""

    PORT_UDP_CLIENT = 20049
    PORT_UDP_SERVER = 23341

    ###############################################################################################################
    def __init__(self, listenerPort):
        threading.Thread.__init__(
            self, name="UDP Listener on port " + str(listenerPort)
        )
        self.setDaemon(True)

        self.active = True

        self.listenerHost = ""  # for UDP purposes
        self.listenerPort = listenerPort

        from Exit import exit

        exit.register(self.cleanUp)

    ###############################################################################################################
    def isActive(self):
        return self.active

    ###############################################################################################################
    def deserialize(self, str_):
        # abstract
        pass

    ###############################################################################################################
    def run(self):
        # Set the socket parameters
        address = (self.listenerHost, self.listenerPort)  # host, port

        # Create socket and bind to address
        self.listenerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.listenerSocket.bind(address)

        logger.debug(
            "start UDP listening on " + self.listenerHost + ":" + str(self.listenerPort)
        )

        # Now wait for client connection.
        while self.isActive():
            # Establish connection with client.
            try:
                encodedBytes, host = self.listenerSocket.recvfrom(1024)
                logger.shit(
                    "UDP bytes recieved from " + host[0] + ": " + str(encodedBytes)
                )
                objectStr = encodedBytes.decode("utf-8")
                logger.shit("UDP Object recieved: " + objectStr)

                object = None
                try:
                    object = self.deserialize(objectStr)
                except:
                    logger.exception(traceback.format_exc())

                self.handle(object, host[0])

            except:
                logger.exception(traceback.format_exc())
                continue

        self.listenerSocket.close()

    ###############################################################################################################
    @staticmethod
    def send(response, host, port):

        # print(response.toJson())
        if response is None:
            return

        logger.shit("sending " + str(response) + " to " + host + ":" + str(port))

        address = (host, port)  # broadcast address explicitly
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Create socket
        """
        AF_INET: پروتکل های IPv4 (هر دو TCP و UDP)
        SOCK_STREAM: جریان بایت TCP با اتصال مسیریابی
        SOCK_DGRAM: انتقال UDP از datagrams (بسته های IP خودی که بر روی تأیید مشتری-سرور تکیه نمی کنند)
        SOCK_RAW: یک سوکت خام
        SOCK_RDM: برای دیتاگرام های قابل اعتماد
        SOCK_SEQPACKET: انتقال متوالی سوابق در یک اتصال
        """
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        """
        There is a socket flag to set, in order to prevent this, socket.SO_REUSEADDR:
        the SO_REUSEADDR flag tells the kernel to reuse a
        local socket in TIME_WAIT state, without waiting for its natural timeout to expire.
        """
        """
        socket.setsockopt(level, optname, value: int)
        socket.setsockopt(level, optname, value: buffer)
        socket.setsockopt(level, optname, None, optlen: int)
        
        Set the value of the given socket option (see the Unix manual page setsockopt(2)). 
        The needed symbolic constants are defined in the socket module (SO_* etc.). 
        The value can be an integer, None or a bytes-like object representing a buffer. 
        In the later case it is up to the caller to ensure that the bytestring contains 
        the proper bits (see the optional built-in module struct for a way to encode
        C structures as bytestrings). When value is set to None, optlen argument is required.
        It’s equivalent to call setsockopt() C function with optval=NULL and optlen=optlen.
        """
        error = None
        for i in range(10):
            try:
                responseStr = response.toJson()
                try:
                    # Deap 2.x mode, sending String
                    if s.sendto(responseStr, address):
                        return True
                except:
                    # Deap 3.x mode, sending bytes
                    encodedBytes = bytes(responseStr, "UTF-8")
                    if s.sendto(encodedBytes, address):
                        return True

            except Exception as e:
                error = str(e)

        logger.debug("Unable to send UDP response because of: " + str(error))
        s.close()
        return False

    ###############################################################################################################
    def handle(self, request, host):
        pass

    ###############################################################################################################
    def cleanUp(self):
        self.active = False
        try:
            self.listenerSocket.close()
        except:
            pass

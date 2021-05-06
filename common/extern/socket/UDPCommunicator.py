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
        threading.Thread.__init__(self, name="UDP Listener on port " + str(listenerPort))
        self.setDaemon(True)

        self.active = True

        self.listenerHost = ''  # for UDP purposes
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

        logger.debug('start UDP listening on ' + self.listenerHost + ':' + str(self.listenerPort))

        # Now wait for client connection.
        while self.isActive():
            # Establish connection with client.
            try:
                encodedBytes, host = self.listenerSocket.recvfrom(1024)
                logger.shit('UDP bytes recieved from ' + host[0] + ': ' + str(encodedBytes))
                objectStr = encodedBytes.decode("utf-8")
                logger.shit('UDP Object recieved: ' + objectStr)

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

        logger.shit('sending ' + str(response) + ' to ' + host + ':' + str(port))

        address = (host, port)  # broadcast address explicitly
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Create socket
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

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
                    encodedBytes = bytes(responseStr, 'UTF-8')
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

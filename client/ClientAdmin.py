
from client.shell.admin.Interface import Interface
"""PyQt client QApplication"""

def init(kernel):
    shell = Interface()

    from Globals import interface
    interface.register(shell)

    shell.initKernel(kernel)
    return shell


def main() :
    from client import ClientKernel
    kernel = ClientKernel.init()

    shell = init(kernel)

    kernel.start()

    import time
    time.sleep(3)

    shell.start()


if __name__ == "__main__":
    main()

from Globals import interface


def init(kernel, shell):
    from client.extern.Interface import Interface
    extern = Interface()
    interface.register(extern)
    extern.initKernel(kernel)
    extern.initShell(shell)
    return extern


def main():
    from client import ClientKernel
    kernel = ClientKernel.init()

    from client import ClientDummyShell
    shell = ClientDummyShell.init(kernel)

    extern = init(kernel, shell)

    kernel.start()
    extern.start()
    shell.start()


if __name__ == "__main__":
    main()

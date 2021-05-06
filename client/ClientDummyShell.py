def init(kernel):
    from client.shell.dummy.Interface import Interface
    shell = Interface()

    from Globals import interface
    interface.register(shell)

    shell.initKernel(kernel)
    return shell


def main():
    from client import ClientKernel
    kernel = ClientKernel.init()

    shell = init(kernel)

    kernel.start()
    shell.start()


if __name__ == "__main__":
    main()

def init(kernel):
    """refrence to interface for pyqt"""
    from client.shell.pc.Interface import Interface
    shell = Interface()

    from Globals import interface
    interface.register(shell)

    shell.initKernel(kernel)
    return shell


def main():
    from client import ClientKernel
    kernel = ClientKernel.init()

    shell = init(kernel)
    """لایه اکسترن نداره فقط کرنلو میاره بالا و شل پی سی 
    در نتیجه فرمان موبایل نمیگیره ولی خودش مانیتور و کیبورد و بهش وصل کنیم کار میکنه دربمون
    """
    kernel.start()
    shell.start()


if __name__ == "__main__":
    main()

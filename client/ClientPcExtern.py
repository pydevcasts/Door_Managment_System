from Globals import interface
"""frame mode"""

def init(kernel, shell):
    from client.extern.Interface import Interface
    extern = Interface()
    interface.register(extern)
    extern.initKernel(kernel)
    extern.initShell(shell)
    return extern


def main():
    """لایه اکسترنالی دارم روی شل بنا شده و شل روی کرنل بنا شده
    """
    from client import ClientKernel
    kernel = ClientKernel.init()
    """کرنل رو از جنس کلاینت کرنل بساز
    """
    from client import ClientPcShell
    shell = ClientPcShell.init(kernel)
    """شا رو از جنس پی سی شل بساز و اینیتش کن
    """
    extern = init(kernel, shell)
    """و خودت بعنوان یه لایه اکسترنال بیا اینیت شو با کرنل و شلی که ساختم 
    و شلمو میتونستم متفاوت بزارم بجای پی سی شل بیام دامی شل بزارم
    """
    kernel.start()
    extern.start()
    shell.start()
    """یو ای من میاد بالا و اکسترن هم لستن کرده روی بلوتوث و کرنلم استارت کرده و خلاصه ارتباط سریالشو شروع کرده
    """

if __name__ == "__main__":
    main()

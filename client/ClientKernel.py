def init():
    from client.kernel.Ini import Ini
    from Globals import ini
    ini.wrap(Ini())

    from client.kernel.Interface import Interface
    """Seriyal door"""
    from Globals import interface
    """frame Mode"""
    kernel = Interface()
    interface.register(kernel)
    """frame mode"""
    return kernel


def main():
    kernel = init()
    kernel.start()
    input("")


if __name__ == "__main__":
    main()

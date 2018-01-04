class Color:
    GREY = '\033[90m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    BEIGE = '\033[96m'
    WHITE = '\033[97m'
    END = '\033[0m'

    @classmethod
    def grey(cls, s, **kwargs):
        print(cls.GREY + s + cls.END, **kwargs)

    @classmethod
    def red(cls, s, **kwargs):
        print(cls.RED + s + cls.END, **kwargs)

    @classmethod
    def green(cls, s, **kwargs):
        print(cls.GREEN + s + cls.END, **kwargs)

    @classmethod
    def yellow(cls, s, **kwargs):
        print(cls.YELLOW + s + cls.END, **kwargs)

    @classmethod
    def blue(cls, s, **kwargs):
        print(cls.BLUE + s + cls.END, **kwargs)

    @classmethod
    def purple(cls, s, **kwargs):
        print(cls.PURPLE + s + cls.END, **kwargs)

    @classmethod
    def beige(cls, s, **kwargs):
        print(cls.BEIGE + s + cls.END, **kwargs)

    @classmethod
    def white(cls, s, **kwargs):
        print(cls.WHITE + s + cls.END, **kwargs)

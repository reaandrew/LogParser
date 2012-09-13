class Something:

    def __init__(self):
        self.items = []
        self.items.append(lambda : getattr(self,"do_a")())
        self.items.append(lambda : getattr(self,"do_b")())

    def do_a(self):
        print("1")

    def do_b(self):
        print("2")

    def go(self):
        for i in self.items:
            i()

Something().go()

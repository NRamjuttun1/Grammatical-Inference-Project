def colourNode(Node):

    def __init__(self, iid):
        super().__init__(self, iid)
        self.colour = False

    def promote(self):
        self.colour = True

    def checkLevel(self):
        return self.colour

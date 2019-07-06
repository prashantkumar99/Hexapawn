from Player import Player
class Human(Player):
    def __init__(self, name):
        Player.__init__(self, name)

    def readMoveCoordinates(self):
        print("Playing:", self.name)
        print("Select Pawn:-")
        pawn = self.readCoordinates()
        print("Select Position to move to:-")
        target = self.readCoordinates()

        return (pawn[0], pawn[1], target[0], target[1])


    def readCoordinates(self):
        return (int(input("Row: ")), int(input("Column: ")))

    def result(self, won):
        pass
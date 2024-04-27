class Player:

    def __init__(self, num) -> None:
        self.ai = False
        self.name = f"Player {num}"
        self.color = "w" if num == 0 else "b"
        


        
class Match:


    def __init__(self,
                 player1,
                 player2,
                 player1_score=0,
                 player2_score=0,
                 winner=None,
                 is_finished=False,):
        self.player1 = player1
        self.player1_score = player1_score
        self.player2 = player2
        self.player2_score = player2_score
        self.winner = winner
        self.is_finished = is_finished

    def __repr__(self):
        return f"{self.player1} vs {self.player2}"

    def set_result(self, winner):
        if winner == 'player1' :
            self.is_finished = True
            self.player1_score = 1
            self.player2_score = 0
        elif winner == 'player2':
            self.is_finished = True
            self.player1_score = 0
            self.player2_score = 1
        elif winner == 'draw':
            self.player1_score = 0.5
            self.player2_score = 0.5
        else:
            raise ValueError("winner doit être 'player1', 'player2' ou 'draw'")

        self.is_finished = True
        self.winner = winner

    def to_tuple(self):
        return ([self.player1, self.player1_score],
                [self.player2, self.player2_score])

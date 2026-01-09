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
        return f'[  {self.player1.firstname}  ] VS [  {self.player2.firstname}  ]'

    def set_result(self, winner):
        if winner == '1':
            self.is_finished = True
            self.player1_score = 1
            self.player2_score = 0
        elif winner == '2':
            self.is_finished = True
            self.player1_score = 0
            self.player2_score = 1
        elif winner == '3':
            self.player1_score = 0.5
            self.player2_score = 0.5
        else:
            raise ValueError("Veuillez selectionner un des choix ci-dessus !\n")

        self.is_finished = True
        self.winner = winner

    def to_tuple(self):
        return ([self.player1, self.player1_score],
                [self.player2, self.player2_score])

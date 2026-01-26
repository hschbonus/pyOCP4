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

    def to_dict(self):
        match_dict = {
            "player1": self.player1.national_id,
            "player2": self.player2.national_id,
            "player1_score": self.player1_score,
            "player2_score": self.player2_score
        }
        return match_dict

    @classmethod
    def from_dict(cls, match_dict):
        match = cls(
            player1=match_dict["player1"],
            player2=match_dict["player2"],
            player1_score=match_dict["player1_score"],
            player2_score=match_dict["player2_score"]
        )
        return match

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

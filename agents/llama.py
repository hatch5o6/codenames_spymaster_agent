from base.assoc import Assoc
from base.constants import Team
from base.spymaster import BaseSpymaster
from agents.prompt_llama import LlamaSpymaster



class MyAssoc(Assoc):
    def __init__(self):
        super().__init__()
        # Initialize your model/embedding here

    def getAssocs(self, pos, neg, topn):
        # Implement your word association logic
        pass

    def preprocess(self, w):
        # Implement any word preprocessing
        pass


class MySpymaster(BaseSpymaster):
    def __init__(self, assoc):
        super().__init__(assoc)
        self.llama_spymaster = LlamaSpymaster(model_id="llama3.1-8b")

    def makeClue(self, board, team: Team):
        """
        Generate a clue for your team.

        Args:
            board: Dictionary with keys 'R' (red), 'U' (blue), 'N' (neutral), 'A'
                (assassin)
            team: Team.RED or Team.BLUE indicating your team

        Returns:
            tuple: ((clue_word, number_of_words), debug_info)
        """
        good_words = board["U" if team == Team.BLUE else "R"]
        bad_words = board["R" if team == Team.BLUE else "U"] 
        bad_words += board["N"] + board["A"]

        print("GOOD WORDS", len(good_words))
        print(good_words)
        print("BAD_WORDS", len(bad_words))
        print(bad_words)

        try:
            response = self.llama_spymaster.make_clue(good_words=good_words, bad_words=bad_words)
            clue = response["clue"]
            num_words = len(response["selected_words"])
            debug_info = "passed"
        except Exception as e:
            clue = "<FAIL>"
            num_words = 0
            debug_info = e

        return ((clue, num_words), debug_info)




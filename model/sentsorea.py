import json
class sentsorea():
    sents_id = 0
    sents_izen = ""
    sents_mota = ""
    sents_desk = ""

    # Array baino, tuple-ak dira... en fin
    def __init__(self, sentsDatuArray):
        self.sents_id = sentsDatuArray[0]
        self.sents_izen = sentsDatuArray[1]
        self.sents_mota = sentsDatuArray[2]
        self.sents_desk = sentsDatuArray[3]

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)
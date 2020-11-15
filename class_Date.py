class Date:
    def __init__(self, question, answer1, check_for_db):
        self.question = question
        self.db = {answer1: check_for_db}

    def add_answer(self, key_for_db, word):
        self.db[key_for_db] = word

    def get_db(self):
        return self.db

    def change(self, key_for_db, word_for_db):
        self.db[key_for_db] = word_for_db

    def tail(self):
        print("Question: ", self.question)
        print("Answer: ", self.db)

    def to_txt(self, filename, iteration):
        with open(filename, 'a', encoding='utf-8') as file:
            words = ''
            for key in self.db:
                if self.db[key] == True:
                    words += 'Question {}: '.format(iteration) + self.question + '\n' + 'Ответ: ' + key + '\n\n'
                    file.write(words)
                    return 0
                else:
                    return 1

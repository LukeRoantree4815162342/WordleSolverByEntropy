from string import ascii_lowercase as asc_L
from numpy import log2 as shan_l2, mean, std


class WordleSolver():
    def __init__(self, strategy=None):
        self.iteration_count = 0
        self.unknown_letters = 5
        self.past_guesses = []
        self.past_results = []
        self.valid_words = []
        self.last_valid_words = []
        with open("WORDLE.txt", 'r') as f:
            for w in f.readlines():
                self.valid_words.append(w.strip('\t').strip('\n'))
        self.freqs = {letter: self.__get_freqs(letter) for letter in asc_L}
        self.rules = []
        if strategy is None:
            self.strategy = self.__strategy_minimise_entropy
        else:
            self.strategy = strategy
    
    def __get_freqs(self, letter):
        return ''.join(self.valid_words).count(letter)/(5*len(self.valid_words))
    
    @staticmethod
    def __strategy_minimise_entropy(solver, word):
        return -sum([solver.freqs[letter]*shan_l2(solver.freqs[letter]) for letter in set(word)])
    
    def __score(self, word):
        return self.strategy(self,word)
    
    def guess(self, n_top_guesses=1):
        rankings = {word:self.__score(word) for word in self.valid_words}
        return [(k,v) for k, v in sorted(rankings.items(), key=lambda item: item[1], reverse=True)[:n_top_guesses]]
        
    def __rule_map(self, position, letter, result, is_first):
        if result == 'g':
            rule_pos = lambda w: w[position]==letter
        elif (result == 'b'):
            if is_first:
                rule_pos = lambda w: letter not in w
            else:
                rule_pos = lambda w: True
        else:
            rule_pos = lambda w: ((letter in w) and (w[position] != letter))
        return rule_pos
        
    def add_rule(self, guess, results):
        self.past_guesses.append(guess)
        self.past_results.append(results)
        self.iteration_count += 1
        self.unknown_letters = ''.join(results).count('b')
        is_first = [True if (guess[:i].count(l)==0) else False for i,l in enumerate(guess)]
        rule_subset = [self.__rule_map(i,guess[i],results[i], is_first[i]) for i in range(5)]
        new_rule = lambda w: all([subrule(w) for subrule in rule_subset])
        self.rules.append(new_rule)
        self.rules.append(lambda w: w != guess)
        self.__update_valid_words()
    
    def __update_valid_words(self):
        new_valid_words = [word for word in self.valid_words if all([rule(word) for rule in self.rules])]
        self.last_valid_words = self.valid_words.copy()
        self.valid_words = new_valid_words
        try:
            self.freqs = {letter: self.__get_freqs(letter) for letter in asc_L}
        except ZeroDivisionError as e:
            pass


def test_strategy(strategy=None, n_words=250):
    from random import shuffle
    from tqdm import tqdm
    wordlist = []
    with open("WORDLE.txt", 'r') as f:
        for w in f.readlines():
            wordlist.append(w.strip('\t').strip('\n'))
    guess_counts = []
    shuffle(wordlist)
    for w in tqdm(wordlist[:n_words]):
        solver = WordleSolver(strategy=strategy)
        guess_counts.append(autoplay(solver,w))
    wins = [1 if gc <=6 else 0 for gc in guess_counts]
    return mean(guess_counts), std(guess_counts), sum(wins)/n_words

def autoplay(solver, word, pair=None, count=1):
    if pair is not None:
        try:
            solver.add_rule(pair[0],pair[1])
        except ZeroDivisionError as e:
            print(word, pair)
            print(e)
            exit
    guess = solver.guess()[0][0]
    word_letter_count =  {l:word.count(l) for l in asc_L}
    guess_letter_count = {l:0 for l in asc_L}

    result = ['b']*5
    for key,letter in enumerate(guess):
        if word[key] == letter:
            result[key] = 'g'
    for key,letter in enumerate(guess):
        guess_letter_count[letter] += 1
        special_case = guess_letter_count[letter] <= word_letter_count[letter]
        conditions = ((word[key] != letter),
                      (letter in word),
                      (result[key] != 'g'),
                      (special_case)
                     )
        if all(conditions):
            result[key] = 'y'
        
    if result == ['g']*5:
        return count
    else:
        return autoplay(solver,word,pair=(guess,result),count=count+1)
    


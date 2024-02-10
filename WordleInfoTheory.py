from string import ascii_lowercase as asc_L
from numpy import log2 as shan_l2


class WordleSolver():
    def __init__(self, strategy=None):
        self.valid_words = []
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
    
    def __strategy_minimise_entropy(self, word):
        return -sum([self.freqs[letter]*shan_l2(self.freqs[letter]) for letter in set(word)])
    
    def __score(self, word):
        return self.strategy(word)
    
    def guess(self, n_top_guesses=1):
        rankings = {word:self.__score(word) for word in self.valid_words}
        return {k: v for k, v in sorted(rankings.items(), key=lambda item: item[1], reverse=True)[:n_top_guesses]}
        
    def __rule_map(self, position, letter, result):
        if result == 'g':
            rule_pos = lambda w: w[position]==letter
        elif result == 'b':
            rule_pos = lambda w: letter not in w
        else:
            rule_pos = lambda w: ((letter in w) and (w[position] != letter))
        return rule_pos
        
    def add_rule(self, guess, results):
        rule_subset = [self.__rule_map(i,guess[i],results[i]) for i in range(5)]
        new_rule = lambda w: all([subrule(w) for subrule in rule_subset])
        self.rules.append(new_rule)
        self.__update_valid_words()
    
    def __update_valid_words(self):
        new_valid_words = [word for word in self.valid_words if all([rule(word) for rule in self.rules])]
        self.valid_words = new_valid_words
        self.freqs = {letter: self.__get_freqs(letter) for letter in asc_L}
        

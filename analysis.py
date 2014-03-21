from __builtin__ import len
import json as js
from sys import maxint

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', "'", ' ', ',', '.', ';', ':', '?', '!', '(', ')', '-', "@", '"', '#']

def analyze_text(text, order, skip):
    """Returns two-dimensional array with characters 
    and their frequencies for a single text"""
    return analyze_text_loop_ready(text, order, skip, None)

def analyze_text_loop_ready(text, order, skip, char_analysis):
    """Returns two-dimensional array with characters 
    and their frequencies for a single text. This function
    can be used to analyze a large text in chunks or mutiple
    texts sequentially by updating char_analysis in every
    iteration."""
    
    
    text = text.lower()
    
    if(char_analysis is None):
        characters = []
        frequencies = []
        if(not skip):
            if(order == 1):
                characters = alphabet
                for i in range(0, len(alphabet)):
                    frequencies.append(0)
            elif(order == 2):
                for i in range(0, len(alphabet)):
                    for j in range(0, len(alphabet)):
                        characters.append(alphabet[i] + alphabet[j])
                        frequencies.append(0)
            elif(order == 3):
                for i in range(0, len(alphabet)):
                    for j in range(0, len(alphabet)):
                        for k in range(0, len(alphabet)):
                            characters.append(alphabet[i] + alphabet[j] + alphabet[k])
                            frequencies.append(0)
    else:
        characters = char_analysis["characters"]
        frequencies = char_analysis["frequencies"]
    
    if(order == 1):
        for i in range(0, len(text)):
            if text[i] in alphabet:
                if text[i] in characters:
                    frequencies[characters.index(text[i])] += 1
                else:
                    characters.append(text[i])
                    frequencies.append(1)
    elif (order == 2):
        duo = ""
        for i in range(0, len(text) - 1):
            if (text[i] in alphabet) and (text[i+1] in alphabet):
                duo = text[i] + text[i + 1]
                if duo in characters:
                    frequencies[characters.index(duo)] += 1
                else:
                    characters.append(duo)
                    frequencies.append(1)    
    elif (order == 3):
        trio = ""
        for i in range(0, len(text) - 2):
            if (text[i] in alphabet) and (text[i+1] in alphabet) and (text[i+2] in alphabet):            
                trio = text[i] + text[i + 1] + text[i + 2]
                if trio in characters:
                    frequencies[characters.index(trio)] += 1
                else:
                    characters.append(trio)
                    frequencies.append(1)
        

    return { "characters": characters, "frequencies": frequencies }


def initialize_third_order_matrix():
    """Initializes a third-order matrix [2x64000]."""
    
    characters = []
    frequencies = []
    
    for i in range(0, len(alphabet)):
        for j in range(0, len(alphabet)):
            for k in range(0, len(alphabet)):
                characters.append(alphabet[i] + alphabet[j] + alphabet[k])
                frequencies.append(0)
                
    return { "characters": characters, "frequencies": frequencies }
    
    
def analyze_text_third_order_responsive(chunk, char_analysis):
    """Returns a two-dimensional array with characters and their frequencies.
    This method is meant to be hosted on a server with a request timeout in place,
    since third-order computation can take a considerable amount of time and in order
    to keep the request alive, the input text is split up into smaller chunks
    and after each chunk the function sends an empty string to notify that it's still
    working."""
    
    characters = char_analysis["characters"]
    frequencies = char_analysis["frequencies"]
    chunk = chunk.lower()
    trio = ""
    
    for i in range(0, len(chunk) - 2):
        if (chunk[i] in alphabet) and (chunk[i+1] in alphabet) and (chunk[i+2] in alphabet):            
            trio = chunk[i] + chunk[i + 1] + chunk[i + 2]
            if trio in characters:
                frequencies[characters.index(trio)] += 1
            else:
                characters.append(trio)
                frequencies.append(1)

    return { "characters": characters, "frequencies": frequencies }

def compute_most_probable_digraph(so_char_analysis, start):
    """Recursively computes the most probable digraph given a second-order
    correlation matrix as input and a character to start with.
    When the successor of the start character is found all possible
    successors of this character are removed in order to avoid loops."""
    
    characters = so_char_analysis["characters"]
    frequencies = so_char_analysis["frequencies"]
    
    if len(characters) == 0:
        return start
    else:
        current_char = start
        next_char = ""
        next_max_freq = 0
        remove_list = []
        
        for i in range (0, len(characters)):
            if characters[i].startswith(current_char):
                remove_list.append(characters[i])
                if frequencies[i] > next_max_freq:
                    next_max_freq = frequencies[i]
                    next_char = characters[i][1]
        
        for i in range(0, len(remove_list)):
            index = characters.index(remove_list[i])
            characters.remove(characters[index])
            frequencies.remove(frequencies[index])
        
        return start + compute_most_probable_digraph({ "characters": characters, "frequencies": frequencies }, next_char)
    
def author_attribution(text):
    """First, computes the second-order matrix (relative frequencies) of the input text.
    Second, computes the sum of the quadratic deviations of the input text against each author in the database."""
    
    text_char_analysis = analyze_text(text, 2, False)
    freqs_text = abs_to_rel_freq(text_char_analysis, 2)
    
    authors = open("res/authors/index").readlines()
    best_match_sum = maxint
    best_match_author = ""
    for author in authors:
        author = author.replace("\n", "")
        current_sum = 0
        author_char_analysis = js.load(open("res/authors/" + author))
        freqs_author = author_char_analysis["frequencies"] 
        for i in range(0, len(freqs_author)):
            current_sum += (freqs_text[i] - freqs_author[i]) ** 2
        
        print "Text matches " + author + " by " + str(current_sum)
        
        if current_sum < best_match_sum:
            best_match_sum = current_sum
            best_match_author = author
            
    return best_match_author
    
    
def abs_to_rel_freq(mat_abs, order):
    """Given an object with attributes 'frequencies' (**absolute** frequencies) and 'characters'
    this function returns the **relative** frequencies."""
    
    given_chars = mat_abs["characters"]
    abs_freqs = mat_abs["frequencies"]
    rel_freqs = []
    
    if (order == 1):
        # TODO
        pass
    elif (order == 2):
        
        for search_char in alphabet:
            total_freq = 0
            for given_char in given_chars:
                if(given_char.startswith(search_char)):
                    total_freq += abs_freqs[given_chars.index(given_char)]
            for given_char in given_chars:
                if(given_char.startswith(search_char)):
                    if total_freq > 0:
                        rel_freqs.append((0.0 + abs_freqs[given_chars.index(given_char)]) / total_freq)
                    else:
                        rel_freqs.append(0)
    
    elif (order == 3):
        # TODO
        pass

    return rel_freqs
from __builtin__ import len, sum
import json as js
from sys import maxint

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', "'", ' ', ',', '.', ';', ':', '?', '!', '(', ')', '-', "@", '"', '#']
special_characters = ["'", ' ', ',', '.', ';', ':', '?', '!', '(', ')', '-', "@", '"', '#']

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
    """Given an nth-order matrix which contains a text character analysis as 
    an object with attributes 'frequencies' (**absolute** frequencies) and 'characters'
    this function returns the corresponding **relative** frequencies."""
    
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

def compute_n_gram_words(n, text, n_gram=None):
    """Returns *n*-grams of a given *text* source
    
    :param n: the size of the contiguous sequence of words
    :param text: the text source to be analyzed
    :param n_gram: takes an existing n_gram as input, which will be extended
    :returns: an object n_gram: { 'sequences': [*top **m** **n**-grams*], 'frequencies': [*the frequencies of n-grams*] }
    """
    
    if n_gram == None:
        n_gram = { "sequences": [], "frequencies": [] }
    
    if n == 1:
        total_words = 0
        for word in text.split(" "):
            total_words += 1
            for special_char in special_characters:
                word = word.replace(special_char, "")
            word = word.lower()
            if word not in n_gram["sequences"]:
                n_gram["sequences"].append(word)
                n_gram["frequencies"].append(1)
            else:
                n_gram["frequencies"][n_gram["sequences"].index(word)] += 1
        for i in range(0,len(n_gram["frequencies"])):
            n_gram["frequencies"][i] = n_gram["frequencies"][i] / (0.0 + total_words)
    else:
        #TODO
        pass
    
    return n_gram

def get_top_m_n_grams(m, n_gram):
    """Reduces a list of n_grams with word sequences and their frequencies
    to the top *m* ones.
    
    :param m: amount of sequences and corresponding frequencies to return
    :param n_gram: an object with attribues 'sequencies' and (index-wise) corresponding 'frequencies'
    :returns: The top *m* sequences (and their frequencies) of the input n-gram in a descending order.
    """
    
    top_m_freqs = [0]
    top_m_index = [0]
    for seq in n_gram["sequences"]:
        freq = n_gram["frequencies"][n_gram["sequences"].index(seq)]
        for i in range(0, len(top_m_freqs)):
            if freq > top_m_freqs[i]:
                top_m_freqs.insert(i, freq)
                top_m_index.insert(i, n_gram["sequences"].index(seq))
                if len(top_m_freqs) > m:
                    top_m_freqs.pop()
                    top_m_index.pop()
                break
            
    result = { "sequences": [], "frequencies": [] }
    
    for index in top_m_index:
        result["sequences"].append(n_gram["sequences"][index])
        result["frequencies"].append(n_gram["frequencies"][index])
        
    return result

def filter_sequences(genres):
    """Given a set of objects (genres) which have n-gram *sequences* and
    their *frequencies* as attributes, this function returns this set of
    objects, where for every object (genre) the sequences, which occur
    not uniquely in an object (genre), are removed.
    
    :param genres: a set of objects (genres) which have n-gram *sequences* and
    their *frequencies* as attributes
    :returns: this set of objects, where for every object (genre) the sequences, which occur
    not uniquely in an object (genre), are removed
    """
    
    seqs_master_list = []
    for genre in genres:
        for seq in genre["1-gram"]["sequences"]:
            found_seq = False
            for seq_master in seqs_master_list:
                if seq_master["seq"] == seq:
                    seq_master["freq"] += 1
                    found_seq = True
            if not found_seq:
                seqs_master_list.append({ "seq": seq, "freq": 1 })
    
    unique_seqs = []
    for seq in seqs_master_list:
        if seq["freq"] == 1:
            unique_seqs.append(seq["seq"])
    
    
    for genre in genres:
        temp_list = { "sequences": [], "frequencies": [] }
        for i in range(0,len(genre["1-gram"]["sequences"])):
            seq = genre["1-gram"]["sequences"][i]
            freq = genre["1-gram"]["frequencies"][i]
            if seq in unique_seqs:
                temp_list["sequences"].append(seq)
                temp_list["frequencies"].append(freq)
        genre["1-gram-unique"] = temp_list
        
    return genres

def genre_attribution(text):
    """This function computes 1-grams of a given input text and compares it
    to 1-grams of known genres from the database. It returns the genre
    with the highest match
    
    :param text: the input text
    :returns: The genre from the database which has the highest similarity in word
    use with the input text.    
    """
    
    n_gram = compute_n_gram_words(1, text)
    seqs = n_gram["sequences"]
    freqs = n_gram["frequencies"]
    
    genre_index = open("res/genres/index").readlines()
    print "Genre index: " + ','.join(genre_index)
    
    diff_best_match = maxint
    best_match = ""
    for current_genre in genre_index:
        diff = 0
        n_gram_genre = js.load(open("res/genres/" + current_genre.replace("\n","")))
        seqs_genre = n_gram_genre["sequences"]
        freqs_genre = n_gram_genre["frequencies"]
        for i in range(0, len(seqs_genre)):
            if seqs_genre[i] in seqs:
                index = seqs.index(seqs_genre[i])
                diff += (freqs_genre[i] - freqs[index]) ** 2 
            else:
                diff += (freqs_genre[i]) ** 2
        print "Diff for " + current_genre + ": " + str(diff)
        if diff < diff_best_match:
            diff_best_match = diff
            best_match = current_genre
            print "Best match set to: " + str(best_match)
    
    return best_match
    
def compute_diff(from_book, to_book):
    
    from_seqs = from_book["n-gram"]["sequences"]
    from_freqs = from_book["n-gram"]["frequencies"]
    to_seqs = to_book["n-gram"]["sequences"]
    to_freqs = to_book["n-gram"]["frequencies"]
    
    diff = 0
    
    for i in range(0, len(from_seqs)):
        if from_seqs[i] in to_seqs:
            diff += (from_freqs[i] - to_freqs[to_seqs.index(from_seqs[i])]) ** 2
        else:
            diff += from_freqs[i] ** 2
    
    for i in range (0, len(to_seqs)):
        if to_seqs[i] not in from_seqs:
            diff += to_freqs[i] ** 2
            
    return diff
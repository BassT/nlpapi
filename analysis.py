from __builtin__ import len


alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', "'", ' ', ',', '.', ';', ':', '?', '!', '(', ')', '-', "@", '"', '#']

def analyze_text(text, order, skip):
    """Returns two-dimensional array with characters and their frequencies """
    
    text = text.lower()
    
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

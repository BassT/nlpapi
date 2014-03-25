from json import dumps, dump
import analysis
def set_up_author_attr_data():
    
    """Load all books"""
    catalog = { "distinct_authors": [], "books": [] }
    file_list = open("res/filenames.txt", "r")
    line = file_list.readline().rstrip("\n")
    while(line != ""):
        line = str(line).split(",")
        filename = line[0]
        author = line[1]
        catalog["books"].append({ "author": author, "filename": filename })
        if author not in catalog["distinct_authors"]:
            catalog["distinct_authors"].append(author)
        line = file_list.readline().rstrip("\n")
    
    print "The catalog: " + dumps(catalog)
    
    """Compute and save the second-order matrix 
    (absolute frequencies) for every distinct author"""
    for author in catalog["distinct_authors"]:
        print "START - Computing second-order matrix for " + author
        char_analysis = None
        for book in catalog["books"]:
            if book["author"] == author:
                print "Found a book written by " + author + ": " + book["filename"]
                text = open("res/" + book["filename"]).read().replace('\n', '')
                char_analysis = analysis.analyze_text_loop_ready(text, 2, False, char_analysis)
        char_analysis["frequencies"] = analysis.abs_to_rel_freq(char_analysis, 2)
        with open("res/authors/" + author.replace(" ", "_"), "w") as outfile:
            dump(char_analysis, outfile)
        print "END - Computing second-order matrix for " + author
        
def set_up_genre_data():
    
    """Load all books"""
    genres = []
    file_list = open("res/filenames.txt", "r")
    line = file_list.readline().rstrip("\n")
    while(line != ""):
        splits = str(line).split(",")
        filename = splits[0]
        for i in range(2, len(splits)):
            text_genre = splits[i].strip().lower()
            found_genre = False
            for genre in genres:
                if genre["name"] == text_genre:
                    genre["books"].append(filename)
                    found_genre = True
            if not found_genre:
                genres.append( { "name": text_genre, "books": [filename]} )
        line = file_list.readline().rstrip("\n")
        
    """Filter out genres which only have 1 book"""
    significant_genres_list = []
    for i in range(0, len(genres)):
        if len(genres[i]["books"]) > 1:
            significant_genres_list.append(i)
    temp_list = []
    for index in significant_genres_list:
        temp_list.append(genres[index])
    genres = temp_list
    
    """Compute 1-gram for each genre"""
    for i in range(0, len(genres)):
        print "\nComputing top 50 1-gram for: " + genres[i]["name"]
        n_gram = None
        for j in range(0, len(genres[i]["books"])):
            print "Analyzing text from " + genres[i]["books"][j] 
            text = open("res/" + genres[i]["books"][j]).read().replace("\r\n", " ").replace("\r"," ").replace("\n"," ")
            n_gram = analysis.compute_n_gram_words(1, text, n_gram)
        # genres[i]["1-gram"] = n_gram
        genres[i]["1-gram"] = analysis.get_top_m_n_grams(500, n_gram)
        print "Computed " + dumps(genres[i]["1-gram"], sort_keys=True, indent=4, separators=(',', ': ')) 
    
    """Filter sequences, which occur in all genres"""
    
    genres = analysis.filter_sequences(genres)    
    
    """Store n-grams for each genre"""
    for genre in genres:
        with open("res/genres/" + genre["name"].replace(" ", "_"), "w") as outfile:
            dump(genre["1-gram"], outfile)
        with open("res/genres/" + genre["name"].replace(" ", "_") + "-unique", "w") as outfile:
            dump(genre["1-gram-unique"], outfile)
    
    print "The catalog: " + dumps(genres, sort_keys=True, indent=4, separators=(',', ': '))
    
def book_to_book_corr():
    
    file_list = open("res/filenames.txt").readlines()
    books = []
    
    diffs = []
    
    for filename in file_list:
        filename = filename.split(",")[0]
        print "Loading " + filename
        text = open("res/" + filename).read().replace("/r/n", " ").replace("/n", " ").replace("/r", " ")
        n_gram = analysis.compute_n_gram_words(1, text)
        books.append( { "title": filename.split(".")[0], "n-gram": n_gram } )
    for from_book in books:
        print "Comparing " + from_book["title"] + " to ..."
        current_diffs = []
        for to_book in books:
            print "... " + to_book["title"]
            current_diffs.append( { "title": to_book["title"], "diff": analysis.compute_diff(from_book, to_book) })
        diffs.append( { "title": from_book["title"], "diffs": current_diffs } )
        
    print "Correlations: " + dumps(diffs, sort_keys=True, indent=4, separators=(",", ": "))
    
    with open("res/book-to-book", "w") as outfile:
        dump(diffs, outfile, sort_keys=True, indent=4, separators=(",", ": "))

book_to_book_corr()
        
        
    
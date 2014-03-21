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
    
    """Compute top 50 3-gram for each genre"""
    for i in range(0, len(genres)):
        for j in range(0, len(genres[i]["books"])):
            genres[i]["3-gram"] = analysis.compute_n_gram_words(50, 3, genres[i]["books"][j], genres[i]["3-gram"])
         
    
    for genre in genres:
        with open("res/genres/" + genre["name"].replace(" ", "_"), "w") as outfile:
            dump(genre["books"], outfile)
    
    print "The catalog: " + dumps(genres, sort_keys=True, indent=4, separators=(',', ': '))
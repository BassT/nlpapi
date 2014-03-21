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
        
set_up_author_attr_data()
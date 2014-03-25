import analysis
from analysis import compute_n_gram_words, get_top_m_n_grams
import json as js


#------------------------------------------ def test_analyze_text_first_order():
    #----- """Tests analysis.analyze_text function with first order analysis."""
#------------------------------------------------------------------------------ 
    #--------------------------------------------------- text = "Some test text"
#------------------------------------------------------------------------------ 
    #---------------------------- # Testing first order with *skip* set to True.
    #----------------------------- result = analysis.analyze_text(text, 1, True)
    #------------------------------------- assert len(result["characters"]) == 7
    #------------------------------------- assert result["characters"][0] == "s"
    #------------------------------------ assert len(result["frequencies"]) == 7
    #-------------------------------------- assert result["frequencies"][3] == 3
#------------------------------------------------------------------------------ 
    #--------------------------- # Testing first order with *skip* set to False.
    #---------------------------- result = analysis.analyze_text(text, 1, False)
    #------------------------------------ assert len(result["characters"]) == 40
    #------------------------------------- assert result["characters"][0] == "a"
    #----------------------------------- assert len(result["frequencies"]) == 40
    #-------------------------------------- assert result["frequencies"][3] == 0
    #-------------------------------------- assert result["frequencies"][4] == 3
#------------------------------------------------------------------------------ 
#------------------------------- def test_analyze_text_loop_ready_first_order():
#------------------------------------------------------------------------------ 
    #------------------------------------------- text = ["Some", "test", "text"]
#------------------------------------------------------------------------------ 
    #---------------------------- # Testing first order with *skip* set to True.
    #------------------------------------------------------------- result = None
    #--------------------------------------------- for i in range(0, len(text)):
        #--- result = analysis.analyze_text_loop_ready(text[i], 1, True, result)
    #------------------------------------- assert len(result["characters"]) == 6
    #------------------------------------- assert result["characters"][0] == "s"
    #------------------------------------ assert len(result["frequencies"]) == 6
    #-------------------------------------- assert result["frequencies"][3] == 3
#------------------------------------------------------------------------------ 
    #--------------------------- # Testing first order with *skip* set to False.
    #------------------------------------------------------------- result = None
    #--------------------------------------------- for i in range(0, len(text)):
        #-- result = analysis.analyze_text_loop_ready(text[i], 1, False, result)
    #------------------------------------ assert len(result["characters"]) == 40
    #------------------------------------- assert result["characters"][0] == "a"
    #----------------------------------- assert len(result["frequencies"]) == 40
    #-------------------------------------- assert result["frequencies"][3] == 0
    #-------------------------------------- assert result["frequencies"][4] == 3
#------------------------------------------------------------------------------ 
#----------------------------------------- def test_analyze_text_second_order():
    #---- """Tests analysis.analyze_text function with second order analysis."""
#------------------------------------------------------------------------------ 
    #--------------------------------------------------------- text = "ab ab ac"
#------------------------------------------------------------------------------ 
    #--------------------------- # Testing second order with *skip* set to True.
    #----------------------------- result = analysis.analyze_text(text, 2, True)
    #-------------------------------------------------------------- print result
    #------------------------------------- assert len(result["characters"]) == 4
    #------------------------------------ assert len(result["frequencies"]) == 4
    #------------------------------------ assert result["characters"][0] == "ab"
    #------------------------------------- assert result["frequencies"][0] ==  2
    #------------------------------------ assert result["characters"][1] == "b "
    #------------------------------------- assert result["frequencies"][1] ==  2
    #------------------------------------ assert result["characters"][2] == " a"
    #------------------------------------- assert result["frequencies"][2] ==  2
    #------------------------------------ assert result["characters"][3] == "ac"
    #------------------------------------- assert result["frequencies"][3] ==  1
#------------------------------------------------------------------------------ 
    #-------------------------- # Testing second order with *skip* set to False.
    #---------------------------- result = analysis.analyze_text(text, 2, False)
    #-------------------------------------------------------------- print result
    #--------------------------------- assert len(result["characters"]) == 40**2
    #-------------------------------- assert len(result["frequencies"]) == 40**2
    #------------------------------------ assert result["characters"][0] == "aa"
    #------------------------------------- assert result["frequencies"][0] ==  0
    #------------------------------------ assert result["characters"][1] == "ab"
    #------------------------------------- assert result["frequencies"][1] ==  2
    #------------------------------------ assert result["characters"][2] == "ac"
    #------------------------------------- assert result["frequencies"][2] ==  1
#------------------------------------------------------------------------------ 
#------------------------------ def test_analyze_text_loop_ready_second_order():
#------------------------------------------------------------------------------ 
    #--------------------------------------------------- text = ["ab","ab","ac"]
#------------------------------------------------------------------------------ 
    #---------------------------- # Testing first order with *skip* set to True.
    #------------------------------------------------------------- result = None
    #--------------------------------------------- for i in range(0, len(text)):
        #--- result = analysis.analyze_text_loop_ready(text[i], 2, True, result)
    #------------------------------------- assert len(result["characters"]) == 2
    #------------------------------------ assert result["characters"][0] == "ab"
    #------------------------------------ assert len(result["frequencies"]) == 2
    #-------------------------------------- assert result["frequencies"][0] == 2
#------------------------------------------------------------------------------ 
    #--------------------------- # Testing first order with *skip* set to False.
    #------------------------------------------------------------- result = None
    #--------------------------------------------- for i in range(0, len(text)):
        #-- result = analysis.analyze_text_loop_ready(text[i], 2, False, result)
    #--------------------------------- assert len(result["characters"]) == 40**2
    #------------------------------------ assert result["characters"][1] == "ab"
    #-------------------------------- assert len(result["frequencies"]) == 40**2
    #-------------------------------------- assert result["frequencies"][0] == 0
    #-------------------------------------- assert result["frequencies"][1] == 2
    #-------------------------------------- assert result["frequencies"][2] == 1
#------------------------------------------------------------------------------ 
#------------------------------------------ def test_analyze_text_third_order():
    #----- """Tests analysis.analyze_text function with third order analysis."""
#------------------------------------------------------------------------------ 
    #--------------------------------------------------------- text = " abc abd"
#------------------------------------------------------------------------------ 
    #---------------------------- # Testing third order with *skip* set to True.
    #----------------------------- result = analysis.analyze_text(text, 3, True)
    #-------------------------------------------------------------- print result
    #------------------------------------- assert len(result["characters"]) == 5
    #------------------------------------ assert len(result["frequencies"]) == 5
    #----------------------------------- assert result["characters"][0] == " ab"
    #------------------------------------- assert result["frequencies"][0] ==  2
    #----------------------------------- assert result["characters"][1] == "abc"
    #------------------------------------- assert result["frequencies"][1] ==  1
    #----------------------------------- assert result["characters"][2] == "bc "
    #------------------------------------- assert result["frequencies"][2] ==  1
    #----------------------------------- assert result["characters"][3] == "c a"
    #------------------------------------- assert result["frequencies"][3] ==  1
    #----------------------------------- assert result["characters"][4] == "abd"
    #------------------------------------- assert result["frequencies"][4] ==  1
#------------------------------------------------------------------------------ 
    #------------------------------------------------------------- text = "aaab"
#------------------------------------------------------------------------------ 
    #---------------------------- # Testing third order with *skip* set to True.
    #---------------------------- result = analysis.analyze_text(text, 3, False)
    #-------------------------------------------------------------- print result
    #--------------------------------- assert len(result["characters"]) == 40**3
    #-------------------------------- assert len(result["frequencies"]) == 40**3
    #----------------------------------- assert result["characters"][0] == "aaa"
    #------------------------------------- assert result["frequencies"][0] ==  1
    #----------------------------------- assert result["characters"][1] == "aab"
    #------------------------------------- assert result["frequencies"][1] ==  1
    #----------------------------------- assert result["characters"][2] == "aac"
    #------------------------------------- assert result["frequencies"][2] ==  0
    #----------------------------------- assert result["characters"][3] == "aad"
    #------------------------------------- assert result["frequencies"][3] ==  0
    #----------------------------------- assert result["characters"][4] == "aae"
    #-------------------------------------- assert result["frequencies"][4] == 0
#------------------------------------------------------------------------------ 
#------------------------------------- def test_initialize_third_order_matrix():
    # """Test the initialize_third_order_matrix method of the analysis module."""
#------------------------------------------------------------------------------ 
    #------------------------- result = analysis.initialize_third_order_matrix()
    #--------------------------------- assert len(result["characters"]) == 40**3
    #-------------------------------- assert len(result["frequencies"]) == 40**3
#------------------------------------------------------------------------------ 
#------------------------------- def test_analyze_text_third_order_responsive():
    # """Test the analyze_text_third_order_responsive method of the analysis module."""
#------------------------------------------------------------------------------ 
    #------------------------------------------------------------- text = "aaab"
    #------------------ char_analysis = analysis.initialize_third_order_matrix()
    # char_analysis = analysis.analyze_text_third_order_responsive(text[0:3], char_analysis)
    # char_analysis = analysis.analyze_text_third_order_responsive(text[1:], char_analysis)
    #---------------------------- assert char_analysis["characters"][0] == "aaa"
    #---------------------------- assert char_analysis["characters"][1] == "aab"
    #------------------------------------- print char_analysis["frequencies"][0]
    #------------------------------- assert char_analysis["frequencies"][0] == 1
    #------------------------------- assert char_analysis["frequencies"][1] == 1
    #------------------------------- assert char_analysis["frequencies"][2] == 0
#------------------------------------------------------------------------------ 
#------------------------------------- def test_compute_most_probable_digraph():
#------------------------------------------------------------------------------ 
    # char_analysis = { "characters": ["ab", "bc", "bd", "cd"], "frequencies": [1, 2, 1, 1] }
    #------- result = analysis.compute_most_probable_digraph(char_analysis, "a")
    #--------------------------------------------------- assert result == "abcd"
#------------------------------------------------------------------------------ 
#------------------------------------------------ def test_author_attribution():
#------------------------------------------------------------------------------ 
    #--- text = open("res/legend_of_sleepy_hollow.txt").read().replace('\n', '')
    #----------- assert analysis.author_attribution(text) == "Washington_Irving"
    #-------- text = open("res/tarzan_of_the_apes.txt").read().replace('\n', '')
    #-------- assert analysis.author_attribution(text) == "Edgar_Rice_Burroughs"
    # text = open("res/adventures_of_huckleberry_finn1.txt").read().replace('\n', '')
    #------------------ assert analysis.author_attribution(text) == "Mark_Twain"
#------------------------------------------------------------------------------ 
#---------------------------------------------- def test_compute_n_gram_words():
#------------------------------------------------------------------------------ 
    #------------------------------------------------------ text = "Test 'text'"
    #---------------------------------------------- text2 = "More test text!!!!"
#------------------------------------------------------------------------------ 
    #------------------------------ n_gram = compute_n_gram_words(1, text, None)
    #------------------------------------ assert len(n_gram["frequencies"]) == 2
    #-------------------------------------- assert len(n_gram["sequences"]) == 2
    #----------------------------------- assert n_gram["sequences"][0] == "test"
    #----------------------------------- assert n_gram["sequences"][1] == "text"
    #------ assert n_gram["frequencies"][n_gram["sequences"].index("test")] == 1
    #------ assert n_gram["frequencies"][n_gram["sequences"].index("text")] == 1
    #--------------------------- n_gram = compute_n_gram_words(1, text2, n_gram)
    #------------------------------------ assert len(n_gram["frequencies"]) == 3
    #-------------------------------------- assert len(n_gram["sequences"]) == 3
    #----------------------------------- assert n_gram["sequences"][0] == "test"
    #----------------------------------- assert n_gram["sequences"][1] == "text"
    #----------------------------------- assert n_gram["sequences"][2] == "more"
    #------ assert n_gram["frequencies"][n_gram["sequences"].index("test")] == 2
    #------ assert n_gram["frequencies"][n_gram["sequences"].index("text")] == 2
    #------ assert n_gram["frequencies"][n_gram["sequences"].index("more")] == 1
#------------------------------------------------------------------------------ 
#------------------------------------------------- def test_get_top_m_n_grams():
#------------------------------------------------------------------------------ 
    #---- n_gram = { "sequences": ["test1", "test2", "test3", "test4", "test5"],
               #----------------------------------- "frequencies": [1,2,3,4,5] }
#------------------------------------------------------------------------------ 
    #------------------------------------- n_gram = get_top_m_n_grams(2, n_gram)
    #-------------------------------------- assert len(n_gram["sequences"]) == 2
    #------------------------------------ assert len(n_gram["frequencies"]) == 2
    #-------------------------------------- assert n_gram["frequencies"][0] == 5
    #-------------------------------------- assert n_gram["frequencies"][1] == 4
    #---------------------------------- assert n_gram["sequences"][1] == "test4"
    #---------------------------------- assert n_gram["sequences"][0] == "test5"
#------------------------------------------------------------------------------ 
#-------------------------------------------------- def test_filter_sequences():
#------------------------------------------------------------------------------ 
    #---------------------------------------------------------------- genres = [
              #--------------------------------------------------------------- {
               #--------------------------------------------- "name": "genre 1",
               #---------------------------------------------------- "1-gram": {
                          #------ "sequences": ["seq1", "seq2", "seq3", "seq4"],
                          #---------------------------- "frequencies": [1,2,3,4]
                          #--------------------------------------------------- }
               #------------------------------------------------------------- },
              #--------------------------------------------------------------- {
               #--------------------------------------------- "name": "genre 2",
               #---------------------------------------------------- "1-gram": {
                          #-------------- "sequences": ["seq1", "seq2", "seq5"],
                          #------------------------------ "frequencies": [1,2,5]
                          #--------------------------------------------------- }
               #-------------------------------------------------------------- }
               #-------------------------------------------------------------- ]
#------------------------------------------------------------------------------ 
    #-------------------------------- genres = analysis.filter_sequences(genres)
    #-- print js.dumps(genres, sort_keys=True, indent=4, separators=(',', ': '))
    #--------------------------------------------------- assert len(genres) == 2
#------------------------------------------------------------------------------ 
    #------------------------------------- assert genres[0]["name"] == "genre 1"
    #------------------ assert len(genres[0]["1-gram-unique"]["sequences"]) == 2
    #---------------- assert len(genres[0]["1-gram-unique"]["frequencies"]) == 2
    #--------------- assert genres[0]["1-gram-unique"]["sequences"][0] == "seq3"
    #--------------- assert genres[0]["1-gram-unique"]["sequences"][1] == "seq4"
    #------------------ assert genres[0]["1-gram-unique"]["frequencies"][0] == 3
    #------------------ assert genres[0]["1-gram-unique"]["frequencies"][1] == 4
#------------------------------------------------------------------------------ 
    #------------------------------------- assert genres[1]["name"] == "genre 2"
    #------------------ assert len(genres[1]["1-gram-unique"]["sequences"]) == 1
    #---------------- assert len(genres[1]["1-gram-unique"]["frequencies"]) == 1
    #--------------- assert genres[1]["1-gram-unique"]["sequences"][0] == "seq5"
    #------------------ assert genres[1]["1-gram-unique"]["frequencies"][0] == 5
#------------------------------------------------------------------------------ 
#------------------------------------------------- def test_genre_attribution():
#------------------------------------------------------------------------------ 
    # text = open("res/the_hound_of_the_baskervilles1.txt").read().replace("\r"," ").replace("\n"," ")
    # text2 = open("res/a_connecticut_yankee_in_king_arthur_s_court1.txt").read().replace("\r"," ").replace("\n"," ")
    # text3 = open("res/tale_of_2_cities.txt").read().replace("\r"," ").replace("\n"," ")
#------------------------------------------------------------------------------ 
    #---------------------------------- genre = analysis.genre_attribution(text)
    #------------------------------------------ print "Genre for text: " + genre
#------------------------------------------------------------------------------ 
    #-------------------------------- genre2 = analysis.genre_attribution(text2)
    #---------------------------------------- print "Genre for text2: " + genre2
#------------------------------------------------------------------------------ 
    #-------------------------------- genre3 = analysis.genre_attribution(text3)
    #---------------------------------------- print "Genre for text3: " + genre3
#------------------------------------------------------------------------------ 
    #------------------------------------- assert genre in ["detective fiction"]
    # assert genre2 in ["humor", "satire", "alternate history", "science fiction", "fantasy"]
    
def test_compute_diff():
    
    from_book = { "name": "from_book",
                  "n-gram": { "sequences": ["seq1", "seq2"],
                              "frequencies": [0.8, 0.2] 
                              } 
                 }
    
    to_book1 = { "name": "to_book1",
                  "n-gram": { "sequences": ["seq1", "seq2"],
                              "frequencies": [0.7, 0.3] 
                              } 
                 }
    
    to_book2 = { "name": "to_book2",
                  "n-gram": { "sequences": ["seq1", "seq3"],
                              "frequencies": [0.7, 0.3] 
                              } 
                 }
    
    to_book3 = { "name": "to_book3",
                  "n-gram": { "sequences": ["seq1", "seq2"],
                              "frequencies": [0.6, 0.4] 
                              } 
                 }
    
    assert analysis.compute_diff(from_book, from_book) == 0
    assert analysis.compute_diff(from_book, to_book1) < analysis.compute_diff(from_book, to_book2)
    assert analysis.compute_diff(from_book, to_book1) < analysis.compute_diff(from_book, to_book3)
    assert analysis.compute_diff(from_book, to_book3) < analysis.compute_diff(from_book, to_book2)
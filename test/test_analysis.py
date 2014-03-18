import analysis


def test_analyze_text_first_order():
    """Tests analysis.analyze_text function with first order analysis."""
    
    text = "Some test text"
    
    # Testing first order with *skip* set to True.
    result = analysis.analyze_text(text, 1, True)
    assert len(result["characters"]) == 7
    assert result["characters"][0] == "s"
    assert len(result["frequencies"]) == 7
    assert result["frequencies"][3] == 3
    
    # Testing first order with *skip* set to False.
    result = analysis.analyze_text(text, 1, False)
    assert len(result["characters"]) == 40
    assert result["characters"][0] == "a"
    assert len(result["frequencies"]) == 40
    assert result["frequencies"][3] == 0
    assert result["frequencies"][4] == 3

def test_analyze_text_second_order():
    """Tests analysis.analyze_text function with second order analysis."""
    
    text = "ab ab ac"
    
    # Testing second order with *skip* set to True.
    result = analysis.analyze_text(text, 2, True)
    print result
    assert len(result["characters"]) == 4
    assert len(result["frequencies"]) == 4
    assert result["characters"][0] == "ab"
    assert result["frequencies"][0] ==  2
    assert result["characters"][1] == "b "
    assert result["frequencies"][1] ==  2
    assert result["characters"][2] == " a"
    assert result["frequencies"][2] ==  2
    assert result["characters"][3] == "ac"
    assert result["frequencies"][3] ==  1
    
    # Testing second order with *skip* set to False.
    result = analysis.analyze_text(text, 2, False)
    print result
    assert len(result["characters"]) == 40**2
    assert len(result["frequencies"]) == 40**2
    assert result["characters"][0] == "aa"
    assert result["frequencies"][0] ==  0
    assert result["characters"][1] == "ab"
    assert result["frequencies"][1] ==  2
    assert result["characters"][2] == "ac"
    assert result["frequencies"][2] ==  1
    
def test_analyze_text_third_order():
    """Tests analysis.analyze_text function with third order analysis."""
    
    text = " abc abd"
    
    # Testing third order with *skip* set to True.
    result = analysis.analyze_text(text, 3, True)
    print result
    assert len(result["characters"]) == 5
    assert len(result["frequencies"]) == 5
    assert result["characters"][0] == " ab"
    assert result["frequencies"][0] ==  2
    assert result["characters"][1] == "abc"
    assert result["frequencies"][1] ==  1
    assert result["characters"][2] == "bc "
    assert result["frequencies"][2] ==  1
    assert result["characters"][3] == "c a"
    assert result["frequencies"][3] ==  1
    assert result["characters"][4] == "abd"
    assert result["frequencies"][4] ==  1
    
    text = "aaab"
    
    # Testing third order with *skip* set to True.
    result = analysis.analyze_text(text, 3, False)
    print result
    assert len(result["characters"]) == 40**3
    assert len(result["frequencies"]) == 40**3
    assert result["characters"][0] == "aaa"
    assert result["frequencies"][0] ==  1
    assert result["characters"][1] == "aab"
    assert result["frequencies"][1] ==  1
    assert result["characters"][2] == "aac"
    assert result["frequencies"][2] ==  0
    assert result["characters"][3] == "aad"
    assert result["frequencies"][3] ==  0
    assert result["characters"][4] == "aae"
    assert result["frequencies"][4] == 0
    
def test_initialize_third_order_matrix():
    """Test the initialize_third_order_matrix method of the analysis module."""
    
    result = analysis.initialize_third_order_matrix()
    assert len(result["characters"]) == 40**3
    assert len(result["frequencies"]) == 40**3
    
def test_analyze_text_third_order_responsive():
    """Test the analyze_text_third_order_responsive method of the analysis module."""
    
    text = "aaab"
    char_analysis = analysis.initialize_third_order_matrix()
    char_analysis = analysis.analyze_text_third_order_responsive(text[0:3], char_analysis)
    char_analysis = analysis.analyze_text_third_order_responsive(text[1:], char_analysis)
    assert char_analysis["characters"][0] == "aaa"
    assert char_analysis["characters"][1] == "aab"
    print char_analysis["frequencies"][0]
    assert char_analysis["frequencies"][0] == 1
    assert char_analysis["frequencies"][1] == 1
    assert char_analysis["frequencies"][2] == 0
    
def test_compute_most_probable_digraph():
    
    char_analysis = { "characters": ["ab", "bc", "bd", "cd"], "frequencies": [1, 2, 1, 1] }
    result = analysis.compute_most_probable_digraph(char_analysis, "a")
    assert result == "abcd"
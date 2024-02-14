from line_similarity_checker.similarity_checker import check_line_similarity


def test_similarity_checker_with_normal_sentence():
    """normalization score: 0.0 is least similar and 1.0 is most similar"""
    """when normalized = False, score is number of edits required to make two lines same"""
    """editing can be i)insertion ii)deletion iii)substitution iv)transposition(swapping)"""

    line1 = "ང་བོད་པ་ཡིན།"
    line2 = "ང་བོད་པ་ཡིན།"
    """lines are same, so score is 0 and normalized score is 1.0"""
    assert check_line_similarity(line1, line2, normalized=False) == 0
    assert check_line_similarity(line1, line2, normalized=True) == 1.0

    line1 = "ང་བོད་པ་ཡིན་"
    line2 = "ང་བོད་པ་ཡིན།"
    """only last character is different, so score is 1 and normalized score very high"""
    assert check_line_similarity(line1, line2, normalized=False) == 1.0
    assert check_line_similarity(line1, line2, normalized=True) == 0.9166666666666666

    line1 = "ང་བོད་པ་ཡིན།"
    line2 = "རྒྱ་གར་ནི་ས་ཆ་ཧ་ཅང་སྐྱིད་པོ་ཞིག་ཡིན།"
    """lines are very different, so score is 26 and normalized score is very low"""
    assert check_line_similarity(line1, line2, normalized=False) == 26.0
    assert check_line_similarity(line1, line2, normalized=True) == 0.2777777777777778


def test_similarity_checker_with_real_data():
    """Testing similarity checker against some sentence from real OCR data"""

    """first line is from batch2,10-1-313b_line_9874_4"""
    """second line is from batch2,7-1-1a_line_9874_0"""
    line1 = "དང༌། རྙེད་པ་དང༌། བཀུར་སྟི་ལ་རྒྱབ་ཀྱིས་ཕྱོགས་པ། དབང་པོ་དང༌། ཉེ་དབང་དང་བཅས་པའི་ལྷ་རྣམས་ཀྱིས་མཆོད་པ་དང༌། རྗེད་པ་དང༌། གུས་པར་སྨྲ་བར་བྱ་བར་གྱུར་ཏོ། །དེ་ནས་བཅོམ་"  # noqa
    line2 = "འདུལ་བ་ཇ་པ་བཞུགས་སོ།།"

    similarity_result = check_line_similarity(line1, line2, normalized=True)
    assert round(similarity_result, 2) == 0.11

    """first line is from batch2,10-1-313b_line_9874_4"""
    """second line is from batch2,8-1-219b_line_9874_3"""
    line1 = "དང༌། རྙེད་པ་དང༌། བཀུར་སྟི་ལ་རྒྱབ་ཀྱིས་ཕྱོགས་པ། དབང་པོ་དང༌། ཉེ་དབང་དང་བཅས་པའི་ལྷ་རྣམས་ཀྱིས་མཆོད་པ་དང༌། རྗེད་པ་དང༌། གུས་པར་སྨྲ་བར་བྱ་བར་གྱུར་ཏོ། །དེ་ནས་བཅོམ་"  # noqa
    line2 = "པ་བཞིས་བསྙེངས་པ་མི་མངའ་བ། ཡན་ལག་ལྔ་སྤངས་པ། འགྲོ་བ་ལྔ་ལས་ཡང་དག་པར་འདས་པ། ཡན་ལག་དྲུག་དང་ལྡན་པ། ཕ་རོལ་ཏུ་ཕྱིན་པ་དྲུག་ཡོངས་སུ་རྫོགས་པ། རྟག་ཏུ་གནས་པ་དྲུག་གིས་"  # noqa

    similarity_result = check_line_similarity(line1, line2, normalized=True)
    assert round(similarity_result, 2) == 0.2

    """first line is from batch2,10-1-313b_line_9874_4"""
    """second line is from batch2,7-1-281a_line_9874_1"""
    line1 = "དང༌། རྙེད་པ་དང༌། བཀུར་སྟི་ལ་རྒྱབ་ཀྱིས་ཕྱོགས་པ། དབང་པོ་དང༌། ཉེ་དབང་དང་བཅས་པའི་ལྷ་རྣམས་ཀྱིས་མཆོད་པ་དང༌། རྗེད་པ་དང༌། གུས་པར་སྨྲ་བར་བྱ་བར་གྱུར་ཏོ། །དེ་ནས་བཅོམ་"  # noqa
    line2 = "དང་བཅས་པས་མཉན་ཡོད་ནས་རྒྱལ་པོའི་ཁབ་ཀྱི་བར་ཇི་ཙམ་བར་བདག་ཅག་ལས་ན་བཟའ་དང༌། བསོད་སྙོམས་དང༌། གནས་མལ་དང༌། སྙུང་བའི་རྐྱེན་དང༌། སྨན་གྱི་ཡོ་"  # noqa
    similarity_result = check_line_similarity(line1, line2, normalized=True)
    assert round(similarity_result, 2) == 0.3

    """first line is from batch2,10-1-111b_line_9874_5"""
    """second line is from batch2,6-1-153a_line_9874_6"""
    line1 = "འཕྱ་ཞིང་དགེ་སྦྱོང་ཤཱཀྱའི་བུ་རྣམས་ནི། གཙང་སྦྲ་མེད་དེ། ལྷུང་བཟེད་བབ་བབ་ཏུ་འཇོག་གོ །ཞེས་ཟེར་བའི་སྐབས་དེ། དགེ་སློང་རྣམས་ཀྱིས་བཅོམ་ལྡན་འདས་ལ་གསོལ་པ་དང༌། བཅོམ་"  # noqa
    line2 = "ཅག་རང་རང་གིས་འཕྲག་པ་དག་གིས་ཀྱང་ཁྱེར་ཞེས་ཀྱང་ཐོས་སོ། །ཞེས་ཟེར་བའི་སྐབས་དེ། དགེ་སློང་རྣམས་ལ་བརྗོད་ནས་དགེ་སློང་རྣམས་ཀྱིས་བཅོམ་ལྡན་འདས་ལ་གསོལ་ཏེ། དེ་ནས་བཅོམ་ལྡན་"  # noqa
    similarity_result = check_line_similarity(line1, line2, normalized=True)
    assert round(similarity_result, 2) == 0.4

    """first line is from batch2,8-1-320b_line_9874_6"""
    """second line is from batch2,7-1-322a_line_9874_4"""
    line1 = "སོ༑ ༑དེའི་བསྟན་ས་ལ་འདི་རབ་ཏུ་བྱུང་ནས་དགེ་སློང་མ་གང་གིས་དེ་རབ་ཏུ་ཕྱུང་བའི་དགེ་སློང་མ་དེ། དེ་བཞིན་གཤེགས་པ་དགྲ་བཅོམ་པ་ཡང་དག་པར་རྫོགས་པའི་སངས་རྒྱས་འོད་སྲུང་གི་"  # noqa
    line2 = "ཅན་གྱི་ལྟ་བའི་རྣམ་པ་མི་གཏོང་བ་ལ་དེང་ཕྱིན་ཆད་དགེ་ཚུལ་ཁྱེད་གཉིས་བཅོམ་ལྡན་འདས་དེ་བཞིན་གཤེགས་པ་དགྲ་བཅོམ་པ་ཡང་དག་པར་རྫོགས་པའི་སངས་རྒྱས་དེ་ལ་སྟོན་པའོ། །"  # noqa
    similarity_result = check_line_similarity(line1, line2, normalized=True)
    assert round(similarity_result, 2) == 0.5

    """first line is from batch2,10-1-181a_line_9874_3"""
    """second line is from batch2,10-1-93a_line_9874_6"""
    line1 = "སྟེ་མི་བཅང༌། བཅོམ་ལྡན་འདས་ཀྱིས་མ་གནང་ངོ༌། །སྐབས་དེ། དགེ་སློང་དག་གིས་བཅོམ་ལྡན་འདས་ལ་གསོལ་པ་དང༌། བཅོམ་ལྡན་འདས་ཀྱིས་བཀའ་སྩལ་པ། དེ་ལྟ་བས་"  # noqa
    line2 = "བདག་རྣམས་ཀྱིས་མཐོང་ནས་འཕྱ་བའི་སྐབས་དེ། དགེ་སློང་རྣམས་ཀྱིས་བཅོམ་ལྡན་འདས་ལ་གསོལ་པ་དང༌། བཅོམ་ལྡན་འདས་ཀྱིས་བཀའ་སྩལ་པ། དགེ་སློང་དག །དེ་ལྟ་བས་"  # noqa
    similarity_result = check_line_similarity(line1, line2, normalized=True)
    assert round(similarity_result, 2) == 0.6

    """first line is from batch2,8-1-68a_line_9874_4"""
    """second line is from batch2,8-1-239b_line_9874_6"""
    line1 = "ཏེ༑ བཙུན་པ། བདག་བཅོམ་ལྡན་འདས་དང༌། ཆོས་དང༌། དགེ་སློང་གི་དགེ་འདུན་ལ་སྐྱབས་སུ་མཆི་ཡི། བདག་དགེ་བསྙེན་དུ་གཟུང་དུ་གསོལ། དེང་སླན་ཆད་ནས་ཇི་སྲིད་འཚོའི་བར་དུ་གློ་བ་"  # noqa
    line2 = "པར་ཞུགས་པ་ལགས་ཏེ། བཙུན་པ། བདག་བཅོམ་ལྡན་འདས་དང༌། ཆོས་དང༌། དགེ་སློང་གི་དགེ་འདུན་ལ་སྐྱབས་སུ་མཆི་ཡི། བདག་དགེ་བསྙེན་མར་གཟུང་དུ་གསོལ། དེང་སླན་ཆད་"  # noqa
    similarity_result = check_line_similarity(line1, line2, normalized=True)
    assert round(similarity_result, 2) == 0.7

    """first line is from batch2,7-1-41a_line_9874_6"""
    """second line is from batch2,6-1-185a_line_9874_5"""
    line1 = "མཛད་ནས་དགེ་སློང་རྣམས་ལ་བཀའ་སྩལ་པ། དགེ་སློང་དག་དེ་ལྟ་བས་ན་སྔ་མ་ནི་བཅས་པ་ཡིན་ལ། འདི་ནི་གནང་བ་ཡིན་ཏེ། ངའི་ཉན་ཐོས་རྣམས་ཀྱིས་འདུལ་བ་ལ་བསླབ་"  # noqa
    line2 = "བཀའ་མཆིད་མཛད་ནས་དགེ་སློང་རྣམས་ལ་བཀའ་སྩལ་པ། དགེ་སློང་དག། དེ་ལྟ་བས་ན། སྔ་མ་ནི། བཅས་པ་ཡིན་ལ། འདི་ནི། གནང་བ་ཡིན་ནོ། །ངའི་ཉན་ཐོས་རྣམས་ཀྱིས་འདུལ་བ་"  # noqa
    similarity_result = check_line_similarity(line1, line2, normalized=True)
    assert round(similarity_result, 2) == 0.81

    """first line is from batch2,6-1-377b_line_9874_2"""
    """second line is from batch2,8-1-302b_line_9874_2"""
    line1 = "སྩལ་པ། དགེ་སློང་དག །དེ་ལྟ་བས་ན། ཕན་ཡོན་བཅུ་ཡང་དག་པར་གཟིགས་པས། འདུལ་བ་ལ་ཉན་ཐོས་རྣམས་ཀྱི་བསླབ་པའི་གཞི་བཅའ་བར་བྱ་སྟེ་ཞེས་བྱ་བ་ལ་སོགས་པ་སྔ་མ་"  # noqa
    line2 = "བཀའ་སྩལ་པ། དགེ་སློང་དག། དེ་ལྟ་བས་ན། ཕན་ཡོན་བཅུ་ཡང་དག་པར་གཟིགས་པས། འདུལ་བ་ལ་ཉན་ཐོས་རྣམས་ཀྱི་བསླབ་པའི་གཞི་བཅའ་བར་བྱ་སྟེ་ཞེས་བྱ་བ་ལ་སོགས་པ་སྔ་མ་བཞིན་ནོ། །"  # noqa
    similarity_result = check_line_similarity(line1, line2, normalized=True)
    assert round(similarity_result, 2) == 0.9

#def test_accuracy():
#    assert hits("thunderbolt") == "Hits" or hits("thunderbolt") == "Missed"
#    assert hits("ice beam") == "Hits" or hits(thunderbolt) == "Missed"
#    assert hits("earth quake") == "Hits" or hits("earth quake") == "Missed"
#    assert hits("protect") == "Works" or hits("protect") == "Failed"
#    assert hits("air slash") == "Hits" or hits("air slash") == "Missed"
#def test_typematchup():
#    assert type_matchup("fire","water") == 0.5
#    assert type_matchup("electric","water") == 2.0
#    assert type_matchup("grass","ground") == 1.0
#    assert type_matchup("ghost","fire") == 1.0
#    assert type_matchup("flying","bug") == 2.0
#def test_speed():
#    assert speed(62,105) == "second pokemon goes first"
#    assert speed(42,42) == "tie(50/50)"
#    assert speed(82,65) == "first pokemon goes first"
#    assert speed(102,105) == "second pokemon goes first"
#    assert speed(125,115) == "first pokemon goes first"
#def test_hp():
#    assert hp(100,-30) == 70
#    assert hp(110,-40) == 60
#    assert hp(100, 30) == 130
#    assert hp(2, 30) == 32
#    assert hp(53, 42) == 95
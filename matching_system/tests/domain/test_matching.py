from app.domain import matching


players = [matching.Player("1", "a", 10),
           matching.Player("2", "b", 20),
           matching.Player("3", "c", 30)]

def test_player_innner_rate():
    point = 20
    player = matching.Player("1", "a", point)
    assert 20 == player.inner_rate


def test_party_inner_rate():
    point1 = 20
    point2 = 5
    point3 = 100
    party = matching.Party(
        [matching.Player("1", "a", point1),
         matching.Player("2", "b", point2),
         matching.Player("3", "c", point3)]
    )

    assert sum([point1, point2, point3]) / 3 == party.inner_rate

def test_solo_matching():
    solos = [matching.Entry([matching.Player("1", "b", 3)]),
             matching.Entry([matching.Player("2", "b", 3)]),
             matching.Entry([matching.Player("3", "b", 3)]),
             
             matching.Entry([matching.Player("4", "b", 4)]),
             matching.Entry([matching.Player("5", "b", 4)]),
             matching.Entry([matching.Player("6", "b", 4)]),
             
             matching.Entry([matching.Player("7", "b", 5)]),
             matching.Entry([matching.Player("8", "b", 6)]),
             matching.Entry([matching.Player("9", "b", 6)]),
             
             matching.Entry([matching.Player("10", "b", 6)]),
             matching.Entry([matching.Player("11", "b", 6)]),
             matching.Entry([matching.Player("12", "b", 7)]),
             
             matching.Entry([matching.Player("13", "b", 7)]),
             matching.Entry([matching.Player("14", "b", 7)])]
        
    solo_matching = matching.SoloMatching(solos)
    actual = solo_matching.make_match()
    expected = [[3, 7, 4],
                [3, 7, 4],
                [3, 7, 5],
                [4, 6, 6],
                [6, 6]]
    
    assert expected == [[p.inner_rate for p in e.players] for e in actual]


def test_duo_matching():
    entries = [matching.Entry([matching.Player("1", "b", 2)]),
               matching.Entry([matching.Player("2", "b", 2)]),
               
               matching.Entry([matching.Player("3", "b", 2),
                               matching.Player("4", "b", 2)]),
                               
               matching.Entry([matching.Player("5", "b", 3)]),
               
               matching.Entry([matching.Player("6", "b", 2),
                               matching.Player("7", "b", 4)]),
                               
               
               matching.Entry([matching.Player("8", "b", 3),
                               matching.Player("9", "b", 3)]),
                               
               matching.Entry([matching.Player("10", "b", 5)])]
    
    duo_matching = matching.DuoMatching(entries)
    actual = duo_matching.make_match()
    expected = set([(2, 2, 5),
                    (3,),
                    (2, 4, 2),
                    (3, 3, 2)])
    assert expected == set(tuple(p.inner_rate for p in e.players) for e in actual)
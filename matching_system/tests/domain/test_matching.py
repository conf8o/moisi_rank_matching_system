from app.domain import matching


def test_player_innner_rate():
    point = 20
    player = matching.Player("1", "a", point)
    assert 20 == player.inner_rate


def test_party_inner_rate():
    point1 = 20
    point2 = 5
    point3 = 100
    party = matching.Party(
        "",
        [matching.Player("1", "a", point1),
         matching.Player("2", "b", point2),
         matching.Player("3", "c", point3)]
    )

    assert sum([point1, point2, point3]) / 3 == party.inner_rate


def variance(entries):
    inner_rates = [e.inner_rate for e in entries]

    rate_avg = sum(inner_rates) / len(inner_rates)
    v = sum([(rate - rate_avg)**2 for rate in inner_rates]) / len(inner_rates)

    return v

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
    
    median = matching._median(solos)
    solo_matching = matching.SoloMatching(solos, median)
    actual = solo_matching.make_match()
    
    assert len(solos) == sum(len(e.players) for e in actual)

    # 内部レートの分散を計算し、マッチング後の分散が減っていることでテストとする
    original_var = variance(solos)
    after_var = variance(actual)
    print(_players_inner_rates(actual))
    print(f"分散: before:{original_var}, after:{after_var}")

    assert original_var > after_var


def _players_inner_rates(entries):
    return [tuple(p.inner_rate for p in e.players) for e in entries]


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
    
    median = matching._median(entries)
    duo_matching = matching.DuoMatching(entries, median)
    actual = duo_matching.make_match()
    
    assert sum(len(e.players) for e in entries) == sum(len(e.players) for e in actual)

    original_var = variance(entries)
    after_var = variance(actual)
    print(_players_inner_rates(actual))
    print(f"分散: before:{original_var}, after:{after_var}")

    assert original_var > after_var


def test_matching():
    entries = [matching.Entry([matching.Player("1", "b", 2)]),
               matching.Entry([matching.Player("2", "b", 2)]),
               
               matching.Entry([matching.Player("3", "b", 2),
                               matching.Player("4", "b", 2)]),
                               
               matching.Entry([matching.Player("5", "b", 3)]),
               
               matching.Entry([matching.Player("6", "b", 2),
                               matching.Player("7", "b", 4)]),
               
               matching.Entry([matching.Player("8", "b", 3),
                               matching.Player("9", "b", 3)]),
                               
               matching.Entry([matching.Player("10", "b", 5)]),

               matching.Entry([matching.Player("11", "b", 3)]),
               matching.Entry([matching.Player("12", "b", 3)]),
               matching.Entry([matching.Player("13", "b", 3)]),
               
               matching.Entry([matching.Player("14", "b", 4),
                               matching.Player("15", "b", 4)]),
               matching.Entry([matching.Player("16", "b", 4)]),
               
               matching.Entry([matching.Player("17", "b", 5),
                               matching.Player("18", "b", 6)]),
               matching.Entry([matching.Player("19", "b", 6)]),
               
               matching.Entry([matching.Player("20", "b", 6)]),
               matching.Entry([matching.Player("21", "b", 6)]),
               matching.Entry([matching.Player("22", "b", 7)]),
               
               matching.Entry([matching.Player("23", "b", 7)]),
               matching.Entry([matching.Player("24", "b", 7)])]
    
    original_var = variance(entries)
    m = matching.Matching(entries)
    actual = m.make_match()
    assert sum(len(e.players) for e in entries) == sum(len(e.players) for e in actual) 
    
    after_var = variance(actual)
    print(_players_inner_rates(actual))
    print(f"分散: before:{original_var}, after:{after_var}")

    assert original_var > after_var

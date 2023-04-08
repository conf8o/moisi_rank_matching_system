from app.domain import matching


def test_player_innner_rate():
    point = 20
    player = matching.Player("1", point)
    assert 20 == player.inner_rate


def test_party_inner_rate():
    point1 = 20
    point2 = 5
    point3 = 100
    party = matching.Party(
        [matching.Player("1", point1),
         matching.Player("2", point2),
         matching.Player("3", point3)]
    )

    assert sum([point1, point2, point3]) / 3 == party.inner_rate

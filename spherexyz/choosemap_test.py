from .choosemap import Choice


def test_choosemap():
    choice = Choice([True] * 8 + [False] * 9)
    assert choice.count_choices() == 8
    assert not choice.is_maximal()
    num_choices = 1
    while not choice.is_maximal():
        assert choice.perfect_hash() == num_choices - 1
        assert type(choice.perfect_hash()) == int
        choice.increment()
        num_choices += 1
    assert choice.perfect_hash() == num_choices - 1
    assert num_choices == 24310

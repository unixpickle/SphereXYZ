from .sphere import Sphere, Turn

SLICE_TURN = Turn.generate_m()


def test_m_u():
    """Test the algorithm 'M U'."""
    puzzle = Sphere()
    SLICE_TURN = Turn.generate_m()
    u_turn = Turn.generate_u()
    puzzle = SLICE_TURN.perform(puzzle)
    puzzle = u_turn.perform(puzzle)
    expected = Sphere.parse('2222111101112222 0111222222221111 11')
    assert expected is not None, 'failed to load control puzzle in algo 1'
    for i in range(0, 34):
        assert puzzle.pieces[i] == expected.pieces[i]


def test_m_s():
    """Test the algorithm 'M S'."""
    puzzle = Sphere()
    s_slice = Turn.generate_s()
    puzzle = SLICE_TURN.perform(puzzle)
    puzzle = s_slice.perform(puzzle)
    expected = Sphere.parse('0111111101111111 1222222212222222 22')
    assert expected is not None, 'failed to load control puzzle in algo 2'
    for i in range(0, 34):
        assert puzzle.pieces[i] == expected.pieces[i]


def test_m2():
    """Test the algorithm 'M2'."""
    slice2 = SLICE_TURN.exp(2)
    expected = [15, 32, 0, 1, 2, 3, 4, 5, 7, 33, 8, 9, 10, 11, 12, 13]
    expected += range(16, 32)
    expected += [14, 6]
    for i in range(0, 34):
        assert slice2.mapping[i] == expected[i]

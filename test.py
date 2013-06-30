import sphere
import choosemap

def test_turns():
    print("testing sphere.Turn()")
    # test M U
    puzzle = sphere.Sphere()
    sliceTurn = sphere.Turn.generate_m()
    uTurn = sphere.Turn.generate_u()
    puzzle = sliceTurn.perform(puzzle)
    puzzle = uTurn.perform(puzzle)
    expected = sphere.Sphere.parse("2222111101112222 0111222222221111 11")
    assert expected != None, "failed to load control puzzle in algo 1"
    for i in range(0, 34):
        if puzzle.pieces[i] != expected.pieces[i]:
            print("difference at " + str(i) + " in algo 1")
            print("expected " + str(expected.pieces[i]) + ", got " + str(puzzle.pieces[i]))

    # test M S
    puzzle = sphere.Sphere()
    sSlice = sphere.Turn.generate_s()
    puzzle = sliceTurn.perform(puzzle)
    puzzle = sSlice.perform(puzzle)
    expected = sphere.Sphere.parse("0111111101111111 1222222212222222 22")
    assert expected != None, "failed to load control puzzle in algo 2"
    for i in range(0, 34):
        if puzzle.pieces[i] != expected.pieces[i]:
            print("difference at " + str(i) + " in algo 2")
    print("test complete")
    
    # test M2
    slice2 = sliceTurn.exp(2)
    expected = [15, 32, 0, 1, 2, 3, 4, 5, 7, 33, 8, 9, 10, 11, 12, 13]
    expected += range(16, 32)
    expected += [14, 6]
    for i in range(0, 34):
        if slice2.mapping[i] != expected[i]:
            print("difference in mapping at " + str(i))

def test_choosemap():
    print("testing choosemap.Choice()")
    choice = choosemap.Choice([True] * 8 + [False] * 9)
    assert choice.count_choices() == 8
    assert not choice.is_maximal()
    numChoices = 1
    while not choice.is_maximal():
        assert choice.perfect_hash() == numChoices - 1
        choice.increment()
        numChoices += 1
    assert choice.perfect_hash() == numChoices - 1
    assert numChoices == 24310
    print("test complete")

test_turns()
test_choosemap()

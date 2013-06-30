import sphere

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

test_turns()

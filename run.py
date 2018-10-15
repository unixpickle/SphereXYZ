"""
A script for training and indexing.
"""

import sys

import spherexyz


def main():
    if len(sys.argv) != 4:
        die_usage()
    cmd = sys.argv[1]
    if cmd == 'solve':
        solve(*sys.argv[2:])
    elif cmd == 'index':
        index(*sys.argv[2:])
    else:
        sys.stderr.write('Unknown sub-command: ' + cmd + '\n')
        die_usage()


def die_usage():
    sys.stderr.write('Usage: python spherexyz solve <scramble> <table file>\n' +
                     '                        index <output> <max depth>\n')
    sys.exit(1)


def solve(scramble, table_file):
    scramble = spherexyz.Sphere.parse(scramble)
    if not scramble:
        sys.stderr.write('Invalid scramble.\n')
        sys.exit(1)
    heuristic = spherexyz.Heuristic(table_file)
    solver = spherexyz.Solver(scramble, heuristic)
    for i in range(0, 20):
        sys.stderr.write('Trying %d move solutions...\n' % i)
        solution = solver.run_depth(i)
        if solution:
            print(solution)
            break
    heuristic.close()


def index(output, max_depth):
    indexer = spherexyz.Indexer(int(max_depth))
    while indexer.step():
        if not indexer.added % 100:
            print('Expanded %d nodes, depth = %d' % (indexer.added, indexer.depth))
    print('Saving...')
    indexer.save(output)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3

import sys, json

import calculate_v0, calculate_v1
from fmt import ppd

def parse_args():
    version = sys.argv[1]
    lengths_needed = []
    for l, n in json.loads(sys.argv[2]).items():
        lengths_needed.extend([int(l)]*n)

    raw_lengths = []
    for l, n in json.loads(sys.argv[3]).items():
        raw_lengths.extend([int(l)]*n)

    ppd({'raw_lengths': raw_lengths})
    ppd({'lengths_needed': lengths_needed})

    return version, raw_lengths, lengths_needed

if __name__ == '__main__':
    version, raw_lengths, lengths_needed = parse_args()
    if version == '0':
        results, offcut_amount = calculate_v0.CutCalculator(raw_lengths, lengths_needed).run()
    elif version == '1':
        results, offcut_amount = calculate_v1.CutCalculator(raw_lengths, lengths_needed).run()

    for i, (offcuts, result) in enumerate(results.items()):
        print('\n' + '#' + '-'*10)
        print(f'{i}/{len(results.keys())}')
        ppd({'offcuts': result.offcuts}, indent=2)

        for i, (c, o) in enumerate(zip(result.cuts, result.offcuts)):
            print(f'- {i}: ', end='')
            ppd({'cuts': c, 'total': sum(c), 'offcut': o})

    print(f'\n{len(results.keys())}', 'total solutions with total offcuts =', offcut_amount)
    for i, (offcuts, result) in enumerate(results.items()):
        ppd(offcuts)


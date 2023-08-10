#!/usr/bin/env python3

import sys, json, time
from dataclasses import dataclass, field, asdict

from fmt import ppd

def unique_permutations_knuth(seq):
    '''
    Yield only unique permutations of seq in an efficient way.

    A python implementation of Knuth's "Algorithm L", also known from the
    std::next_permutation function of C++, and as the permutation algorithm
    of Narayana Pandita.
    '''
    # Precalculate the indices we'll be iterating over for speed
    i_indices = list(range(len(seq) - 1, -1, -1))
    k_indices = i_indices[1:]
    # The algorithm specifies to start with a sorted version
    seq = sorted(seq)

    while True:
        yield seq
        # Working backwards from the last-but-one index,           k
        # we find the index of the first decrease in value.  0 0 1 0 1 1 1 0
        for k in k_indices:
            if seq[k] < seq[k + 1]:
                break
        else:
            # Introducing the slightly unknown python for-else syntax:
            # else is executed only if the break statement was never reached.
            # If this is the case, seq is weakly decreasing, and we're done.
            return

        # Get item from sequence only once, for speed
        k_val = seq[k]
        # Working backwards starting with the last item,           k     i
        # find the first one greater than the one at k       0 0 1 0 1 1 1 0
        for i in i_indices:
            if k_val < seq[i]:
                break
        # Swap them in the most efficient way
        seq[k], seq[i] = seq[i], seq[k]                    #       k     i
                                                           # 0 0 1 1 1 1 0 0
        # Reverse the part after but not                           k
        # including k, also efficiently.                     0 0 1 1 0 0 1 1
        seq[k+1:] = seq[-1:k:-1]


from tqdm import tqdm

@dataclass
class CutSequence:
    raw_lengths: list
    cut_list: list
    blade_width: int = 2
    offcuts: list = field(default_factory=list)
    cuts: list = field(default_factory=list)

    @property
    def total_offcut(self):
        return sum(self.offcuts)

    def perform_cuts(self):
        i = 0
        current = self.raw_lengths[i]
        current_cut = []
        for cut in self.cut_list:
            cut = cut + self.blade_width
            if current - cut < 0:
                self.offcuts.append(current)
                self.cuts.append(current_cut)
                current_cut = []
                i += 1
                if i == len(self.raw_lengths):
                    return
                current = self.raw_lengths[i]
            current -= cut
            current_cut.append(cut)
        self.offcuts.append(current)
        self.cuts.append(current_cut)
        # for j in range(i+1, len(self.raw_lengths)):
        #     self.offcuts.append(self.raw_lengths[j])

from functools import lru_cache

@lru_cache
def run_cuts(raw_lengths, cuts):
    seq = CutSequence(raw_lengths, cuts)
    seq.perform_cuts()
    return seq

@dataclass
class CutCalculator:
    raw_lengths: list
    lengths_needed: list

    @property
    def total_raw_lengths(self):
        return sum(self.raw_lengths)

    @property
    def total_lengths_needed(self):
        return sum(self.lengths_needed)

    def run(self):
        current = 1_000_000
        best = dict()
        smallest_offcut = 1_000_000
        n_smallest_offcut = 0
        start_time = time.time()
        print('calculating cuts...')

        pbar = tqdm()
        for i, g in enumerate(unique_permutations_knuth(self.lengths_needed)):
            if i % 100_000 == 0:
                pbar.update(100_000)
                # print(f'\r{i:,d}', end='')
            seq = run_cuts(tuple(self.raw_lengths), tuple(g))
            s = min(seq.offcuts)
            n = seq.offcuts.count(s)
            if seq.total_offcut < current:
                if s < smallest_offcut:
                    smallest_offcut = s
                    n_smallest_offcut = n
                    # print('new best', seq.total_offcut)
                    current = seq.total_offcut
                    best = {tuple(sorted(seq.offcuts)): seq}
            elif seq.total_offcut == current:
                if s < smallest_offcut or (s == smallest_offcut and n > n_smallest_offcut):
                    pbar.write(f'new best {seq.total_offcut}, {s}x{n}')
                    smallest_offcut = s
                    n_smallest_offcut = n
                    current = seq.total_offcut
                    best = {tuple(sorted(seq.offcuts)): seq}
        pbar.close()


        end_time = time.time()
        print(f'\ncomplete! tested {i:,d} cuts in {end_time-start_time:.2f}s')

        return best, current

#!/usr/bin/env python3

import sys, json, time
from dataclasses import dataclass, field, asdict

from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalTrueColorFormatter

@dataclass
class CutCalculator:
    raw_lengths: list
    lengths_needed: list

    @property
    def raw_lengths_sorted(self):
        return sorted(self.raw_lengths, reverse=True)

    @property
    def lengths_needed_sorted(self):
        return sorted(self.lengths_needed, reverse=True)

    def split_cuts(self, raw_length, cuts):
        total = 0
        split = []
        for i, c in enumerate(cuts):
            if total + c > raw_length:
                return cuts[:i], cuts[i:]
            total += c
        return cuts, []

    def run(self):
        for r in self.raw_lengths_sorted:
            print(self.split_cuts(r, self.lengths_needed))
        return {}, 0
        pass


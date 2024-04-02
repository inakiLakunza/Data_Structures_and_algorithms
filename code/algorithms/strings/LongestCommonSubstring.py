

import bisect
from collections import deque

class LongestCommonSubstring:

    def __init__(self, strings):
        self.strings = strings
        self.k = 2
        self.num_sentinels = len(strings)
        self.text_length = sum(len(s) for s in strings) + self.num_sentinels
        self.shift = 0
        self.lowest_ascii_value = float('inf')
        self.highest_ascii_value = float('-inf')
        self.imap = []
        self.text = []
        self.sa = []
        self.lcp = []
        self.lcss = set()

    def main(self):
        self.init()
        self.solve()

    def init(self):
        self.compute_text_length()
        self.build_reverse_color_mapping()
        self.compute_shift()
        self.build_text()

    def compute_text_length(self):
        self.text_length = sum(len(s) for s in self.strings) + self.num_sentinels

    def build_reverse_color_mapping(self):
        self.imap = []
        for i, s in enumerate(self.strings):
            for _ in range(len(s)):
                self.imap.append(i)
                self.lowest_ascii_value = min(self.lowest_ascii_value, ord(s[_]))
                self.highest_ascii_value = max(self.highest_ascii_value, ord(s[_]))
        for _ in range(self.num_sentinels):
            self.imap.append(_)

    def compute_shift(self):
        self.shift = self.num_sentinels - self.lowest_ascii_value

    def build_text(self):
        self.text = [0] * self.text_length
        sentinel = 0
        k = 0
        for i in range(len(self.strings)):
            s = self.strings[i]
            for j in range(len(s)):
                self.text[k] = ord(s[j]) + self.shift
                k += 1
            self.text[k] = sentinel
            k += 1
            sentinel += 1

    def enough_unique_colors_in_window(self, lo, hi):
        colors = set()
        for i in range(lo, hi + 1):
            colors.add(self.imap[self.sa[i]])
        return len(colors) == self.k

    def retrieve_string(self, i, length):
        return ''.join(chr(self.text[i + j] - self.shift) for j in range(length))

    def add_lcs(self, lo, hi, window_lcp):
        if hi - lo + 1 < self.k:
            return
        if window_lcp == 0:
            return
        if not self.enough_unique_colors_in_window(lo, hi):
            return
        if window_lcp > len(self.lcss):
            self.lcss.clear()
        if window_lcp == len(self.lcss):
            self.lcss.add(self.retrieve_string(self.sa[lo], window_lcp))

    def solve(self):
        suffix_array = SuffixArray(self.text)
        self.sa = suffix_array.get_sa()
        self.lcp = suffix_array.get_lcp_array()
        tree = CompactMinSegmentTree(self.lcp)

        lo = self.num_sentinels
        hi = self.num_sentinels

        while True:
            shrink_window = True if hi == self.text_length - 1 else self.enough_unique_colors_in_window(lo, hi)
            if shrink_window:
                lo += 1
            else:
                hi += 1
            if lo == self.text_length - 1:
                break
            if lo == hi:
                continue
            window_lcp = tree.query(lo + 1, hi + 1)
            self.add_lcs(lo, hi, window_lcp)

class SuffixArray:

    def __init__(self, text):
        self.text = text
        self.n = len(text)
        self.sa = []
        self.lcp = []

    def get_sa(self):
        self.construct_suffix_array()
        return self.sa

    def get_lcp_array(self):
        self.build_lcp_array()
        return self.lcp

    def construct_suffix_array(self):
        suffix_ranks = [[self.text[i], i] for i in range(self.n)]
        suffix_ranks.sort()
        ranks = [0] * self.n
        new_rank = 0

        for i in range(1, self.n):
            if suffix_ranks[i][0] != suffix_ranks[i - 1][0]:
                new_rank += 1
            ranks[suffix_ranks[i][1]] = new_rank

        for k in range(1, self.n * 2, k * 2):
            rank_tuples = []
            for i in range(self.n):
                second_half = ranks[i + k] if i + k < self.n else -1
                rank_tuples.append((ranks[i], second_half, i))
            rank_tuples.sort()
            new_rank = 0
            for i in range(1, self.n):
                if rank_tuples[i][0] != rank_tuples[i - 1][0] or rank_tuples[i][1] != rank_tuples[i - 1][1]:
                    new_rank += 1
                ranks[rank_tuples[i][2]] = new_rank

        self.sa = [x[2] for x in rank_tuples]

    def build_lcp_array(self):
        inv_sa = [0] * self.n
        for i in range(self.n):
            inv_sa[self.sa[i]] = i

        self.lcp = [0] * self.n
        len_lcp = 0
        for i in range(self.n):
            if inv_sa[i] > 0:
                k = self.sa[inv_sa[i] - 1]
                while i + len_lcp < self.n and k + len_lcp < self.n and self.text[i + len_lcp] == self.text[k + len_lcp]:
                    len_lcp += 1
                self.lcp[inv_sa[i] - 1] = len_lcp
                if len_lcp > 0:
                    len_lcp -= 1

class CompactMinSegmentTree:

    def __init__(self, values):
        self.n = len(values)
        self.tree = [float('inf')] * (2 * self.n)
        self.construct(values)

    def function(self, a, b):
        if a == float('inf'):
            return b
        elif b == float('inf'):
            return a
        return min(a, b)

    def modify(self, i, value):
        i += self.n
        self.tree[i] = value
        while i > 1:
            i >>= 1
            self.tree[i] = self.function(self.tree[i << 1], self.tree[i << 1 | 1])

    def query(self, l, r):
        res = float('inf')
        l += self.n
        r += self.n
        while l < r:
            if l & 1:
                res = self.function(res, self.tree[l])
                l += 1
            if r & 1:
                r -= 1
                res = self.function(res, self.tree[r])
            l >>= 1
            r >>= 1
        return res

strings = ["abcde", "habcab", "ghabcdf"]
solver = LongestCommonSubstring(strings)
solver.main()
print("Longest common substrings:", solver.lcss)

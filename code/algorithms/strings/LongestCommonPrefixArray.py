

class SuffixArray:
    def __init__(self, text):
        self.ALPHABET_SZ = 256
        self.T = text
        self.N = len(text)
        self.sa = [0] * self.N
        self.sa2 = [0] * self.N
        self.rank = [0] * self.N
        self.c = [0] * max(self.ALPHABET_SZ, self.N)
        self.construct()
        self.kasai()

    def construct(self):
        c = [0] * self.ALPHABET_SZ
        for i in range(self.N):
            self.rank[i] = self.T[i]
            c[self.rank[i]] += 1
        for i in range(1, self.ALPHABET_SZ):
            c[i] += c[i - 1]
        for i in range(self.N - 1, -1, -1):
            c[self.T[i]] -= 1
            self.sa[c[self.T[i]]] = i
        p = r = 0
        while p < self.N:
            r = 0
            for i in range(self.N - p, self.N):
                self.sa2[r] = i
                r += 1
            for i in range(self.N):
                if self.sa[i] >= p:
                    self.sa2[r] = self.sa[i] - p
                    r += 1
            c = [0] * self.ALPHABET_SZ
            for i in range(self.N):
                c[self.rank[i]] += 1
            for i in range(1, self.ALPHABET_SZ):
                c[i] += c[i - 1]
            for i in range(self.N - 1, -1, -1):
                c[self.rank[self.sa2[i]]] -= 1
                self.sa[c[self.rank[self.sa2[i]]]] = self.sa2[i]
            self.sa2[self.sa[0]] = r = 0
            for i in range(1, self.N):
                if not (self.rank[self.sa[i - 1]] == self.rank[self.sa[i]] and
                        self.sa[i - 1] + p < self.N and self.sa[i] + p < self.N and
                        self.rank[self.sa[i - 1] + p] == self.rank[self.sa[i] + p]):
                    r += 1
                self.sa2[self.sa[i]] = r
            self.rank, self.sa2 = self.sa2, self.rank
            if r == self.N - 1:
                break
            self.ALPHABET_SZ = r + 1
            p <<= 1

    def kasai(self):
        self.lcp = [0] * self.N
        inv = [0] * self.N
        for i in range(self.N):
            inv[self.sa[i]] = i
        i = 0
        while i < self.N:
            if inv[i] > 0:
                k = self.sa[inv[i] - 1]
                length = 0
                while i + length < self.N and k + length < self.N and self.T[i + length] == self.T[k + length]:
                    length += 1
                self.lcp[inv[i] - 1] = length
                if length > 0:
                    length -= 1
            i += 1

    def display(self):
        print("-----i-----SA-----LCP---Suffix")
        for i in range(self.N):
            suffix_len = self.N - self.sa[i]
            suffix = ''.join(chr(c) for c in self.T[self.sa[i]:])
            print(f"{i:7} {self.sa[i]:7} {self.lcp[i]:7} {suffix}")


if __name__ == "__main__":
    str_ = "abcbbccaabcaabc"
    sa = SuffixArray([ord(c) for c in str_])
    sa.display()
    print("The LCP array is:", sa.lcp)

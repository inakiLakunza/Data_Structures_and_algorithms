

class SuffixArray:
    def __init__(self, text):
        self.ALPHABET_SZ = 256
        self.N = len(text)
        self.T = text
        self.sa = [0] * self.N
        self.sa2 = [0] * self.N
        self.rank = [0] * self.N
        self.c = [0] * max(self.ALPHABET_SZ, self.N)
        self.construct()
        self.kasai()

    def construct(self):
        p = r = 0
        for i in range(self.N):
            self.c[self.rank[i] == self.T[i]] += 1
        for i in range(1, self.ALPHABET_SZ):
            self.c[i] += self.c[i - 1]
        for i in range(self.N - 1, -1, -1):
            self.sa[self.c[self.T[i]] - 1] = i
            self.c[self.T[i]] -= 1
        p = 1
        while True:
            r = 0
            for i in range(self.N - p, self.N):
                self.sa2[r] = i
                r += 1
            for i in range(self.N):
                if self.sa[i] >= p:
                    self.sa2[r] = self.sa[i] - p
                    r += 1
            self.c = [0] * max(self.ALPHABET_SZ, self.N)
            for i in range(self.N):
                self.c[self.rank[i]] += 1
            for i in range(1, self.ALPHABET_SZ):
                self.c[i] += self.c[i - 1]
            for i in range(self.N - 1, -1, -1):
                self.sa[self.c[self.rank[self.sa2[i]]] - 1] = self.sa2[i]
                self.c[self.rank[self.sa2[i]]] -= 1
            self.sa2[self.sa[0]] = r = 0
            for i in range(1, self.N):
                if not (self.rank[self.sa[i - 1]] == self.rank[self.sa[i]] and self.sa[i - 1] + p < self.N and self.sa[i] + p < self.N and self.rank[self.sa[i - 1] + p] == self.rank[self.sa[i] + p]):
                    r += 1
                self.sa2[self.sa[i]] = r
            self.tmp = self.rank
            self.rank = self.sa2
            self.sa2 = self.tmp
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

    def lrs(self):
        max_len = 0
        lrss = set()
        for i in range(self.N):
            if self.lcp[i] > 0 and self.lcp[i] >= max_len:
                if self.lcp[i] > max_len:
                    lrss.clear()
                max_len = self.lcp[i]
                lrss.add("".join(map(chr, self.T[self.sa[i]:self.sa[i] + max_len])))
        return lrss


def main():
    str1 = "ABC$BCA$CAB"
    sa1 = SuffixArray(list(map(ord, str1)))
    print("LRS(s) of", str1, "is/are:", sa1.lrs())

    str2 = "aaaaa"
    sa2 = SuffixArray(list(map(ord, str2)))
    print("LRS(s) of", str2, "is/are:", sa2.lrs())

    str3 = "abcde"
    sa3 = SuffixArray(list(map(ord, str3)))
    print("LRS(s) of", str3, "is/are:", sa3.lrs())


if __name__ == "__main__":
    main()

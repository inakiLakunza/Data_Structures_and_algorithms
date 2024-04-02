

#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

class SuffixArray {
public:
    int ALPHABET_SZ = 256;
    int N;
    vector<int> T, lcp, sa, sa2, rank, tmp, c;

    SuffixArray(string str) {
        T = toIntArray(str);
        N = str.length();
        sa.resize(N);
        sa2.resize(N);
        rank.resize(N);
        c.resize(max(ALPHABET_SZ, N));
        construct();
        kasai();
    }

    vector<int> toIntArray(string s) {
        vector<int> text(s.length());
        for (int i = 0; i < s.length(); i++) text[i] = s[i];
        return text;
    }

    void construct() {
        vector<int> c(ALPHABET_SZ);
        for (int i = 0; i < N; ++i) c[rank[i] = T[i]]++;
        for (int i = 1; i < ALPHABET_SZ; ++i) c[i] += c[i - 1];
        for (int i = N - 1; i >= 0; --i) sa[--c[T[i]]] = i;
        for (int p = 1, r = 0; p < N; p <<= 1) {
            for (int i = N - p, r = 0; i < N; ++i) sa2[r++] = i;
            for (int i = 0; i < N; ++i) if (sa[i] >= p) sa2[r++] = sa[i] - p;
            fill(c.begin(), c.begin() + ALPHABET_SZ, 0);
            for (int i = 0; i < N; ++i) c[rank[i]]++;
            for (int i = 1; i < ALPHABET_SZ; ++i) c[i] += c[i - 1];
            for (int i = N - 1; i >= 0; --i) sa[--c[rank[sa2[i]]]] = sa2[i];
            int i;
            for (sa2[sa[0]] = r = i = 0; i < N; ++i) {
                if (!(rank[sa[i - 1]] == rank[sa[i]]
                        && sa[i - 1] + p < N && sa[i] + p < N
                        && rank[sa[i - 1] + p] == rank[sa[i] + p])) r++;
                sa2[sa[i]] = r;
            }
            tmp = rank;
            rank = sa2;
            sa2 = tmp;
            if (r == N - 1) break;
            ALPHABET_SZ = r + 1;
        }
    }

    void kasai() {
        lcp.resize(N);
        vector<int> inv(N);
        for (int i = 0; i < N; i++) inv[sa[i]] = i;
        for (int i = 0, len = 0; i < N; i++) {
            if (inv[i] > 0) {
                int k = sa[inv[i] - 1];
                while (i + len < N && k + len < N && T[i + len] == T[k + len]) len++;
                lcp[inv[i] - 1] = len;
                if (len > 0) len--;
            }
        }
    }

    void display() {
        cout << "-----i-----SA-----LCP---Suffix" << endl;
        for (int i = 0; i < N; i++) {
            int suffixLen = N - sa[i];
            string suffix(T.begin() + sa[i], T.end());
            cout << i << "       " << sa[i] << "      " << lcp[i] << "    " << suffix << endl;
        }
    }
};

int main() {
    string str = "abcbbccaabcaabc";
    SuffixArray sa(str);
    sa.display();
    cout << "The LCP array is: ";
    for (int i = 0; i < sa.lcp.size(); ++i) {
        cout << sa.lcp[i] << " ";
    }
    cout << endl;
    return 0;
}



#include <iostream>
#include <vector>
#include <set>
#include <algorithm>

using namespace std;

class SuffixArray {
private:
    int ALPHABET_SZ = 256;
    int N;
    vector<int> T, sa, sa2, rank, c, lcp;
    vector<int> toIntArray(const string& s) {
        vector<int> text(s.length());
        for (int i = 0; i < s.length(); i++) text[i] = s[i];
        return text;
    }
    void construct() {
        int p, r;
        for (int i = 0; i < N; ++i) c[rank[i] = T[i]]++;
        for (int i = 1; i < ALPHABET_SZ; ++i) c[i] += c[i - 1];
        for (int i = N - 1; i >= 0; --i) sa[--c[T[i]]] = i;
        for (p = 1; p < N; p <<= 1) {
            for (int r = 0, i = N - p; i < N; ++i) sa2[r++] = i;
            for (int i = 0; i < N; ++i) if (sa[i] >= p) sa2[r++] = sa[i] - p;
            fill(c.begin(), c.begin() + ALPHABET_SZ, 0);
            for (int i = 0; i < N; ++i) c[rank[i]]++;
            for (int i = 1; i < ALPHABET_SZ; ++i) c[i] += c[i - 1];
            for (int i = N - 1; i >= 0; --i) sa[--c[rank[sa2[i]]]] = sa2[i];
            sa2[sa[0]] = r = 0;
            int i;
            for (i = 1; i < N; ++i) {
                if (!(rank[sa[i - 1]] == rank[sa[i]]
                    && sa[i - 1] + p < N
                    && sa[i] + p < N
                    && rank[sa[i - 1] + p] == rank[sa[i] + p])) r++;
                sa2[sa[i]] = r;
            }
            vector<int> tmp = rank;
            rank = sa2;
            sa2 = tmp;
            if (r == N - 1) break;
            ALPHABET_SZ = r + 1;
        }
    }
    void kasai() {
        lcp = vector<int>(N);
        vector<int> inv(N);
        for (int i = 0; i < N; i++) inv[sa[i]] = i;
        for (int i = 0, len = 0; i < N; i++) {
            if (inv[i] > 0) {
                int k = sa[inv[i] - 1];
                while ((i + len < N) && (k + len < N) && T[i + len] == T[k + len]) len++;
                lcp[inv[i] - 1] = len;
                if (len > 0) len--;
            }
        }
    }

public:
    SuffixArray(const string& str) : SuffixArray(toIntArray(str)) {}
    SuffixArray(const vector<int>& text) {
        T = text;
        N = text.size();
        sa = vector<int>(N);
        sa2 = vector<int>(N);
        rank = vector<int>(N);
        c = vector<int>(max(ALPHABET_SZ, N));
        construct();
        kasai();
    }
    set<string> lrs() {
        int max_len = 0;
        set<string> lrss;
        for (int i = 0; i < N; i++) {
            if (lcp[i] > 0 && lcp[i] >= max_len) {
                if (lcp[i] > max_len) lrss.clear();
                max_len = lcp[i];
                lrss.insert(string(T.begin() + sa[i], T.begin() + sa[i] + max_len));
            }
        }
        return lrss;
    }
};

int main() {
    string str1 = "ABC$BCA$CAB";
    SuffixArray sa1(str1);
    cout << "LRS(s) of " << str1 << " is/are: ";
    for (const auto& lrs : sa1.lrs()) {
        cout << lrs << " ";
    }
    cout << endl;

    string str2 = "aaaaa";
    SuffixArray sa2(str2);
    cout << "LRS(s) of " << str2 << " is/are: ";
    for (const auto& lrs : sa2.lrs()) {
        cout << lrs << " ";
    }
    cout << endl;

    string str3 = "abcde";
    SuffixArray sa3(str3);
    cout << "LRS(s) of " << str3 << " is/are: ";
    for (const auto& lrs : sa3.lrs()) {
        cout << lrs << " ";
    }
    cout << endl;

    return 0;
}

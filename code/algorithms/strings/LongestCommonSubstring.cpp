#include <iostream>
#include <vector>
#include <algorithm>
#include <set>
#include <tuple>

class SuffixArray {
private:
    std::vector<int> sa;
    std::vector<int> lcp;
    std::vector<int> text;
    int n;

public:
    SuffixArray(const std::vector<int>& text) : text(text), n(text.size()) {}

    std::vector<int> get_sa() {
        construct_suffix_array();
        return sa;
    }

    std::vector<int> get_lcp_array() {
        build_lcp_array();
        return lcp;
    }

private:
    void construct_suffix_array() {
        std::vector<std::tuple<int, int, int>> rank_tuples(n);

        for (int i = 0; i < n; i++) {
            rank_tuples[i] = std::make_tuple(text[i], i, 0);
        }

        std::sort(rank_tuples.begin(), rank_tuples.end());

        std::vector<int> ranks(n);
        int new_rank = 0;

        for (int i = 1; i < n; i++) {
            if (std::get<0>(rank_tuples[i]) != std::get<0>(rank_tuples[i - 1])) {
                new_rank++;
            }
            ranks[std::get<1>(rank_tuples[i])] = new_rank;
        }

        for (int k = 1; k < n * 2; k *= 2) {
            std::vector<std::tuple<int, int, int>> new_rank_tuples(n);

            for (int i = 0; i < n; i++) {
                int second_half = (i + k < n) ? ranks[i + k] : -1;
                new_rank_tuples[i] = std::make_tuple(ranks[i], second_half, i);
            }

            std::sort(new_rank_tuples.begin(), new_rank_tuples.end());

            new_rank = 0;
            for (int i = 1; i < n; i++) {
                if (std::get<0>(new_rank_tuples[i]) != std::get<0>(new_rank_tuples[i - 1]) ||
                    std::get<1>(new_rank_tuples[i]) != std::get<1>(new_rank_tuples[i - 1])) {
                    new_rank++;
                }
                ranks[std::get<2>(new_rank_tuples[i])] = new_rank;
            }
        }

        sa.resize(n);
        for (int i = 0; i < n; i++) {
            sa[i] = std::get<2>(rank_tuples[i]);
        }
    }

    void build_lcp_array() {
        std::vector<int> inv_sa(n);
        for (int i = 0; i < n; i++) {
            inv_sa[sa[i]] = i;
        }

        lcp.resize(n);
        int len_lcp = 0;
        for (int i = 0; i < n; i++) {
            if (inv_sa[i] > 0) {
                int k = sa[inv_sa[i] - 1];
                while (i + len_lcp < n && k + len_lcp < n && text[i + len_lcp] == text[k + len_lcp]) {
                    len_lcp++;
                }
                lcp[inv_sa[i] - 1] = len_lcp;
                if (len_lcp > 0) {
                    len_lcp--;
                }
            }
        }
    }
};

class LongestCommonSubstring {
private:
    std::vector<std::string> strings;
    int k;
    int num_sentinels;
    int text_length;
    int shift;
    int lowest_ascii_value;
    int highest_ascii_value;
    std::vector<int> imap;
    std::vector<int> text;
    std::vector<int> sa;
    std::vector<int> lcp;
    std::set<std::string> lcss;

public:
    LongestCommonSubstring(const std::vector<std::string>& strings) : strings(strings), k(2) {
        num_sentinels = strings.size();
        compute_text_length();
        build_reverse_color_mapping();
        compute_shift();
        build_text();
    }

    void main() {
        solve();
    }

private:
    void compute_text_length() {
        text_length = 0;
        for (const std::string& s : strings) {
            text_length += s.length();
        }
        text_length += num_sentinels;
    }

    void build_reverse_color_mapping() {
        imap.clear();
        lowest_ascii_value = INT_MAX;
        highest_ascii_value = INT_MIN;

        for (int i = 0; i < strings.size(); i++) {
            for (char c : strings[i]) {
                imap.push_back(i);
                lowest_ascii_value = std::min(lowest_ascii_value, (int)c);
                highest_ascii_value = std::max(highest_ascii_value, (int)c);
            }
        }

        for (int i = 0; i < num_sentinels; i++) {
            imap.push_back(i);
        }
    }

    void compute_shift() {
        shift = num_sentinels - lowest_ascii_value;
    }

    void build_text() {
        text.clear();
        text.resize(text_length);
        int sentinel = 0;
        int k = 0;
        for (int i = 0; i < strings.size(); i++) {
            const std::string& s = strings[i];
            for (char c : s) {
                text[k++] = c + shift;
            }
            text[k++] = sentinel++;
        }
    }

    bool enough_unique_colors_in_window(int lo, int hi) {
        std::set<int> colors;
        for (int i = lo; i <= hi; i++) {
            colors.insert(imap[sa[i]]);
        }
        return colors.size() == k;
    }

    std::string retrieve_string(int i, int length) {
        std::string result;
        for (int j = 0; j < length; j++) {
            result.push_back(text[i + j] - shift);
        }
        return result;
    }

    void add_lcs(int lo, int hi, int window_lcp) {
        if (hi - lo + 1 < k || window_lcp == 0 || !enough_unique_colors_in_window(lo, hi)) {
            return;
        }

        if (window_lcp > lcss.size()) {
            lcss.clear();
        }

        if (window_lcp == lcss.size()) {
            lcss.insert(retrieve_string(sa[lo], window_lcp));
        }
    }

    void solve() {
        SuffixArray suffix_array(text);
        sa = suffix_array.get_sa();
        lcp = suffix_array.get_lcp_array();

        int lo = num_sentinels;
        int hi = num_sentinels;

        while (true) {
            bool shrink_window = (hi == text_length - 1) ? true : enough_unique_colors_in_window(lo, hi);

            if (shrink_window) {
                lo++;
            } else {
                hi++;
            }

            if (lo == text_length - 1) {
                break;
            }

            if (lo == hi) {
                continue;
            }

            int window_lcp = *std::min_element(lcp.begin() + lo, lcp.begin() + hi);
            add_lcs(lo, hi, window_lcp);
        }

        std::cout << "Longest common substrings:" << std::endl;
        for (const std::string& lcs : lcss) {
            std::cout << lcs << std::endl;
        }
    }
};

int main() {
    std::vector<std::string> strings = {"abcde", "habcab", "ghabcdf"};
    LongestCommonSubstring solver(strings);
    solver.main();
    return 0;
}

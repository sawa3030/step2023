#include <bits/stdc++.h>

using namespace std;

int main () {
    string random_word;
    cin >> random_word;

    sort(random_word.begin(), random_word.end());

    std::ifstream dictionary;
    dictionary.open("words_small.txt", std::ios::in);
    std::string reading_line_buffer;
    vector<pair<string, string>> pair_dictionary;
    while(getline(dictionary, reading_line_buffer)){
        pair_dictionary.push_back(make_pair(reading_line_buffer, reading_line_buffer));
    }

    for(int i = 0; i < pair_dictionary.size(); i++) {
        sort(pair_dictionary.at(i).first.begin(), pair_dictionary.at(i).first.end());
    }
    sort(pair_dictionary.begin(), pair_dictionary.end());

    /*for(int i = 0; i < pair_dictionary.size(); i++) {
        cout << pair_dictionary.at(i).first << " " << pair_dictionary.at(i).second << endl;
    }*/

    int left = 0, right = pair_dictionary.size() - 1; // 配列 a の左端と右端
    while (right >= left) {
        int mid = left + (right - left) / 2; // 区間の真ん中
        if (pair_dictionary.at(mid).first == random_word) {
            for(int i = mid; pair_dictionary.at(i).first == random_word; i--) {
                cout << pair_dictionary.at(i).second;
            }
            for(int i = mid+1; pair_dictionary.at(i).first == random_word; i++) {
                cout << pair_dictionary.at(i).second;
            }
            return 0;
        } else if (pair_dictionary.at(mid).first > random_word) {
            right = mid - 1;
        } else if (pair_dictionary.at(mid).first < random_word) {
            left = mid + 1;
        }
    }

    cout << "no anagram" << endl;
}
#include <bits/stdc++.h>

using namespace std;

vector<string> better_solution(string random_word, vector<string> dictionary) {
    sort(random_word.begin(), random_word.end());

    vector<pair<string, string>> new_dictionary;

    for(int i = 0; i < dictionary.size(); i++) {
        new_dictionary.push_back(make_pair(dictionary.at(i), dictionary.at(i)));
    }

    for(int i = 0; i < new_dictionary.size(); i++) {
        sort(new_dictionary.at(i).first.begin(), new_dictionary.at(i).first.end());
    }
    sort(new_dictionary.begin(), new_dictionary.end());

    /*
    for(int i = 0; i < new_dictionary.size(); i++) {
        cout << new_dictionary.at(i).first << " " << new_dictionary.at(i).second << endl;
    }
    */

    vector<string> anagram;
    int left = 0, right = new_dictionary.size() - 1; // 配列 a の左端と右端
    while (right >= left) {
        int mid = left + (right - left) / 2; // 区間の真ん中
        if (new_dictionary.at(mid).first == random_word) {
            for(int i = mid; new_dictionary.at(i).first == random_word; i--) {
                anagram.push_back(new_dictionary.at(i).second);
            }
            for(int i = mid+1; new_dictionary.at(i).first == random_word; i++) {
                anagram.push_back(new_dictionary.at(i).second);
            }
            return anagram;
        } else if (new_dictionary.at(mid).first > random_word) {
            right = mid - 1;
        } else if (new_dictionary.at(mid).first < random_word) {
            left = mid + 1;
        }
    }

    return anagram;
}

int main () {
    string random_word;
    cin >> random_word;

    //sort(random_word.begin(), random_word.end());

    ifstream dictionary;
    dictionary.open("words_small.txt", std::ios::in);
    string reading_line_buffer;
    vector<pair<string, string>> pair_dictionary;
    vector<string> old_dictionary;
    while(getline(dictionary, reading_line_buffer)){
        old_dictionary.push_back(reading_line_buffer);
    }

/*
    for(int i = 0; i < pair_dictionary.size(); i++) {
        sort(pair_dictionary.at(i).first.begin(), pair_dictionary.at(i).first.end());
    }
    sort(pair_dictionary.begin(), pair_dictionary.end());
*/
    /*for(int i = 0; i < pair_dictionary.size(); i++) {
        cout << pair_dictionary.at(i).first << " " << pair_dictionary.at(i).second << endl;
    }*/

/*
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
    */

    vector<string> ans = better_solution (random_word, old_dictionary);

    for(int i = 0; i < ans.size(); i++) {
        cout << ans.at(i) << endl;
    }
}
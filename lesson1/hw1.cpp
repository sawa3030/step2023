#include <bits/stdc++.h>

using namespace std;

vector<pair<string, string>> make_new_dictionary (vector<string> dictionary) {
    //ソートした辞書を作成
    vector<pair<string, string>> new_dictionary;

    for(int i = 0; i < static_cast<int>(dictionary.size()); i++) {
        new_dictionary.push_back(make_pair(dictionary.at(i), dictionary.at(i)));
    }

    for(int i = 0; i < static_cast<int>(new_dictionary.size()); i++) {
        sort(new_dictionary.at(i).first.begin(), new_dictionary.at(i).first.end());
    }
    sort(new_dictionary.begin(), new_dictionary.end());

    return new_dictionary;
}

vector<string> better_solution(string random_word, vector<pair<string, string>> new_dictionary) {
    sort(random_word.begin(), random_word.end()); //与えられた文字列をソート

    //二分探索
    vector<string> anagram;
    int left = 0, right = static_cast<int>(new_dictionary.size()) - 1;
    while (right >= left) {
        int mid = left + (right - left) / 2;
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

    ifstream dictionary_input;
    dictionary_input.open("words_small.txt", std::ios::in); //後々words.txtに直す
    string reading_line;
    vector<string> old_dictionary;
    while(getline(dictionary_input, reading_line)){
        old_dictionary.push_back(reading_line);
    }

    vector<pair<string, string>> new_dictionary = make_new_dictionary(old_dictionary);

    vector<string> ans = better_solution (random_word, new_dictionary);

    for(int i = 0; i < static_cast<int>(ans.size()); i++) {
        cout << ans.at(i) << endl;
    }
}
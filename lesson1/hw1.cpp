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
        int mid = (right + left) / 2;
        if (new_dictionary.at(mid).first == random_word) {
            for(int i = mid; i >= 0; i--) {
                if(new_dictionary.at(i).first == random_word) {
                    anagram.push_back(new_dictionary.at(i).second);
                } else {
                    break;
                }
            }
            for(unsigned long int i = mid+1; i < new_dictionary.size(); i++) {
                if(new_dictionary.at(i).first == random_word) {
                    anagram.push_back(new_dictionary.at(i).second);
                } else {
                    break;
                }
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
    ifstream random_word_input;
    random_word_input.open("test_case.txt", std::ios::in);
    string reading_line;
    vector<string> random_word;
    while(getline(random_word_input, reading_line)){
        random_word.push_back(reading_line);
    }

    //辞書の入力
    ifstream dictionary_input;
    dictionary_input.open("words.txt", std::ios::in);
    vector<string> old_dictionary;
    while(getline(dictionary_input, reading_line)){
        old_dictionary.push_back(reading_line);
    }

    vector<pair<string, string>> new_dictionary = make_new_dictionary(old_dictionary);

    ofstream output("ans.txt");
    for(unsigned long int j = 0; j < random_word.size(); j++) {
        vector<string> ans = better_solution (random_word.at(j), new_dictionary);

        for(int i = 0; i < static_cast<int>(ans.size()); i++) {
            output << ans.at(i) << " ";
        }
        output << endl;
    }
    
}
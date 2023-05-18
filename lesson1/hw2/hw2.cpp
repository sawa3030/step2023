#include <bits/stdc++.h>

using namespace std;

map<char, int> score_map = {
    {'a', 1},
    {'b', 3},
    {'c', 2},
    {'d', 2},
    {'e', 1},
    {'f', 3},
    {'g', 3},    
    {'h', 1},
    {'i', 1},
    {'j', 4},
    {'k', 4},
    {'l', 2},
    {'m', 2},
    {'n', 1},
    {'o', 1},
    {'p', 3},
    {'q', 4},
    {'r', 1},
    {'s', 1},
    {'t', 1},
    {'u', 2},
    {'v', 3},
    {'w', 3},
    {'x', 4},
    {'y', 3},
    {'z', 4}
};

map<char, int> alphabet_number = {
    {'a', 0},
    {'b', 1},
    {'c', 2},
    {'d', 3},
    {'e', 4},
    {'f', 5},
    {'g', 6},    
    {'h', 7},
    {'i', 8},
    {'j', 9},
    {'k', 10},
    {'l', 11},
    {'m', 12},
    {'n', 13},
    {'o', 14},
    {'p', 15},
    {'q', 16},
    {'r', 17},
    {'s', 18},
    {'t', 19},
    {'u', 20},
    {'v', 21},
    {'w', 22},
    {'x', 23},
    {'y', 24},
    {'z', 25}
};

vector<vector<int>> make_new_dictionary (vector<string> dictionary) {
    vector<vector<int>> number_table(dictionary.size(), vector<int>(27));

    for(long unsigned int i = 0; i < dictionary.size(); i++) {
        int score = 0; 
        for(long unsigned int j = 0; j < dictionary.at(i).length(); j++) {
            char character = dictionary.at(i).at(j);
            number_table.at(i).at(alphabet_number.at(character)) ++;
            score += score_map.at(character);
        }
        number_table.at(i).at(26) = score;
    }

    return number_table;
}

int better_solution(string random_word, vector<vector<int>> new_dictionary) {
    vector<int> counted_random_word(26);

    for(long unsigned int i = 0; i < random_word.size(); i++) {
        char character = random_word.at(i);
        counted_random_word.at(alphabet_number.at(character))++;
    }

    int ans_score = 0;
    int ans_num = -1;
    for(long unsigned int i = 0; i < new_dictionary.size(); i++) {
        bool ans = true;
        for(int j = 0 ; j < 26; j++) {
            if(new_dictionary.at(i).at(j) > counted_random_word.at(j)) {
                ans = false;
                break;
            }
        }
        if(ans && new_dictionary.at(i).at(26) > ans_score) {
            ans_num = static_cast<int>(i);
            ans_score = new_dictionary.at(i).at(26);
        }
    }

    return ans_num;
}

struct counted_word {
    string word;
    vector<int> num_of_char;
    int score = 0;

    bool operator<(const counted_word& another) const {
        return score > another.score;
    }
};

vector<counted_word> make_newer_dictionary (vector<string> dictionary) {
    vector<counted_word> new_dictionary(dictionary.size());

    for(long unsigned int i = 0; i < dictionary.size(); i++) {
        vector<int> number_table (26, 0);
        int score = 0; 
        for(long unsigned int j = 0; j < dictionary.at(i).length(); j++) {
            char character = dictionary.at(i).at(j);
            number_table.at(alphabet_number.at(character)) ++;
            score += score_map.at(character);
        }
        new_dictionary.at(i).word = dictionary.at(i);
        new_dictionary.at(i).num_of_char = number_table;
        new_dictionary.at(i).score = score;
    }

    sort(new_dictionary.begin(), new_dictionary.end());

    return new_dictionary;
}

string faster_solution(string random_word, vector<counted_word> new_dictionary) {
    vector<int> counted_random_word(26);

    for(long unsigned int i = 0; i < random_word.size(); i++) {
        char character = random_word.at(i);
        counted_random_word.at(alphabet_number.at(character))++;
    }

    int ans_num = -1;
    for(long unsigned int i = 0; i < new_dictionary.size(); i++) {
        bool ans = true;
        for(int j = 0 ; j < 26; j++) {
            if(new_dictionary.at(i).num_of_char.at(j) > counted_random_word.at(j)) {
                ans = false;
                break;
            }
        }
        if(ans) {
            return new_dictionary.at(i).word;
        }
    }

    return "";
}

int main () {
    //random_wordへの入力
    ifstream random_word_input;
    random_word_input.open("medium.txt", std::ios::in);
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

    /*
    vector<vector<int>> new_dictionary = make_new_dictionary(old_dictionary);  

    //出力
    ofstream output("medium_answer.txt");
    for(unsigned long int i = 0; i < random_word.size(); i++) {
        int ans_num = better_solution(random_word.at(i), new_dictionary);

        if(ans_num == -1){
            output << "no answer" << endl;
        } else {
            string ans = old_dictionary.at(ans_num);
            output << ans << endl;
        }
    }
    */    

    vector<counted_word> newer_dictionary = make_newer_dictionary(old_dictionary);
    
    for(unsigned long int i = 0; i < newer_dictionary.size(); i++) {
        cout << newer_dictionary.at(i).word << " ";
        for (int j = 0; j < 26; j++) {
            cout << newer_dictionary.at(i).num_of_char.at(j) << " ";
        }
        cout << newer_dictionary.at(i).score << endl;
    }

    ofstream output("medium_answer.txt");
    for(unsigned long int i = 0; i < random_word.size(); i++) {
        string ans = faster_solution(random_word.at(i), newer_dictionary);
        output << ans << endl;
    }
}
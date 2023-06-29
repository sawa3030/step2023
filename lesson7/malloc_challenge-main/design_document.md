## 第7週目宿題
‐ best-fit mallocやfree list binを実装し、mallocの性能向上を計る

### 様々な方法と考察
- simple_malloc
    - 最初に見つけた空き領域を用いる方法で、既に実装されていたもの
    - 結果(Time[ms]とUtilization[%]について)
        - Challenge #1: 22ms, 70%
        - Challenge #2: 12ms, 40%
        - Challenge #3: 181ms, 8%
        - Challenge #4: 43687ms, 16%
        - Challenge #5: 35451ms, 15%

- best-fit
    - 必要なメモリのサイズよりも大きい空き領域を持つものの中で最も空き領域が小さいものを選択する
    - 結果(Time[ms]とUtilization[%]について)
        - Challenge #1: 1855ms, 70%
        - Challenge #2: 1162ms, 39%
        - Challenge #3: 1398ms, 51%
        - Challenge #4: 12230ms, 72%
        - Challenge #5: 38494ms, 72%
    - 考察
        - 全体的にtimeもutilizationも改善しているが、Challenge #1 ~ #3ではむしろ時間がかかっている
        - Challenge #1 ~ #3 では比較的データサイズの分散が小さいので、最初に見つけた空き領域を使うfirst fitでも無駄が出にくく、むしろ最適な空き領域を探し当てるために全ての空き領域を精査することが必要であるbest fitの方が非効率的になってしまっていると考えられる


- worst fit
    - 常に最も大きい空き領域を使用する
    - 結果(Time[ms]とUtilization[%]について)
        - Challenge #1: 1957ms, 70%
        - Challenge #2: 1185ms, 39%
        - Challenge #3: 89838ms, 4%
        - Challenge #4: 1302306ms, 7%
        - Challenge #5: 1126273ms, 7%
    - 考察
        - 予想通り、time、utilization共に悪化した
        - ただ、Challenge #1, #2に関しては、全ての空き領域を探索しているためにtimeが長くなっているものの、utilizationはfirst fitからほとんど変化していない。これはChallenge #1と#2のデータサイズの分散が小さいため、ほぼ全ての空き領域が同じような状態（大きさ）にあるからだと考えられる

- free list bin
    - 空き領域のサイズごとに異なるリストを作った
    - binの種類が4つの場合
    - 各free listの空き領域のサイズは0~999, 1000~1999, 2000~2999, 3000~3999と1000区切りにした
    - best fitと合わせた結果が以下の通り
    - 結果(Time[ms]とUtilization[%]について)
        - Challenge #1: 1924ms, 70%
        - Challenge #2: 1132ms, 39%
        - Challenge #3: 1341ms, 51%
        - Challenge #4: 8095ms, 72%
        - Challenge #5: 6254ms, 72%
    - 考察
        - best fit単独の時と比べてtimeは多少改善したが、変化は小さい
        - 空き領域の分け方が適当でなかったと考えられる
        - 例えばbinの種類が多ければ、探索する範囲が小さくなる可能性は高くなるので、binの数を大きく増加させる方法が有効なのではないかと考えた

    - binの種類を100個にしたとき（各free listの区切りは40ごと）
    - 結果(Time[ms]とUtilization[%]について)
        - Challenge #1: 2613ms, 70%
        - Challenge #2: 2140ms, 39%
        - Challenge #3: 1692ms, 51%
        - Challenge #4: 759ms, 72%
        - Challenge #5: 1476ms, 72%
    - 考察
        - Challenge #4 ~ #5で予想通りの劇的な改善が見られた
        - しかし、best fitのみと比較して、Challenge #1 ~ #3ではtimeが悪化している
        - Challenge #1 ~ #3のsizeは分散が小さく、そもそも細かい区切りがあまり意味をなしていないこと、そしてfree listの数が増えたことでlistの中身が存在しないfree listを見る手間が増えたことが要因ではないかと考えた。

    - Challenge1で使われるデータはsizeが比較的小さいものが多いためsizeが小さい領域をより細かく分割するために、2の累乗で区切りをした
    - binの種類は12個、n番目のfree listは2^(n-1) ~ 2^nのsizeの空き領域のリストとした
    - 結果(Time[ms]とUtilization[%]について)
        - Challenge #1: 2345ms, 70%
        - Challenge #2: 2183ms, 39%
        - Challenge #3: 1241ms, 51%
        - Challenge #4: 1788ms, 72%
        - Challenge #5: 2079ms, 72%
    - 考察
        - 100個のbinを用意した時に比べると、全体的にtime, utilizationの値は悪化したものの、Challenge #1ではtimeが早くなった
        ‐ 空のfree listが少なくなったため、探索のときに無駄が少なくなったからではないかと考えた

- testについて
       - testを追加し、できるだけ動作が簡略なtestでバグを見つけられるようにした
       - 具体的には、my_mallocの使用、2回目以降のmy_mallocで異なるメモリが確保されているか、新たにOSからメモリを確保したときにメモリが正しく確保されているか、メモリの解放が解放したメモリ以外への影響を及ぼさないか、などを確認した
        
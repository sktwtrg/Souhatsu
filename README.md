souhatsu.py 本体
score_board.py スコア画面管理

GUI に渡すjson
type kyoku の始め　点数、dora
type 自分or相手が切った時、切ったハイ、リーチ棒, button
type 自分or相手がないた時、泣いたハイ,pon or minkan or ankan, button
type 積もった時、 自分or相手, つもはい, button
type 上がった時、上がった人、hand
    
{type : initial,
data :{ ophandnum:int,
    opfuro:{type:'pon', contents:[str]},
    opriver:[str],
    opscore:int,
    hand:[str],
    furo:{type:'pon', contents:[str]},
    score:int,
    ribou:('up', 'bottom'),
    dora : 2
    }
}
    
    
TODO

    ルール部分
        役完成
            河底
            海底
            イペイコ
            ちゃんかん
        ドラ実装
        本場実装
        フリテン実装***(時間かかりそう)
        リー棒のやり取り実装
        流局実装

    GUI関連
        field上に親子表示
        山表示（ドラなど）
        scoreboard点数表示部分(役満の時付はいらない・他の役表示もいらない)
        トビ履歴作る

    実装関連
        Hand Analyzer作る？
        GUI
            位置情報などファイルにまとめて管理

            hand.pyにHandクラスを作り直す
                entitiesをどうする--いちいちhandとentitiesをいじらんとあかん
                いじるとき
                    ツモのとき、鳴きのとき、捨てるとき（Fieldでやってる）
                HaiのsurfaceはEnumにしていい
https://github.com/cookpad/2018-newgrads-engineer-portfolio
            まずはHandからGui部分消して、hand.pyにまとめる

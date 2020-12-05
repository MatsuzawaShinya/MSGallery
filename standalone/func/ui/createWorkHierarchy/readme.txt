「CreateWorkHierarchy」
● GUI
    ・作成のタブと編集のタブを用意
        ・作成
            新規に追加する場合に使用する。
                実行する内容は「● コピーする際に変更する箇所」を参照
            実行内容はwidgetinfo.jsonに追記する。
                ・バックアップ機能も搭載する
        ・編集
            既に作成された情報を編集する
                .jsonファイルを参照（widgetinfo.json）
                編集前と編集した内容をミラーリングし、実行出来るようにする。
                    ・バックアップ機能も搭載する
● コピーする際に変更する箇所
    ■ .bat
        バッチファイルの名前

    ■ __init__.py
        特になし

    ■ func.py
        getAboutInfoの内容
        'release' : '9999/99/99', -> 今日の日付へ
        'update'  : '9999/99/99', -> 今日の日付へ
            「'9999/99/99'」の部分は編集しやすい文字列に変える？
            TemplateClassNames -> 指定したクラス名へ

    ■ ui.py
        クラス名を変更
            TemplateClassNames -> 指定したクラス名へ

    ■ json
        ウィジェット起動に必要な辞書データを追記
            CreateWorkHierarchyで指定したパラメータを参照しアップデートする方式

        "keynames" : {
            起動するウィジェットのフォルダ名。[str]
            
            "start"  : "True",
                mastemaに表示するかどうか。[bool]
            "order"  : 10,
                mastemaに表示させる順番。低いほど最初に来る。[int]
                    指定した数が既に使用されている場合は文字色を変えるなどして警告を出す
            "name"   : "ImageExporter",
                起動するウィジェットクラス名。[str]
                    基本的にkeynamesに使用した名前の先頭が大文字になるようになる。
                        imageExporter -> ImageExporter, renamer -> Renamer
                    keynamesから情報を取得し自動的にセットする。
            "size"   : [280,250],
                初回起動時のウィンドウデフォルトサイズ。[list[int,int]]
            "drop"   : "True"
                ファイルドロップの許可。[bool]
        }

● 別途準備するもの
    ・アイコン
    
● その他
    パスの取得について
        ../standalone/lib/template を参照する。
            ・相対的の場合
                フォルダ階層が変わらない事が前提で、起動したGUI位置から逆算する
                    → 階層を何回があがるため、どこかにマスターデータを置き
                       dirを上がる回数を記憶させておく？
                    →「standalone」が固定とするならば、dirを上がって確定させるのもあり？
                ※ 絶対指定は階層を変えると機能しなくなるので不採用
                
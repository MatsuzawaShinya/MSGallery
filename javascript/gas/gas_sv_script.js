/*---------------------------------------------------------------------------------------------
// common setting
*/
var __DEBUG__ = false;
var _UND_ = undefined;
var menuName = 'sv_menu';
var cellWeith = 60;
var colorIndexList = {
  'ave_1-2':'#FFFCCC', //平均1-2間色
  'ave_2-3':'#FFE8D1', //平均2-3間色
  'ave_3-4':'#FFD1D1', //平均3-4間色
  'ave_4-5':'#EC8686', //平均4-5間色
  'card_L' :'#DFC8DF', //レジェンド色
  'card_G' :'#FDEABD', //ゴールド色
  'card_S' :'#F2F2F2', //シルバー色
  'card_B' :'#E9A68A', //ブロンズ色
  'heading':'#BBDD77', //見出しの深緑色
  'エルフ':'#AADDAA',
  'ロイヤル':'#FFFFCC',
  'ウィッチ':'#99CCFF',
  'ドラゴン':'#FFDD99',
  'ネクロマンサー':'#DDBBEE',
  'ヴァンパイア':'#FFCCCC',
  'ビショップ':'#FEFEFE',
  'ネメシス':'#DDDDDD',
  'other'  :'#000000'
};

var _getActiveSheet = function(){
    return SpreadsheetApp.getActiveSheet();
}
var _getActiveSpreadsheet = function(){
    return SpreadsheetApp.getActiveSpreadsheet();
}
var _GAS_ = function(){
  return _getActiveSheet();
}
var _GASS_ = function(){
  return _getActiveSpreadsheet();
}

var __print = function(w){
  Logger.log(String(w));
}

var _tmp = function(){
  __print(1111);
}

var digitConversion = function(word,len,suf,connectType){
  if(word==_UND_){
    return '';
  }
  if(len==_UND_){
    len = 2;
  }
  var suffix  = '';
  var wd      = String(word);
  var sw      = ((suf)?suf:'0');
  var wd_len  = wd.length;
  var fix_len = (Number(len)-wd_len);
  for(var _i=0;_i<fix_len;_i++){
    suffix += sw;
  }
  return ((wd_len<len)?(((connectType)?(word+suffix):(suffix+word))):word);
}
var getDate = function(){
  var _data = new Date();
  var y = String(_data.getFullYear());
  var m = digitConversion(String(_data.getMonth()+1));
  var d = digitConversion(String(_data.getDate()));
  return (String(y+'/'+m+'/'+d));
}
var getTime = function(){
  var _data = new Date();
  var h = digitConversion(String(_data.getHours()));
  var m = digitConversion(String(_data.getMinutes()));
  var s = digitConversion(String(_data.getSeconds()));
  return (String(h+':'+m+':'+s));
}

/*---------------------------------------------------------------------------------------------
// main func
*/

function _main(){
  var resultmsg = Browser.msgBox('confirmation','アンケートを収集しますか？',Browser.Buttons.OK_CANCEL);
  if(resultmsg=='cancel'){
    return;
  }
  if(__DEBUG__){
    var yn = ('テストシート '+getTime());
  }else{
    var yn = Browser.inputBox('シート名入力',
      "このシートをもとに作成される新しいシートの名前を入力してください",
      Browser.Buttons.OK_CANCEL);
    if(yn=='cancel'){
      return;
    }
  }
  var baseSheet = _GAS_();
  // コピー範囲を指定
  var last_row = baseSheet.getLastRow();
  var last_clm = baseSheet.getLastColumn();
  var startPoint = convertA1NotationMain(1,1);
  var lastPoint  = convertA1NotationMain(last_row,last_clm);
  
  // コピー先のシート作成
  var newsheet = insertSheetLast(yn);
  // コピー(転置して貼り付け)
  baseSheet.getRange(startPoint+':'+lastPoint).copyTo(newsheet.getRange(startPoint),SpreadsheetApp.CopyPasteType.PASTE_VALUES,true);
  // タイムスタンプ(１行目)は不要なので削除
  newsheet.deleteRow(1);
  // カード名列の幅調整
  newsheet.getRange(1,1).setValue('カード名／項目');
  newsheet.setColumnWidth(1,350);
  // タイトル用の行挿入
  newsheet.insertRows(1,1);
  newsheet.getRange(1,1)
    .setValue('【'+yn+'】集計結果')
    .setFontSize(24)
    .setFontWeight('bold');
  // 項目センター寄せ
  newsheet.getRange(2,1).setHorizontalAlignment('center');
  
  // 集計用の列を挿入
  var insertPos = 2;
  var insertNum = 3;
  newsheet.insertColumns(insertPos,insertNum);
  
  // カード名とその他アンケートの位置を取得
  var card_start  = _UND_; //カード名開始位置
  var card_end    = _UND_; //カード名終了位置
  var other_start = _UND_; //その他項目開始位置
  var other_end   = _UND_; //その他項目終了位置
  // カード名からスタート(var i=3)
  for(var i=3;i<=newsheet.getMaxRows();i++){
    var cell = newsheet.getRange(i,1);
    var cv = cell.getValue();
    // 空セルを取得した場合は処理抜ける
    if(cv.length==0){
      other_end = (i-1);
      break;
    }
    var reg = cv.match(/^.+\[.：.+\]$/);
    // ヒットした(カード名)の場合
    if(reg){
      if(card_start==_UND_){
        card_start = i;
      }
    // それ以外(別途アンケート)の場合
    }else{
      if(other_start==_UND_){
        card_end = (i-1);
        other_start = i;
      }
    }
  }
  if(__DEBUG__){
    __print('card_start : '+card_start);
    __print('card_end : '+card_end);
    __print('other_start : '+other_start);
    __print('other_end : '+other_end);
  }
  
  // カード名カラーリング条件付き書式設定
  var s_range = newsheet.getRange(
    convertA1NotationMain(card_start,1)+':'+convertA1NotationMain(card_end,1));
  var allRules = newsheet.getConditionalFormatRules();
  for(var alh of ['L','G','S','B']){
    var s_rule = SpreadsheetApp.newConditionalFormatRule()
      .whenTextContains(alh+'：')
      .setBackground(colorIndexList['card_'+alh])
      .setRanges([s_range])
      .build();
      allRules.push(s_rule);
  }
  newsheet.setConditionalFormatRules(allRules);
  
  // 評価値設定
  var classAverageValueDict = {};
  var insertDict = [
    [2,'平均値',  'AVERAGE','0.00'],
    [3,'最頻値',  'MODE',   '0'],
    [4,'標準偏差','STDEV',  '0.00']
  ];
  var nsl = newsheet.getLastColumn();
  for(var i=0;i<insertNum;i++){
    var c_index = insertDict[i][0];
    var c_func  = insertDict[i][2];
    var c_decimal = insertDict[i][3];
    newsheet.getRange(2,c_index)
      .setValue(insertDict[i][1])
      .setBackground(colorIndexList['heading'])
      .setHorizontalAlignment('center')
    newsheet.setColumnWidth(i+insertPos,cellWeith);
    
    var cells = newsheet.getRange(card_start,c_index,(card_end-card_start+1),1);
    var setRangeList = [];
    for(var y=0;y<cells.getValues().length;y++){
      var s_pos = convertA1NotationMain((y+card_start),(insertPos+insertNum));
      var e_pos = convertA1NotationMain((y+card_start),nsl);
      setRangeList.push([String('='+c_func+'($'+s_pos+':$'+e_pos+')')]);
    }
    cells
      .setNumberFormat(c_decimal)
      .setHorizontalAlignment('center')
      .setValues(setRangeList);
    
    // averageの列を条件付き書式でカラーリング
    if(i==0){
      var allRules = newsheet.getConditionalFormatRules();
      for(var y=1;y<=4;y++){
        var s0 = y;
        var s1 = y+1;
        var s_rule = SpreadsheetApp.newConditionalFormatRule()
          .whenNumberBetween(s0,s1)
          .setBackground(colorIndexList[('ave_'+s0+'-'+s1)])
          .setRanges([cells])
          .build();
          allRules.push(s_rule);
      }
      newsheet.setConditionalFormatRules(allRules);
    }
  }
  var setBorgerRange = newsheet.getRange(
    insertPos,1,(card_end-1),(insertPos+insertNum-1));
  setBorgerRange.setBorder(true,true,true,true,true,true);
  
  // その他のアンケート項目を設定
  // 評価者点数の平均設定
  var add = 1
  var userAverageRow = other_start;
  newsheet.insertRows(other_start,add);
  other_start += add;
  other_end   += add;
  var setrange = newsheet.getRange(userAverageRow,2);
  setrange
    .setValue('評価者の平均点数')
    .setBackground(colorIndexList['heading'])
    .setHorizontalAlignment('center')
    .setBorder(true,true,true,true,true,true);
  newsheet.getRange(userAverageRow,2,1,3).merge();
  var userColumnRange = (newsheet.getLastColumn()-(insertPos+insertNum));
  var setUserAverageRange = [];
  for(var i=0;i<=userColumnRange;i++){
    var ind_s = ((insertPos+insertNum)+i);
    var functxt = ('=AVERAGE('+
      convertA1NotationMain(card_start,ind_s)+':'+
      convertA1NotationMain(card_end,ind_s)  +')');
    setUserAverageRange.push(functxt);
  }
  newsheet.getRange(
      userAverageRow,(insertPos+insertNum),1,(setUserAverageRange.length))
    .setValues([setUserAverageRange])
    .setNumberFormat('0.00')
    .setBackground('#E2E2E2')
    .setHorizontalAlignment('center');
  
  // 交互の背景色設定
  newsheet.getRange(
    card_start,insertPos,(card_end-card_start+1),(newsheet.getLastColumn()-insertPos+1)
  ).applyRowBanding(SpreadsheetApp.BandingTheme.LIGHT_GREY,false,false);
  
  // ohter項目の設定
  var otherValueList = [];
  var src_range = newsheet.getRange(other_start,1,(other_end-other_start+1),1);
  var dst_range = newsheet.getRange(other_start,4,(other_end-other_start+1),1);
  dst_range
    .setValues(src_range.getValues())
    .setHorizontalAlignment('right');
  src_range.clear();
  // otherグラフを作成
  var g_offset = 1;
  for(var i=other_start;i<=other_end;i++){
    var titleGraphIndex = 4;
    var graphRange = newsheet.getRange(
      i,titleGraphIndex,1,(newsheet.getLastColumn()-titleGraphIndex+1));
    var gt = graphRange.getValues()[0][0];
     
    // タイトルを修正
    var r_gt = gt.match(/^.\）(.+$)/);
    var s_gt = ((r_gt)?r_gt[1]:gt);
    newsheet.getRange(i,titleGraphIndex).setValue(s_gt);
    
    if(!gt.match(/^G\）/)){
      continue;
    }
    var c = newsheet.newChart()
      .setChartType(Charts.ChartType.PIE)
      .addRange(graphRange)
      .setPosition(i,titleGraphIndex,0+(g_offset*10),10)
      .setOption('title',s_gt)
      .setNumHeaders(1)
      .setTransposeRowsAndColumns(true)
      .build();
    newsheet.insertChart(c);
    g_offset += 1;
  }
  
  // クラス毎のaverage値を集計し反映
  var cells = newsheet.getRange(card_start,1,(card_end-card_start+1),2);
  var cellValues = cells.getValues();
  var classAverageValueList = {};
  for(var i=0;i<cellValues.length;i++){
    var classname = cellValues[i][0].match(/(^.+)[ 　]\[.：.+\]$/)[1];
    if(!classAverageValueList[classname]){
      classAverageValueList[classname] = [];
    }
    classAverageValueList[classname].push(cellValues[i][1]);
  }
  var setValueList = [];
  setValueList.push(['タイプ別評価平均点','']);
  for(var s in classAverageValueList){
    var d = classAverageValueList[s];
    var ave_value = String(d.reduce(function(a,x){return a+x;})/d.length);
    setValueList.push([s,ave_value]);
  }
  var classTypeStartPos = (other_end+4);
  var cells = newsheet.getRange(classTypeStartPos,1,setValueList.length,2);
  cells
    .setValues(setValueList)
    .setNumberFormat('0.00')
    .setHorizontalAlignment('center')
    .setBorder(true,true,true,true,true,true); //(top,left,bottom,right,vertival,horizontal)
  for(var i=(classTypeStartPos+1);i<(classTypeStartPos+setValueList.length);i++){
    var targetcell = newsheet.getRange(i,1);
    targetcell.setBackground(colorIndexList[targetcell.getValue()]);
  }
  
  // 名前欄のリサイズ
  var max = newsheet.getLastColumn();
  // .setColumnWidths(スタート位置,スタート位置から変更する列の位置,変更するセルの大きさ)
  newsheet.setColumnWidths((insertPos+insertNum),(max-(insertPos+insertNum-1)),(cellWeith-10));
  
  // 表示の固定
  newsheet.setFrozenColumns(4);
  newsheet.setFrozenRows(2);
  
  // 新しいシートにアクティブ合わせ
  newsheet.activate();
}

/*---------------------------------------------------------------------------------------------
// sub func
*/
/*----------------------------------------
// シート取得
*/
var getNowSheet = function(){
  return checkSheetName(_GASS_().getSheetName());
}
var getNowSheetName = function(){
  return _GASS_().getSheetName();
}
/*----------------------------------------
// シートを確認
*/ 
var checkSheetName = function(name){
  var ck = _GASS_().getSheetByName(name);
  if(ck){
    return ck;
  }else{
    return _UND_;
  }
}
/*----------------------------------------
// シート取得
*/ 
var getAllSheet = function(){
  return sheets = _GASS_().getSheets();
}
// シート数取得
var getSheetNum = function(){
  return _GASS_().getNumSheets();
}
/*----------------------------------------
// シート挿入
*/ 
var insertSheet = function(name,index){
  // indexが未設定の場合現在シートの次に挿入
  if(index==_UND_){
    return _GASS_().insertSheet(name);
  // -1以下の場合は末尾に挿入
  }else if(index<=-1){
    return _GASS_().insertSheet(name,getSheetNum());
  // それ以外はindex位置に挿入
  }else{
    return _GASS_().insertSheet(name,index);
  }
}
// シート末尾に挿入
var insertSheetLast = function(name){
  return _GASS_().insertSheet(name,getSheetNum());
}
/*----------------------------------------
// シートコピー
*/
var copySheet = function(baseSheetName,dstSheetName){
  var ck = checkSheetName(baseSheetName);
  if(ck==_UND_){
    return;
  }
  var dst = ck.copyTo(_GASS_());
  dst = dst.setName(dstSheetName);
  return dst;
}
var copyNowSheet = function(dstSheetName){
  return copySheet(_GASS_().getSheetName(),dstSheetName);
}
/*----------------------------------------
// シート削除
*/
var deleteSheet = function(name){
  var ck = checkSheetName(name);
  if(ck){
    _GASS_().deleteSheet(ck);
  }
}
var deleteNowSheet = function(){
  var sheetNowIndex = _GAS_().getIndex();
  deleteSheet(_GASS_().getSheetName());
  // 削除した後一つ前のシートをアクティブに
  if(sheetNowIndex!=1){
    var allsheet = getAllSheet();
    // 非表示シートは除外する
    for(var i=0;i<allsheet.length;i++){
      var activesheet = allsheet[sheetNowIndex-(2+i)];
      if(!activesheet.isSheetHidden()){
        activesheet.activate();
        break;
      }
    }
  }
}

/*----------------------------------------
// セル番地をA1等の形式に変換する
*/ 
var convertA1NotationMain = function(row,column){
  return _GAS_().getRange(row,column).getA1Notation();
}
var convertA1Notation = function(cell){
  return convertA1NotationMain(cell.getRow(),cell.getColumn());
}
var nowCellConvert = function(){
  return convertA1Notation(_GAS_().getActiveCell());
}

/*---------------------------------------------------------------------------------------------
// menu func
*/

var deleteMenu = function(){
  _GASS_().removeMenu(menuName);
}
var execute = function(){
  _main();
}

var createMenu = function(){
  var ui = SpreadsheetApp.getUi();
  ui.createMenu(menuName)
    .addItem(('+++ '+getDate()+' '+getTime()+' +++'),'_tmp')
    .addSeparator()
    .addItem('アンケート結果を収集','execute')
    .addItem('今のシートを削除','deleteNowSheet')
    .addSeparator()
    .addItem('メニューをアップデート','createMenu')
    .addItem('メニューを削除', 'deleteMenu')
    .addSubMenu(
      ui.createMenu('Sub menu')
        .addItem('A','_tmp')
        .addItem('B','_tmp')
    )
    .addToUi();
}

/*---------------------------------------------------------------------------------------------
// シートを開いた時に自動的にスクリプトを実行する
*/
function onOpen(){
  createMenu();
}

/*---------------------------------------------------------------------------------------------
// startup
*/
function svQuestionnaireFunc_startupMenu(){
  createMenu();
}

/*---------------------------------------------------------------------------------------------
// memo
*/

var _memo = function(){
  var sss = SpreadsheetApp.getActiveSheet().getActiveCell();
  //sss.setBackground('#E9967A'); // ブロンズ
  //sss.setBackground('#BBDD77');
}

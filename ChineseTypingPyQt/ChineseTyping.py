# Chinese typing program PyQt Port
# Powered by Qt, Python
# Form made by QtDesigner
# Program writen by Bob Pan 2023.02 - 
# Coding on Ubuntu 22.10
# And these tools: 
# Appimage python 3.5
# PyQt5(Qt 5.6.3) complied by myself and install into appimage
# fcitx-qt5 plugin complied by myself(Fix input method can't be enabled in the app)

from PyQt5 import QtWidgets, QtGui, QtCore
from MainWin import Ui_MainWindow
from ScoreWin import Ui_ScoreWindow
from string_compare import string_compare_line
from os.path import expanduser, join, isfile
import datetime
from traceback import format_exc

# Global vars
ui = Ui_MainWindow()    # Main UI
scui = Ui_ScoreWindow()  # Score Ui
listModel = QtCore.QStringListModel()
listQ_count = 0     # The lines of the article
rem_sec = 600       # The remain time
sel_sec = 600       # Selection time
stat_start = False  # Start stat
typTimer = QtCore.QTimer()  # Timer
artlist = []        # Answer's list
wrtMessage = ""     # Messages to be write
cTime = datetime.datetime.now() # Timestamp
rFileName = ""      # File name for record


DEBUG = False
# Debug Print
def debugPrint(*args):
    if DEBUG:
        print("DEBUG:", end=" ")
        for arg in args:
            print(arg, end=" ")
        print()

# Change Article
def chArtClicked():
    # Pick article
    debugPrint("Choosing article...")
    # For safe disable start btn
    ui.testToggle.setEnabled(True)
    # Open dialog
    fileName = QtWidgets.QFileDialog.getOpenFileName(MainWindow, "Open File",
                                       "./",
                                       "題目文字檔 (*.txt)")
    # Make sure file choosed
    if not(fileName[0] == ''):
        debugPrint("File name:", fileName[0])
        err = False
        try:
            # Record filename
            global rFileName
            rFileName = fileName[0]
            # Read file
            art_file = open(fileName[0], mode='r', encoding='UTF-8')
            # artlist is global
            global artlist
            # Update list view
            artlist = []
            lcnt = 0
            for art_line in art_file:
                artlist.append(art_line.replace('\n', ''))
                lcnt += 1
            #debugPrint(artlist)
            listModel.setStringList(artlist)
            ui.artListView.setModel(listModel)
        except UnicodeDecodeError:
            # Decode error(Format not correct)
            debugPrint("ERROR! UnicodeDecodeError")
            QtWidgets.QMessageBox.critical(MainWindow, "解碼失敗", "請檢查\n* 是否使用UTF-8編碼儲存題目文字檔\n* 檔案是否完整\n" + format_exc())
            err = True
        if not err:
            # Finally sucess read
            debugPrint("File can be read.")
            ui.testToggle.setEnabled(True)
            # listQ_count is global
            global listQ_count
            listQ_count = lcnt
            art_file.close()
    else:
        debugPrint("Canceled selection.")


# Selection method https://stackoverflow.com/questions/15777159/how-do-i-set-the-selection-in-a-listview
def updateArtsel(sel = int()):
    # CreateIndex: row, column
    qindex = listModel.createIndex(sel, 0)
    # Clear old selection
    ui.artListView.clearSelection()
    # Hightlight current line
    ui.artListView.selectionModel().select(qindex, QtCore.QItemSelectionModel.Select)
    # Scroll to current line's postion
    ui.artListView.scrollTo(qindex, QtWidgets.QAbstractItemView.PositionAtBottom)

# Line follow method
# Get line num
def txtCurChanged():
    # Get the number no
    lineno = ui.plainTextEdit.textCursor().blockNumber()
    debugPrint("Now moved to line", lineno, "/", listQ_count - 1)
    if(lineno < listQ_count):
        # Select the line you are typing
        updateArtsel(lineno)
    else:
        debugPrint("WARN: This line over the article!")
        rep = QtWidgets.QMessageBox.question(MainWindow, "已經達到最後一行", "是否交卷？", 
                                             QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel, QtWidgets.QMessageBox.Ok)
        if rep == QtWidgets.QMessageBox.Ok:
            typTimer.stop()
            check_typing(False)

# Time combo picked
def timeComboPicked():
    # Get the selection
    debugPrint("Change the test time to:", ui.timeCombo.currentIndex(), ",", ui.timeCombo.currentText())
    timeMin = int(ui.timeCombo.currentText().replace("分鐘", ""))
    # rem_sec and sel_sec is global var.
    global rem_sec, sel_sec
    rem_sec = timeMin * 60
    sel_sec = rem_sec
    uiTimerUpdate()

# Update UI's timer
def uiTimerUpdate():
    # Make sure no floating point and calculate time
    u_min = str(int(rem_sec / 60)).zfill(2)
    u_sec = str(int(rem_sec % 60)).zfill(2)
    ui.remLabel.setText(u_min + ":" + u_sec)

# Checking Method
# Most same as the WX's version
def check_typing(times_up = bool()):
    # 2 list for userinput and answer
    user_input = []
    answer_art = []
    total_incorrect = 0
    total_need_type = 0
    total_cleartype = 0

    # Clear result plainText
    scui.resultText.clear()
    # Notice checking stat
    debugPrint("Checking...")
    # 時間到的話，看使用者輸入了幾行，否則檢查全部。
    if times_up:
        max_line = ui.plainTextEdit.blockCount()
    else:
        max_line = listQ_count

    # Extract user input
    usertxt = ui.plainTextEdit.toPlainText().split("\n")

    # debugPrint("ans =", answer_art)
    # debugPrint("usr =", usertxt)

    # 將文字儲存成陣列
    for line_no in range(0, max_line):
        # 取出文字
        debugPrint("Getting line", str(line_no))
        # 取出答案的一行字
        answer_art.append(artlist[line_no])
        # 取出作答的一行字
        current_line = usertxt[line_no]
        # 遇到空行要判斷
        if current_line == '':
            # 使用者來不及打的行，就把答案那(最後)行刪掉
            if line_no == (max_line - 1):
                answer_art.pop(line_no)
                max_line = max_line - 1
            else:
                # 否則就增加空行(使用者跳行)
                user_input.append('')
        else:
            # 否則就新增那行的字(一般情況)
            user_input.append(current_line)
            
    debugPrint("ans(" + str(len(answer_art)) + ") =", answer_art)
    debugPrint("usr(" + str(len(user_input)) + ") =", user_input)

    # 逐行批閱
    # return：
    # 0 answer_show = 顯示在richbox的答案行
    # 1 userin_show = 顯示在richbox的輸入行
    # 2 mark_index = 需要標顏色的index
    # 3 err_point = 總扣擊數
    # 4 correct_type = 正確字數
    # 5 line_need_text = 須輸入字數

    for line_no in range(max_line):
        res = []
        # 使用者來不及打完就不要檢查到最後。
        if (line_no == max_line - 1) and (times_up):
            debugPrint('Times up, dont check to the end.')
            res = string_compare_line(answer_art[line_no], user_input[line_no], True)
        else:
            res = string_compare_line(answer_art[line_no], user_input[line_no], False)
        
        # 放上題目
        # 因QT全形空格無法以HTML正確顯示，故使用方框符號代替全形空格顯示
        scui.resultText.appendPlainText(res[0].replace("　", "□"))

        append_text = ""
        markflag = False
        for pos in range(len(res[2])):
            # res[1] = 整理過得答案
            # 需在res[2]提到需要標注的地方放上html tag
            current_text = res[1][pos]
            # 偵測到需標注的字
            if res[2][pos]:
                if not markflag:
                    # 前一個字沒有被標注，所以放上opening tag
                    append_text += "<span style=\"background: red; color: white\">"
                    markflag = True
            else:
                if markflag:
                    # 前一個字被標注，現在這個字沒有，所以放上closing tag
                    append_text += "</span>"
                    markflag = False
            # 放上應該放的文字(取代符號)
            append_text += current_text.replace(" ", "&nbsp;").replace("　", "□")
        # 結束後確認marking flag有沒有被放下(最後一個字還是要被marking，這時候不會產生closing tag)
        if(markflag):
            append_text += "</span>"
        # 新增處理好的作答文字
        scui.resultText.appendHtml(append_text)

        # 批閱結果顯示
        append_text = '<br /> ^^ 第 ' + str(line_no + 1) + ' 行批閱結果 ^^ <br />'
        append_text = append_text + '淨字數: 正確字數(' + str(res[4]) + ')'
        remain_correct = res[4] - (res[3] * 0.5)
        # 淨字數不小於0
        if remain_correct < 0:
            remain_correct = 0
        total_cleartype = total_cleartype + remain_correct  # 淨字數統計
        append_text = append_text + ' - (錯誤次數(' + str(res[3]) + ') * 0.5) => ' + str(remain_correct)
        append_text = append_text + ' | 應輸入字數: ' + str(res[5])
        total_incorrect = total_incorrect + res[3]  # 總錯誤數
        total_need_type = total_need_type + res[5]  # 應輸入字數
        # 套上格式並放上ui
        append_text = "<small>" + append_text + "</small><br />"
        scui.resultText.appendHtml(append_text)
        
    # 結果行顯示
    global sel_sec, rem_sec
    append_text = '測驗結果: \n'
    
    use_time = sel_sec - rem_sec
    append_text = append_text + '用時: ' + str(use_time) + ' 秒\n'
    avg_type = round(total_cleartype / (use_time / 60), 2)
    append_text = append_text + '平均字數: ' + str(avg_type) + ' 字/分鐘\n'
    err_rate = round((total_incorrect / total_need_type) * 100 ,2)
    append_text = append_text + '錯誤率: ' + str(err_rate) + ' %'
    if err_rate > 10.0:
        append_text = append_text + '(無效)'
    else:
        # 分級
        append_text += "\n"
        if(avg_type >= 80):
            append_text += "(已達TQC中文輸入\"專業級\"標準！)"
        elif(avg_type >= 30):
            append_text += "(已達TQC中文輸入\"進階級\"標準！)"
        elif(avg_type >= 15):
            append_text += "(已達TQC中文輸入\"實用級\"標準！)"
    # 新增至UI
    scui.resultText.appendPlainText(append_text)
    # 放入紀錄檔
    global wrtMessage
    wrtMessage = append_text

    # 顯示視窗
    ScoreWindow.exec()

    # Change ui's stat
    ui.chArt_Btn.setEnabled(True)
    ui.timeCombo.setEnabled(True)
    ui.testToggle.setText("開始測驗")
    ui.plainTextEdit.setEnabled(False)
    ui.plainTextEdit.clear()
    global stat_start
    stat_start = False
    # Reset timer
    rem_sec = sel_sec
    uiTimerUpdate()

# On timer tick
def timerTick():
    # rem_sec, stat_start is global
    global rem_sec, stat_start
    # Decrease time
    rem_sec -= 1
    # Update time shown
    uiTimerUpdate()
    if rem_sec <= 0:
        debugPrint('Times Up')
        # Stop timer
        typTimer.stop()
        # Block input
        ui.plainTextEdit.setEnabled(False)
        QtWidgets.QMessageBox.information(MainWindow, "哎呀", "時間到！")
        check_typing(True)

# Control buttom function
def controlbtnClick():
    # stat_start, rem_sec is global
    global stat_start, rem_sec
    if stat_start:
        # Stop timer
        typTimer.stop()
        # Change ui's stat
        ui.chArt_Btn.setEnabled(True)
        ui.timeCombo.setEnabled(True)
        ui.testToggle.setText("開始測驗")
        ui.plainTextEdit.setEnabled(False)
        stat_start = False
        # Reset timer
        rem_sec = sel_sec
        uiTimerUpdate()
    else:
        # Start timer
        typTimer.start()
        # Select first line
        updateArtsel(0)
        # Change ui's stat
        ui.chArt_Btn.setEnabled(False)
        ui.timeCombo.setEnabled(False)
        ui.testToggle.setText("停止測驗")
        ui.plainTextEdit.setEnabled(True)
        # Clear old input
        ui.plainTextEdit.clear()
        # Focus to input
        ui.plainTextEdit.setFocus()
        stat_start = True
        # Timestamp
        global cTime
        cTime = datetime.datetime.now()

def saveBtnClicked():
    # Get home dir and filename
    dist = join(expanduser("~"), "TypingScore.txt")
    try:
        # Generate message
        wrtText = "═════════════════════════\n"
        wrtText += "測驗時間：" + cTime.strftime("%Y/%m/%d %H:%M:%S") + "\n"
        wrtText += "測驗檔案：" + rFileName + "\n"
        wrtText += "─────────────────────────\n"
        wrtText += wrtMessage + "\n"
        # If have file append to the file
        if isfile(dist):
            scFile = open(dist, "a", encoding="UTF-8")
        else:
            scFile = open(dist, "w", encoding="UTF-8")
        scFile.write(wrtText)
        scFile.close()
    except Exception:
        # Have exception
        QtWidgets.QMessageBox.critical(ScoreWindow, "寫入失敗", "請檢查文字檔\"" + dist + "\"是否能正常讀寫\n" + format_exc())
    finally:
        # Successfully write
        QtWidgets.QMessageBox.information(ScoreWindow, "完成", "寫入\"" + dist + "\"成功！")
        ScoreWindow.close()

def discardClicked():
    rep = QtWidgets.QMessageBox.question(ScoreWindow, "確定放棄成績", "放棄成績嗎？\n此次成績將不會寫到文字檔內。", 
                                             QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
    if(rep == QtWidgets.QMessageBox.Yes):
        ScoreWindow.close()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    # Init main form
    MainWindow = QtWidgets.QMainWindow()
    ui.setupUi(MainWindow)
    # Init result form
    ScoreWindow = QtWidgets.QDialog()
    scui.setupUi(ScoreWindow)
    # Article btn click event
    ui.chArt_Btn.clicked.connect(chArtClicked)
    # Cursor move event
    ui.plainTextEdit.cursorPositionChanged.connect(txtCurChanged)
    # Time combo picked event
    ui.timeCombo.currentIndexChanged.connect(timeComboPicked)
    # Toggle btn click event
    ui.testToggle.clicked.connect(controlbtnClick)
    # Save btn click event
    scui.saveBtn.clicked.connect(saveBtnClicked)
    # Discard btn click event
    scui.discardBtn.clicked.connect(discardClicked)
    # Timer tick event
    typTimer.timeout.connect(timerTick)
    # Set timer's interval
    typTimer.setInterval(1000)
    # Set timer type: https://doc.qt.io/qt-6/qt.html#TimerType-enum
    typTimer.setTimerType(0)
    # Disable start test button
    ui.testToggle.setEnabled(False)
    # Time select default index
    #ui.timeCombo.setCurrentIndex(4)
    # Only can select one row
    ui.artListView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
    # Disable user input
    ui.plainTextEdit.setEnabled(False)
    MainWindow.show()
    sys.exit(app.exec_())

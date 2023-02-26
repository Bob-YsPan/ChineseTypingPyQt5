# Chinese Typing PyQt5
Chinese typing software rewrite in the PyQt5

這個Repo包括了打包前的文件以及製作時的UI檔案與程式碼的另一份備份，絕大多數的程式邏輯皆為從[wxChineseTypingSoftware](https://github.com/Bob-YsPan/wxChineseTypingSoftware)加以修改而成。

## 自行使用其他函式版本打包

### 需準備(最後面括號為本Repo使用的版本)：

1.  [python-appimage](https://github.com/niess/python-appimage)，選擇需要的appimage下載即可 [3.5]
2.  [PyQt5原始碼](https://sourceforge.net/projects/pyqt/files/PyQt5/)(需要新版的可以自行編譯) [5.4.1]  
    PyQt5編譯時需先編譯[sip](https://sourceforge.net/projects/pyqt/files/sip/) [4.16.6]
3.  [QT](https://download.qt.io/archive/qt/)，到歷史版本載需要的版本即可 [5.6.3]
4.  [fcitx5-qt](https://github.com/fcitx/fcitx5-qt)，整合系統的Fcitx輸入法 [latest(5.0.16)]

### 編譯過程概述(以下指令請依照自己環境修改引數)

1.  先對Python的appimage使用`--appimage-extract`解出檔案
2.  將sip解開到與appimage解開後的squashfs-root相同目錄下，並且使用以下指令編譯  
    ```
    $ ../squashfs-root/opt/python3.5/bin/python3.5 configure.py
    $ make
    $ make install
    ```
    編譯好應該會直接講sip安裝到解開的appimage裡面
3.  將QT的安裝`.run`檔賦予執行權限後，點開安裝(會是圖形的安裝程式)到與squashfs-root資料夾同目錄下的`QT56`資料夾(QT僅需安裝gcc的工具以及無法取消句選的即可，不需要安裝其他功能！)
4.  解開PyQt5的原始碼至squashfs-root相同目錄下，使用以下指令編譯  
    ```
    $ ../squashfs-root/opt/python3.5/bin/python3.5 configure.py --sip="../squashfs-root/opt/python3.5/bin/sip" --qmake="../QT56/5.6.3/gcc_64/bin/qmake"
    $ make
    $ make install
    ```
5.  

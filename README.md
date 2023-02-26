# Chinese Typing PyQt5
Chinese typing software rewrite in the PyQt5

這個Repo包括了製作時的UI檔案與程式碼，絕大多數的程式邏輯皆為從[wxChineseTypingSoftware](https://github.com/Bob-YsPan/wxChineseTypingSoftware)加以修改而成。  
如果需針對整個環境進行修改，可以使用`--appimage-extract`指令獲得開發環境修改好再打包回去

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
    ```shell
    $ ../squashfs-root/opt/python3.5/bin/python3.5 configure.py
    $ make
    $ make install
    ```
    編譯好應該會直接講sip安裝到解開的appimage裡面
3.  將QT的安裝`.run`檔賦予執行權限後，點開安裝(會是圖形的安裝程式)到與squashfs-root資料夾同目錄下的`QT56`資料夾(QT僅需安裝gcc的工具以及無法取消句選的即可，不需要安裝其他功能！)
4.  解開PyQt5的原始碼至squashfs-root相同目錄下，使用以下指令編譯  
    ```shell
    $ ../squashfs-root/opt/python3.5/bin/python3.5 configure.py --sip="../squashfs-root/opt/python3.5/bin/sip" --qmake="../QT56/5.6.3/gcc_64/bin/qmake"
    $ make
    $ make install
    ```
    安裝好這步的同時會在你編譯用的QT目錄下(這裡是`QT56/5.6.3/gcc_64/bin/`)產生一個designer的執行檔，可以使用這個工具修改需要的UI文件  
    完成後使用指令進行更新(以下指令假設ui檔在squashfs-root相同路徑下)  
    如果需要編譯程式進入點，則需要多加`-x`引數  
    ```shell
    $ ./squashfs-root/opt/python3.5/bin/python3.5 -m PyQt5.uic.pyuic MainWin.ui -o MainWin.py
    ```
5.  編譯輸入法整合：先在`CMakeLists.txt`大概第7行(有set指令那邊)進行修改
    ```cmake
    # 新增這五行set
    set(Qt5_DIR (你的QT目錄)/5.6.3/gcc_64/lib/cmake/Qt5)
    set(Qt5Core_DIR (你的QT目錄)/5.6.3/gcc_64/lib/cmake/Qt5Core)
    set(Qt5Gui_DIR (你的QT目錄)/5.6.3/gcc_64/lib/cmake/Qt5Gui)
    set(Qt5Widgets_DIR (你的QT目錄)/5.6.3/gcc_64/lib/cmake/Qt5Widgets)
    set(Qt5DBus_DIR (你的QT目錄)/QT56/5.6.3/gcc_64/lib/cmake/Qt5DBus)

    find_package(ECM 1.4.0 REQUIRED)

    set(CMAKE_MODULE_PATH ${ECM_MODULE_PATH} ${CMAKE_CURRENT_SOURCE_DIR}/cmake)
    
    # 這邊的option調整成這個狀態，只編譯需要的東西
    option(ENABLE_QT4 "Enable Qt 4" Off)
    option(ENABLE_QT5 "Enable Qt 5" On)
    option(ENABLE_QT6 "Enable Qt 6" Off)
    option(BUILD_ONLY_PLUGIN "Build only plugin" On)
    option(BUILD_STATIC_PLUGIN "Build plugin as static" Off)
    option(WITH_FCITX_PLUGIN_NAME "Enable plugin name with fcitx" On)
    ```
6.  如果使用的是舊版的QT(例如5.6)，修改fcitx-qt5這邊解開的資料夾下`qt5/platforminputcontext/qfcitxplatforminputcontext.cpp`，找到500多行像這樣的內容
    ```cpp
        if (proxy) {
        proxy->focusIn();
        // We need to delegate this otherwise it may cause self-recursion in
        // certain application like libreoffice.
        QMetaObject::invokeMethod(
            this,
            [this, window = QPointer<QWindow>(lastWindow_)]() {
                if (window != lastWindow_) {
                    return;
                }
                update(Qt::ImHints | Qt::ImEnabled);
                updateCursorRect();
            },
            Qt::QueuedConnection);
        }
    ```
    修改成這樣(新版QT可能不需要)
    ```cpp
        if (proxy) {
            cursorRectChanged();
            proxy->focusIn(); 
        }
    ```
    接下來進到原始碼的資料夾內，使用以下指令編譯
    ```shell
    $ cmake . --fresh
    $ make
    ```
7.  fcitx-qt5原始碼的資料夾下`qt5/platforminputcontext/`應該可以找到`libfcitx5platforminputcontextplugin.so`，複製到appimage解開後的`squashfs-root/opt/python3.5/lib/python3.5/site-packages/PyQt5/Qt/plugins/platforminputcontexts`資料夾下(QT以後的資料夾要自己創建)，同時複製QT安裝路徑資料夾下`5.6.3/gcc_64/plugins/platforminputcontexts`(5.6.3是你安裝的版本)，的兩個`.so`檔案到同樣資料夾下

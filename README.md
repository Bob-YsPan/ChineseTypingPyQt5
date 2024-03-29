# Chinese Typing PyQt5
Chinese typing software rewrite in the PyQt5

這個Repo包括了製作時的UI檔案與程式碼，絕大多數的程式邏輯皆為從[wxChineseTypingSoftware](https://github.com/Bob-YsPan/wxChineseTypingSoftware)加以修改而成。  
  
macOS電腦目前沒辦法那麼快取得，因此macOS的打包作業與單一執行檔會需要等待一陣子後推出　　

## 相比舊版優勢

1.  盡量做到各大平台都能夠打包成獨立運作的檔案(Linux採用Appimage、Windows使用Pyinstaller)
2.  使用Qt5並改寫大量視窗程式(沿用舊版批閱方式)，獲得更佳的輸入法整合性
3.  增加儲存成績功能(將成績單部分內容儲存在個人資料夾下的文字檔)，以記錄個人學習狀態
4.  **v1.1之後統一讀取UTF-8格式的題目(以免遇到不同系統的編碼問題)**

## 題庫

*   請參考[ChineseTypingArticles](https://github.com/Bob-YsPan/ChineseTypingArticles)底下的題庫與來源參考，有空會再製作更多的題庫供使用者運用。
*   亦可自己建立題庫，建議使用全部全型字，單行32個全型字(含空格)，建立UTF-8編碼的文字檔

## 截圖展示

* Windows 11  
  ![Windows 11 01](https://user-images.githubusercontent.com/46966555/223390068-8273927d-2f3f-4e68-92e2-781728531f12.png)
* Windows XP  
  ![Windows XP 01](https://user-images.githubusercontent.com/46966555/223389999-41c46298-acaa-49a7-9abd-62d1fee279fa.PNG)
  ![Windows XP 02](https://user-images.githubusercontent.com/46966555/223390020-89644278-740b-491e-a287-ba9b80a37674.PNG)
* Ubuntu MATE Dark Theme(Linux)  
  ![Ubuntu MATE 01](https://user-images.githubusercontent.com/46966555/223390239-227d77af-3ee9-4441-9619-b3f0eb31024a.png)
* macOS Catalina  
  ![macOS Catalina](https://user-images.githubusercontent.com/46966555/224923074-c7e01aa5-3aa1-4faa-8e6e-be12403160f5.png)
* Manjaro Linux Dark theme  
  ![Manjaro Linux](https://user-images.githubusercontent.com/46966555/226096520-fc31e292-fbde-4063-9532-ab05d1f406ca.png)

## 給Linux使用者的建議 Tips For Linux User

1.  請先降版成Fcitx 4，全形字元的支援度比較完整(Fcitx 5的Chewing還缺乏小鍵盤跟全形框架)
2.  設定可以打開這三個選項，會得到垂直型態的候選列表(跟Windows體驗比較類似)跟懸浮工具列　　
    ![未命名](https://user-images.githubusercontent.com/46966555/225788357-db12ef53-7c6e-4bde-90cc-c5e3fa89d568.png)　　
    ![未命名2](https://user-images.githubusercontent.com/46966555/225788381-4e8a78fe-5e02-4693-b6cc-50239c644cac.png)　　
3.  找個可以輸入中文的地方，按下`Ctrl + Alt + B`呼叫出螢幕小鍵盤，切換成**全形字元**鍵盤備用，半全形切換請切換成全型  
    ![螢幕截圖2023-03-17 09-27-16](https://user-images.githubusercontent.com/46966555/225788815-42a66033-d3d3-4630-bf5c-6bc24ffef7d2.png)  
    ![未命名3](https://user-images.githubusercontent.com/46966555/225789199-7737ef96-2a27-4c07-afa3-322b01cab5f8.png)　　
4.  打字時，直接按下空白鍵即可輸入全形空格，使用`Ctrl + Alt + B`輸入全形英文跟符號(類似Windows新注音在英數+全形字的情況下)，輸入完成再按一次`Ctrl + Alt + B`即可回到中文模式

## 給macOS使用者的建議 Tips For macOS User

1.  由於macOS原生的注音輸入法可以輸入全形英數，第三方的輸入框架不見得可以(例如我測試時使用[威注音](https://vchewing.github.io/README.html))，建議兩套輸入法都準備一下
2.  打字前先依序把原生注音輸入法跟第三方輸入法都切換一次(`Control + 空白鍵`)，之後開始打字，威注音的話可以透過`Shift + 空白鍵`輸入全形空格，當需要輸入全形符號或數字時，透過按一次`Control + 空白鍵`暫時切換到macOS原生的注音輸入法輸入，之後再按一次切換回來

## 打包方式(Linux)

### Linux下如果不須更換Python版本等只須小修改內容，可以使用`--appimage-extract`指令獲得開發環境修改好再打包回去 

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

## 打包方式(Windows，python 3.4，兼容Windows XP SP3的打包法)

### 需準備

1.  [PyInstaller 3.4](https://pypi.org/project/pyinstaller/3.4/#files)(From pypi)
2.  [pywin32 220](https://sourceforge.net/projects/pywin32/files/pywin32/Build%20220/pywin32-220.win-amd64-py3.4.exe/download)(From SourceForge)
3.  [PyQt5 5.4.1 32bit](https://sourceforge.net/projects/pyqt/files/PyQt5/PyQt-5.4.1/PyQt5-5.4.1-gpl-Py3.4-Qt5.4.1-x32.exe/download)(From SourceForge)
4.  Python 3.4.4(虛擬環境或是安裝包皆可)

### 打包步驟(以PowerShell為例)

#### 建立虛擬環境

*   virtualenv需要下載沒有新增新版python語法的舊版本
*   `--no-download`避免建立環境時去下載新版pip造成錯誤

```
> python -m pip install virtualenv==14.0.6
> python -m virtualenv --no-download pyqtwin-venv
> .\pyqtwin-venv\Scripts\activate.ps1
```

#### 安裝PyQt5(路徑須選在你的virtualenv下)

![image](https://user-images.githubusercontent.com/46966555/223384729-fde27e60-677b-42ce-9173-efe39f160e4d.png)

![image](https://user-images.githubusercontent.com/46966555/223384773-0dcceddb-5f80-46dc-8673-4e25fb43ee87.png)

#### 安裝pywin32

這裡使用virtualenv下的python完成(須執行上面"建立虛擬環境"步驟的*activate.ps1*，命令列前面會出現`(虛擬環境名)`)

```
> easy_install-3.4.exe .\pywin32-220.win32-py3.4.exe
```

#### 編譯、安裝pyinstaller

*   首先先將pyinstaller的tar.gz包解開成資料夾，並透過`cd`指令進入該資料夾
*   需要解決依賴問題(Python 3.4 不支援fstring等新語法)，因此先透過pip預先安裝舊版pefile

````
> cd PyInstaller-3.4
> pip install pefile==2019.04.18
> python .\setup.py install
````

#### 打包

*   先將這個github的原始碼解壓縮一份，並進到該解壓的資料夾

```
> cd .\ChineseTypingPyQt
```

*   將Qt的plugins從virtualenv底下的site-package複製一份到C槽下  
    `剛剛建立虛擬環境的資料夾 > pyqtwin-venv > Lib > site-packages > PyQt5 > plugins` `複製到 C:\Qt\5.4.1 下`

![image](https://user-images.githubusercontent.com/46966555/223387603-52c5a8ab-7bc2-4142-af78-532f0d8218d4.png)

*   執行打包指令

```
> pyinstaller.exe -F .\ChineseTyping.py
```

*   如果出現錯誤，檢查有沒有像底下的錯誤訊息，把剛剛複製過去的plugin資料夾移動到錯誤訊息提示的路徑下

```
Exception:
            Cannot find existing PyQt5 plugin directories
            Paths checked: C:/Qt/5.4.1/plugins
```

*   指令順利完成後，應該可以在資料夾中的`dist`資料夾內找到打包好的單個`.exe`執行檔

![image](https://user-images.githubusercontent.com/46966555/223388902-e7303e81-f10b-481d-9da8-877f1261a3f8.png)

## 打包方式(macOS Catalina，python 3.5)

### 需準備

1.  [Command Line Tools for Xcode 11.5](https://download.developer.apple.com/Developer_Tools/Command_Line_Tools_for_Xcode_11.5/Command_Line_Tools_for_Xcode_11.5.dmg)(From Apple Developers site，需要登入)
2.  [Python 3.5.4](https://www.python.org/downloads/release/python-354/)(From Python Site)


### 更新pip(python 3.5的舊版pip已經不堪使用)

```
curl https://bootstrap.pypa.io/pip/3.5/get-pip.py | python3
```

### 打包過程

#### 安裝虛擬環境

```
pip3 install virtualenv
mkdir ChineseTypingQT5

# 將這個repo的檔案下載下來，刪除`.ui`的檔案，解開到`ChineseTypingQt5`資料夾(你剛剛mkdir的資料夾名稱)

cd ChineseTypingQT5
python3 -m virtualenv TypMenv
source TypMenv/bin/activate
```

#### 安裝相關的函式庫

```
pip install PyQt5==5.8.2
pip install py2app==0.25
```

#### 打包

```
py2applet --make-setup ChineseTyping.py
python setup.py py2app
```

即可在dist資料夾下發現打包好的app  
![截圖 2023-03-14 15 08 24](https://user-images.githubusercontent.com/46966555/224922987-35d683b8-90ca-4ab4-a71b-36cbdf952487.png)

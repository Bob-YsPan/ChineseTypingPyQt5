from difflib import ndiff

# define 比較方法

# 丟入：
# answer_str = 一行答案(string)
# userin_str = 一行使用者輸入(string)
# user_last = 是不是使用者輸入的最後一行

# return：
# answer_show = 顯示在richbox的答案行
# userin_show = 顯示在richbox的輸入行
# mark_index = 需要標顏色的index
# err_point = 總扣擊數
# correct_type = 正確字數
# line_need_text = 須輸入字數

DEBUG = False
# Debug Print
def debugPrint(*args):
    if DEBUG:
        print("DEBUG:", end=" ")
        for arg in args:
            print(arg, end=" ")
        print()

def string_compare_line(answer_str = '', userin_str = '', user_last = False):

    # answer = '君不見黃河之水天上來，奔流到海不復回。君不見高堂明鏡悲白髮，朝如青絲暮成雪。'
    # userin = ''

    answer = answer_str
    userin = userin_str

    if answer == userin:
        debugPrint('all correct.')
        mark_index = []
        for index in range(len(answer)): mark_index.append(False)
        return answer, userin, mark_index, 0, len(answer), len(answer)
    else:
        # 幾個變數
        err_point = 0
        answer_show = ''
        userin_show = ''
        mark_index = []
        
        # 用ndiff得出差異處並存入列表
        # 參考：https://stackoverflow.com/questions/17904097/python-difference-between-two-strings/17904977
        diff = ndiff(userin, answer)
        check_list = [[], []]
        for index, stat in enumerate(diff):
            debugPrint('index = ' + str(index) + ' , stat = ' + str(stat[0]) + ' , text = ' + str(stat[-1]))
            if stat[0] == ' ':
                check_list[0].append(0)
            elif stat[0] == '+':
                check_list[0].append(1)
            elif stat[0] == '-':
                check_list[0].append(-1)
            check_list[1].append(stat[-1])
        debugPrint(check_list[0])
        debugPrint(check_list[1])

        # 將列表取出並判斷
        chunk_size = 0
        chunk_end = False  # 這個小區結束的指標
        swap_end = False  # 判斷是否剛剛判斷出了一組顛倒字
        index = 0 # 檢查用的index函數，因為不能用for in range
        last_run = False # 最後一次跑迴圈
        correct_type = 0 # 正確字數
        line_need_text = 0 # 行應輸入字數

        while(index < len(check_list[0])):
            # 出現非0那判斷這區有多大，以及進行顛倒字的判斷
            if not(check_list[0][index] == 0):
                # 出現正就要判斷顛倒字
                if check_list[0][index] > 0:
                    # 是否Out of range
                    if index < (len(check_list[1]) - 2):
                        # 是否是 + _ - 排列，且字相同(顛倒字)
                        if (check_list[0][index + 1] == 0 and check_list[0][index + 2] < 0 and check_list[1][index] == check_list[1][index + 2]):
                            chunk_end = True
                            swap_end = True
                            answer_show = answer_show + check_list[1][index] + check_list[1][index + 1]
                            userin_show = userin_show + check_list[1][index + 1] + check_list[1][index + 2]
                            mark_index.append(True)
                            mark_index.append(True)
                            # 扣分
                            err_point = err_point + 1
                            index = index + 2  # 顛倒字的index跳過
                            debugPrint('Swap occured.')
                            # 統計應輸入字
                            line_need_text = line_need_text + 2
                        else:
                            # 非顛倒字就加chunk size
                            chunk_size = chunk_size + 1
                    else:
                        # 非顛倒字就加chunk size
                        chunk_size = chunk_size + 1
                elif check_list[0][index] < 0:
                    # 漏字就加chunk size
                    chunk_size = chunk_size + 1
            elif(chunk_size > 0):
                # 有chunk且有抓到錯字那就判定是chunk end
                # 這個正確字後面再補加上
                chunk_end = True
            else:
                # 正確區段的話就把字增加上去
                answer_show = answer_show + check_list[1][index]
                userin_show = userin_show + check_list[1][index]
                mark_index.append(False)
                # 統計正確字
                correct_type = correct_type + 1
                # 統計應輸入字
                line_need_text = line_need_text + 1
            # 如果是最後一次迴圈，又有沒有處理的錯誤chunk要舉chunkend，並且增加一個index。
            # 上面如果舉chunk end那則維持原樣(最後一個字是對的)
            debugPrint('now chunk size = ' + str(chunk_size) + ' index = ' + str(index) + ' chunk end = ' + str(chunk_end))
            if (chunk_size > 0) and (index == (len(check_list[0]) - 1)) and (chunk_end == False):
                debugPrint('last_run')
                chunk_end = True
                last_run = True

            # 判定是Chunk End就算有多少錯字或多漏打
            # 看多字跟漏字的量
            if chunk_end:
                # 剛剛有顛倒字(顛倒字會多兩個)
                if swap_end:
                    # 多算那組顛倒字的範圍(前面沒有顛倒字就不算)
                    start_index = index - chunk_size - 2
                    end_index = index - 3
                else:
                    # 最後一次跑要Shift一格
                    if last_run:
                        end_index = index
                        start_index = index - chunk_size + 1
                    else:
                        # 否則算正常的chunk size
                        start_index = index - chunk_size
                        end_index = index - 1

                debugPrint('this chunk: start = ' + str(start_index) + ' end = ' + str(end_index) + ' size = ' + str(chunk_size))
                # 統計這個chunk有多少個多字跟少字，並記index
                # + 代表要多打，為漏字
                # - 代表要刪除，為多字
                more = []
                miss = []
                for index_2 in range(start_index, end_index + 1):
                    debugPrint('cal ' + str(index_2))
                    if check_list[0][index_2] < 0:
                        more.append(index_2)
                    elif check_list[0][index_2] > 0:
                        miss.append(index_2)
                # 相減得非錯字量，再跟大的相減就會得到錯字量
                if len(miss) - len(more) == 0:
                    # 代表全是錯字(數量一樣)
                    debugPrint('all incorrect')
                    for index_3 in miss:
                        answer_show = answer_show + check_list[1][index_3]
                        # mark index只需要一次
                        mark_index.append(True)
                        # 統計應輸入字
                        line_need_text = line_need_text + 1
                        # 扣分
                        err_point = err_point + 1
                    for index_3 in more:
                        userin_show = userin_show + check_list[1][index_3]
                elif len(more) > len(miss):
                    # 代表多打比較多(有真的多打)
                    debugPrint('more text')
                    # 多打的放出來
                    for index_3 in more:
                        userin_show = userin_show + check_list[1][index_3]
                        mark_index.append(True)
                    # 漏打的放出來
                    for index_3 in miss:
                        answer_show = answer_show + check_list[1][index_3]
                        # 扣分(錯字)
                        err_point = err_point + 1
                        # 統計應輸入字
                        line_need_text = line_need_text + 1
                    for index_3 in range(len(more) - len(miss)):
                        answer_show = answer_show + '＃'
                        # 扣分(真正多打)
                        err_point = err_point + 1
                elif len(more) < len(miss):
                    # 代表漏打比較多(有真的漏打)
                    debugPrint('miss text')
                    # 多打的放出來
                    for index_3 in more:
                        userin_show = userin_show + check_list[1][index_3]
                        # 扣分(錯字)
                        err_point = err_point + 1
                    if (user_last):
                        # 取出相同數量的miss就好，迴圈跟別人不一樣
                        # 因為是沒打完的
                        for index_3 in range(len(more)):
                            debugPrint('last_user_line')
                            answer_show = answer_show + check_list[1][miss[index_3]]
                            mark_index.append(True)
                            # 統計應輸入字
                            line_need_text = line_need_text + 1
                    else:
                        # 漏打的放出來(一般情況)
                        for index_3 in miss:
                            answer_show = answer_show + check_list[1][index_3]
                            mark_index.append(True)
                            # 統計應輸入字
                            line_need_text = line_need_text + 1
                        for index_3 in range(len(miss) - len(more)):
                            userin_show = userin_show + 'Ｘ'
                            # 扣分(真正漏打)，補上X
                            err_point = err_point + 1
                # 如果不是因為抓到swap跳進來的，就把最後一個字補上
                if not(swap_end or last_run):
                    answer_show = answer_show + check_list[1][index]
                    userin_show = userin_show + check_list[1][index]
                    mark_index.append(False)
                    # 統計正確字
                    correct_type = correct_type + 1
                    # 統計應輸入字
                    line_need_text = line_need_text + 1
                # 放flag
                swap_end = False
                chunk_end = False
                chunk_size = 0
            debugPrint('index = ' + str(index))
            index = index + 1
        debugPrint(answer_show)
        debugPrint(userin_show)
        debugPrint(mark_index)
        debugPrint('Line Err = ' + str(err_point))
        return answer_show, userin_show, mark_index, err_point, correct_type, line_need_text
# 調用測試
# string_compare_line()

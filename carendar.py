import re #文章を分割するライブラリ
def main():
    youbi = ["  日","  月","  火","  水","  木","  金","  土"]
    month_date = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31] #月ごとの日数
    sum_days = 0 #紀元が始まった時からの日にち
    count = 0 #曜日
    count2 = 1 #日にち
    end = False #システム終了
    yotei_ari = False #その日に予定があるかないか
    
    #システム終了が選択されるまでループ
    while end == False:
        choice = input("カレンダーを見る = 1, 予定を入れる = 2, 予定を見る = 3, 終了 = 4 : ")
        
        #カレンダーを見る#################################################
        if choice == str(1):
            year = int(input("year?: "))
            month = int(input("month?: "))
            
            #予定を書き込んだファイルを読み出して分割する
            f = open("yotei.txt", "r")
            line = re.split('[ \n]',f.read())
            f.close()
            
            #入力した年までの日数を計算
            for i in range(1,year):
                sum_days = sum_days + 365 + uruu(i)
    
            #入力した年の月までの日数を計算
            if uruu(year) == 1:
                month_date[1] += 1
        
            for i in range(0,month-1):
                sum_days += month_date[i]
        
            #カレンダー表示
            print("{0}年 {1}月".format(year,month))
            
            #初日の曜日のずれを修正
            for i in range(0,(sum_days % 7)+1):
                print("{0}".format(youbi[count]))
                count += 1

            #カレンダー出力
            for i in range(1,month_date[month-1]+1):
                #日曜日の時は1行開ける
                if count % 7 == 0: 
                        print(" ")
                 
                #書き込んだ予定を周回する            
                for t in range(0,int((len(line)-1)/4)):
                    yotei_year = int(line[(4*t)])
                    yotei_month = int(line[1+(4*t)])
                    yotei_day = int(line[2+(4*t)])
                    yotei_contents = line[3+(4*t)]
                    
                    #予定日と日にちが一致すれば予定を表示する
                    if year == yotei_year and month == yotei_month and count2 == int(yotei_day):
                        print("{0}  {1} : {2}".format(youbi[count%7],count2,yotei_contents))
                        count += 1
                        count2 += 1
                        yotei_ari = True
                
                    #何も予定がなかったときは日にちだけを表示する        
                if yotei_ari == False:
                    print("{0}  {1}".format(youbi[count%7],count2))
                    count += 1
                    count2 += 1
                yotei_ari = False
            
            #リセット        
            count = 0
            count2 = 1
            month_date[1] = 28
            sum_days = 0
            line.clear()
            continue

        #予定を入れる############################################################
        if choice == str(2):
            year = input("year?: ")
            month = input("month?: ")
            day = input("day?: ")
            contents = input("contents?: ")
            
            #ファイルに書き込む
            f = open("yotei.txt", "a")
            print("{0} {1} {2} {3}".format(year,month,day,contents),file=f)
            f.close()
            continue
        
        #予定を見る################################################################
        if choice == str(3):
            line3 = []
            r2 = 0
            r3 = 0
            saigo = False
            saigo2 = False
            f = open("yotei.txt", "r")
            line2 = f.read()
            f.close()
            #ファイルから予定を読み出す
            line2 = re.split('[ \n]',line2)
            #4つずつに分割する    
            for i in range(0, len(line2), 4):
                line3.append(line2[i: i+4])
            
            #改行を消す    
            line3.pop()
            
            #3次元バブルソート
            #年数でバブルソート
            for i in range(0,len(line3)):
                for t in range(0,len(line3)-1):
                    if int(line3[t+1][0]) < int(line3[t][0]):
                        line3[t],line3[t+1] = line3[t+1],line3[t]
            
            #月でバブルソート
            r = line3[0][0]
            while saigo != True:
                for i in range(0,len(line3)):
                    if int(line3[i][0]) == int(r):
                        r2 += 1
                for m in range(r3,r3+r2):
                    for t in range(r3,r3+r2-1):
                        if int(line3[t+1][1]) < int(line3[t][1]):
                            line3[t],line3[t+1] = line3[t+1],line3[t]
                
                if len(line3) <= r3+r2:
                    saigo = True
                    break
                
                r = line3[r3+r2][0]
                r3 += r2
                r2 = 0
            
            #日でバブルソート
            r = line3[0][0]
            r5 = line3[0][1]
            r3 = 0
            r2 = 0
            while saigo2 != True:
                for i in range(0,len(line3)):
                    if int(line3[i][0]) == int(r) and int(line3[i][1]) == int(r5):
                        r2 += 1
                        
                for m in range(r3,r3+r2):
                    for t in range(r3,r3+r2-1):
                        if int(line3[t+1][2]) < int(line3[t][2]):
                            line3[t],line3[t+1] = line3[t+1],line3[t]
                
                if len(line3) <= r3+r2:
                    saigo2 = True
                    break
                
                r = line3[r3+r2][0]
                r5 = line3[r3+r2][1]
                r3 += r2
                r2 = 0
            
            #予定を表示
            for i in range(0,len(line3)):
                print(*line3[i])
            line3.clear()
            line2.clear()
            continue
        
        #システム終了#########################################################
        if choice == str(4):
            end = True
            break
    
#うるう年かどうか判定する関数    
def uruu(year):
    if (year % 400 == 0) or (year % 4 == 0 and year % 100 != 0):
        return 1
    return 0

main()
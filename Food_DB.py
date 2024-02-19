import numpy as np
import re
import csv
import pandas as pd
import cvxpy as cp

# Calculate daily nutrient intake using Total_Kcal and User_Input
def daily_nutrient_intake(Total_Kcal,User_Input_Gender):
    """
    Input: Total_Kcal, User_Input_Gender
    Return: dictionary of daily nutrient that includes protein, carb, fat, sugar, natrium
    """

    carb_calories = Total_Kcal * 0.5
    protein_calories = Total_Kcal * 0.3
    fat_calories = Total_Kcal * 0.2

    carb_grams = carb_calories / 4
    protein_grams = protein_calories / 4
    fat_grams = fat_calories / 9
    sugar_limit = 37.5 if User_Input_Gender == 'M' else 25
    naturium_limit = 2400

    return {
        'Fd_Protein(g)': protein_grams,
        'Fd_Cbhyd(g)': carb_grams,
        'Fd_Fat(g)': fat_grams,
        'Fd_Sugar(g)': sugar_limit,
        'Fd_Natrium(mg)': naturium_limit,
    }

# Get user's personal information and calculate Total Kcal and daily nutrient
def get_personel_info():
    """
    Input: none
    Output: total_kcal, daily_nutrient
    Get user's personal information.
    Using Harris-Benedict Equeation, calculate Total Kcal that user can eat and daily nutrient that user should intake.

    """
    #입력한 사용자의 신체정보를 토대로 대사량을 계산
    print("------식단관리 프로그램------")
    print("당신의 대사량(Kcal)을 계산하겠습니다.")

    # get user's age
    while True:
        User_Input_Age = input("당신의 나이를 입력하세요: ")
        User_Input_Age= User_Input_Age.strip()

        # validation check - is integer bigger than 0
        if User_Input_Age.isdigit():
            if int(User_Input_Age) > 0:
                break
            else: print("나이는 자연수로 입력되어야 합니다. 다시 입력해주세요.")
        else:
            print("입력한 값은 숫자가 아닙니다. 다시 입력해주세요.")

    # get user's weight 
    while True:
        User_Input_Weight = input("당신의 몸무게를 입력하세요 Kg: ")
        User_Input_Weight = User_Input_Weight.strip()

        # validation check - is float number bigger than 0
        try:
            User_Input_Weight = float(User_Input_Weight)
            if User_Input_Weight > 0:
                break
            else:
                print("몸무게는 0보다 커야합니다. 다시 입력해주세요.")
        except ValueError:
            print("입력한 값은 숫자가 아닙니다. 다시 입력해주세요.")
    
    # get user's height
    while True:
        User_Input_Height=input("당신의 키를 입력하세요 cm: ")
        User_Input_Height=User_Input_Height.strip()

        # validation check - is float number bigger than 0
        try:
            User_Input_Height=float(User_Input_Height)
            if User_Input_Height>0:
                break
            else:
                print("키는 0보다 커야합니다. 다시 입력해주세요.")
        except ValueError:
            print("입력한 값은 숫자가 아닙니다. 다시 입력해주세요.")
    
    # get user's gender
    while True:
        User_Input_Gender = input("당신의 성별을 입력하세요. (남성 또는 여성): ")
        Uesr_Input_Gender= User_Input_Gender.strip()

        # validation check - is in ("남성", "여성")
        if User_Input_Gender in ("남성", "여성"):
            break
        else:
            print("입력한 값은 남성 또는 여성이 아닙니다. 다시 입력해주세요.")

    print(f"당신의 나이는 {User_Input_Age}살 몸무게는 {User_Input_Weight}Kg 성별은 {User_Input_Gender}입니다.")

    # get user's activity type
    while True:
        User_Input_Act_type=input("당신의 활동 유형을 입력하세요. (1: 30분이하 가벼운 활동, 2: 1~2시간 사이 가벼운 활동, 3: 2~4시간 정도의 보통 활동 4: 4시간이상의 심한 활동)\n")
        User_Input_Act_type=User_Input_Act_type.strip()
        if User_Input_Act_type in ("1", "2", "3", "4"):
            break
        else:
            print("입력한 값은 1,2,3,4 중 하나가 아닙니다. 다시 입력해주세요.")

    User_Input_Age = float(User_Input_Age)
    User_Input_Weight = float(User_Input_Weight)
    User_Input_Height = float(User_Input_Height)

    # Calculate Basic_Kcal using Harris-Benedict Equation
    # Using Activity type, gender, weight, height, age
    if User_Input_Gender=="남성":
        # for male
        Basic_Kcal=88.362+(13.397*User_Input_Weight)+(4.799*User_Input_Height)-(5.677*User_Input_Age)
        if User_Input_Act_type=="1":
            Total_Kcal=Basic_Kcal*1.1
        elif User_Input_Act_type=="2":
            Total_Kcal=Basic_Kcal*1.3
        elif User_Input_Act_type=="3":
            Total_Kcal=Basic_Kcal*1.5
        elif User_Input_Act_type=="4":
            Total_Kcal=Basic_Kcal*2.0
        print(f"당신의 총대사량은 {Total_Kcal:.1f}Kcal 입니다.")

    else:
        # for female
        Basic_Kcal=447.593+(9.247*User_Input_Weight)+(3.098*User_Input_Height)-(4.330*User_Input_Age)
        if User_Input_Act_type=="1":
            Total_Kcal=Basic_Kcal*1.1
        elif User_Input_Act_type=="2":
            Total_Kcal=Basic_Kcal*1.3
        elif User_Input_Act_type=="3":
            Total_Kcal=Basic_Kcal*1.5
        elif User_Input_Act_type=="4":
            Total_Kcal=Basic_Kcal*2.0
        print(f"당신의 총대사량은 {Total_Kcal:.1f}Kcal 입니다.")

    daily_nutrient = daily_nutrient_intake(Total_Kcal, User_Input_Gender)

    return Total_Kcal, daily_nutrient


def get_recommended_intake(Total_Kcal, daily_nutrient, detected_food, remaining_meals): 
    """
    Input: daily nutrient and food that user can eat, list of food that detected from image
    Output: recommended intake of each food
    """

    # Read Food_DB to get nutrient information of each food
    df = pd.read_csv('Food_DB.csv', encoding='utf-8')

    df = df[[
        'Fd_Name', 
        'Fd_Kcal', 
        'Fd_Protein', 
        'Fd_fat', 
        'Fd_cbhyd', 
        'Fd_sugar', 
        'Fd_natrium' ]]

    # Dictionary to store nutrient information
    nutrient_info = {
        'Fd_kcal': 0,  # 칼로리
        'Fd_Protein(g)': 0,  # 단백질
        'Fd_Cbhyd(g)': 0,  # 탄수화물
        'Fd_Fat(g)': 0,  # 지방
        'Fd_Sugar(g)': 0,  # 당류
        'Fd_Natrium(mg)': 0,  # 나트륨
    }

    # 최적해에 사용될 A값을 저장할 변수 선언
    A=[]
    input_list = []

    # todo: 사용자가 입력한 음식이 아니라, list를 통해 들어온 입력값을 통해 음식의 양을 추천해야함
    for User_Input_Food in detected_food:
    # while True:
    #     User_Input_Food = input("당신이 먹은 음식은 무엇인가요? (종료하려면 'q'를 입력하세요): ")
    #     if User_Input_Food.lower() == 'q':
    #         break
        # food_row, A에 사용자가 입력한 음식의 정보를 저장=
        if(df.loc[df['Fd_Name'] == User_Input_Food].values.tolist() == []) :
            continue
        food_row = df.loc[df['Fd_Name'] == User_Input_Food]
        A.append( df.loc[df['Fd_Name'] == User_Input_Food].values.tolist()[0][1:])
        input_list.append(User_Input_Food)
        if not food_row.empty:
            # 딕셔너리에 음식의 영양소 정보 저장
            nutrient_info['Fd_kcal'] += food_row['Fd_Kcal'].values[0]
            nutrient_info['Fd_Protein(g)'] += food_row['Fd_Protein'].values[0]
            nutrient_info['Fd_Cbhyd(g)'] += food_row['Fd_cbhyd'].values[0]
            nutrient_info['Fd_Fat(g)'] += food_row['Fd_fat'].values[0]
            nutrient_info['Fd_Sugar(g)'] += food_row['Fd_sugar'].values[0]
            nutrient_info['Fd_Natrium(mg)'] += food_row['Fd_natrium'].values[0]
        else:
            print("입력한 음식을 찾을 수 없습니다.")


    b = np.array([Total_Kcal]+list(daily_nutrient.values()))

    # todo: 3끼로 나누는 것보단 전에 먹은 양을 기준으로 나누는 것이 바람직해 보임
    b = b / remaining_meals

    # list to numpy
    A = np.array(A).T

    x = cp.Variable((len(input_list),1), nonneg=True)

    prob = cp.Problem(cp.Minimize((1/2)*cp.quad_form(x, A.T @ A) - b @ A @ x), [ -x <= 0 ])
    prob.solve()

    return input_list, x

"""
하루에 2~3끼
전체 섭취 권장량 / 3 => 한 끼의 권장량
칼로리만 계산했다? 나머지 영양소는 계산 안하고?

______________________________________________________________________________________________________

한계점 1 - user feedback이 안된다는 점
아침에 좀 무겁게 먹었어 a b c d e f

점심 저녁 전체 섭취 권장량 / 3 
오버가 되어버리는 상황
______________________________________________________________________________________________________

한계점 2 - 추천된 음식의 양이 고르지 못하다는 점
ex)
쌀밥의 권장 섭취량은 242g 입니다.
김치찜의 권장 섭취량은 120g 입니다.
콩나물무침의 권장 섭취량은 0g 입니다.

해결책: 메인메뉴와 사이드메뉴를 구분하고 메인메뉴의 양은 제한을 걸어두고 사이드메뉴의 양은 제한을 걸지 않는다.
"""
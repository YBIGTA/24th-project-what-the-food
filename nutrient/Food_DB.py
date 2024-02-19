import numpy as np
import re
import csv
import pandas as pd
import cvxpy as cp

#function 모음

# 개인의 일일섭취 영양소 정보를 저장하는 함수
def daily_nutrient_intake(Total_Kcal,User_Input_Gender):
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

# 일일섭취영양소와 사용자가 섭취한 영양소를 비교하여 경고 메시지를 출력하는 함수
def check_nutrient_limit(daily_nutrient, User_Input_Food):
    for nutrient, consumed in nutrient_info.items():
        if nutrient in daily_nutrient and consumed > daily_nutrient[nutrient] and nutrient != 'Fd_kcal':
            print(f"Warning:{User_Input_Food}섭취시 1일 섭취 권장 영양소 {nutrient}를 초과하게 됩니다.")

#입력한 사용자의 신체정보를 토대로 대사량을 계산
print("------식단관리 프로그램------")
print("당신의 대사량(Kcal)을 계산하겠습니다.")
while True:
    User_Input_Age = input("당신의 나이를 입력하세요: ")
    User_Input_Age= User_Input_Age.strip() #입력받은 값의 양쪽 공백을 제거
    if User_Input_Age.isdigit(): #나이는 숫자로만 입력받아야하므로 숫자인지 확인
        if int(User_Input_Age) > 0: #나이는 0보다 커야하므로 0보다 큰지 확인
            break
        else: print("나이는 자연수로 입력되어야 합니다. 다시 입력해주세요.")
    else:
        print("입력한 값은 숫자가 아닙니다. 다시 입력해주세요.")
while True:
    User_Input_Weight = input("당신의 몸무게를 입력하세요 Kg: ")
    User_Input_Weight = User_Input_Weight.strip() #입력받은 값의 양쪽 공백을 제거
    try:
        User_Input_Weight = float(User_Input_Weight)
        if User_Input_Weight > 0: # 몸무게는 0보다 커야하므로 0보다 큰지 확인
            break
        else:
            print("몸무게는 0보다 커야합니다. 다시 입력해주세요.")
    except ValueError:
        print("입력한 값은 숫자가 아닙니다. 다시 입력해주세요.")
while True:
    User_Input_Height=input("당신의 키를 입력하세요 cm: ")
    User_Input_Height=User_Input_Height.strip() #입력받은 값의 양쪽 공백을 제거
    try:
        User_Input_Height=float(User_Input_Height)
        if User_Input_Height>0: #키는 0보다 커야하므로 0보다 큰지 확인
            break
        else:
            print("키는 0보다 커야합니다. 다시 입력해주세요.")
    except ValueError:
        print("입력한 값은 숫자가 아닙니다. 다시 입력해주세요.")
while True: #Front에서 성별을 애초에 binary값으로 받도록 해도 좋을 거 같아요
    User_Input_Gender = input("당신의 성별을 입력하세요. (남성 또는 여성): ")
    Uesr_Input_Gender= User_Input_Gender.strip() #입력받은 값의 양쪽 공백을 제거
    if User_Input_Gender in ("남성", "여성"):
        break
    else:
        print("입력한 값은 남성 또는 여성이 아닙니다. 다시 입력해주세요.")
# User_Input값을 출력을 통해 확인한 후, 잘못입력되었으면 다시 입력받도록함 
print(f"당신의 나이는 {User_Input_Age}살 몸무게는 {User_Input_Weight}Kg 성별은 {User_Input_Gender}입니다.")
while True:
    User_Input_Act_type=input("당신의 활동 유형을 입력하세요. (1: 30분이하 가벼운 활동, 2: 1~2시간 사이 가벼운 활동, 3: 2~4시간 정도의 보통 활동 4: 4시간이상의 심한 활동)\n")
    User_Input_Act_type=User_Input_Act_type.strip() #입력받은 값의 양쪽 공백을 제거
    if User_Input_Act_type in ("1", "2", "3", "4"):
        break
    else:
        print("입력한 값은 1,2,3,4 중 하나가 아닙니다. 다시 입력해주세요.")
# 이미 입력받은 문자열 값을 float 형태로 변환
User_Input_Age = float(User_Input_Age)
User_Input_Weight = float(User_Input_Weight)
User_Input_Height = float(User_Input_Height)

# User_Input 데이터를 활용하여 기초대사량을 계산
# B_Kcal계산에서는 개정 Harris-Benedict 방정식 사용, 활동유형에 따라 기초대사량에
if User_Input_Gender=="남성":
    Basic_Kcal=88.362+(13.397*User_Input_Weight)+(4.799*User_Input_Height)-(5.677*User_Input_Age)
    if User_Input_Act_type=="1":
        Total_Kcal=Basic_Kcal*1.1
    elif User_Input_Act_type=="2":
        Total_Kcal=Basic_Kcal*1.3
    elif User_Input_Act_type=="3":
        Total_Kcal=Basic_Kcal*1.5
    elif User_Input_Act_type=="4":
        Total_Kcal=Basic_Kcal*2.0
    print(f"당신의 총대사량은 {Total_Kcal:.1f}Kcal 입니다.") #소수점 첫째자리까지만 출력
else:
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
daily_nutrient = daily_nutrient_intake(Total_Kcal,User_Input_Gender)
print(daily_nutrient)


#사용자가 먹은 음식의 정보를 받아서 영양소 정보를 저장하는 프로그램
# CSV에 저장된 음식 및 영양소 정보 읽어오기
df = pd.read_csv('Food_DB.csv', encoding='utf-8')
# 필요한 열만 선택하여 새로운 DataFrame 생성
df = df[[
    'Fd_Name', 
    'Fd_Kcal', 
    'Fd_Protein', 
    'Fd_fat', 
    'Fd_cbhyd', 
    'Fd_sugar', 
    'Fd_natrium' ]]

# 영양소 정보를 저장할 Dictionary 변수선언
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
while True:
    User_Input_Food = input("당신이 먹은 음식은 무엇인가요? (종료하려면 'q'를 입력하세요): ")
    if User_Input_Food.lower() == 'q':
        break
    # food_row, A에 사용자가 입력한 음식의 정보를 저장
    print(df.loc[df['Fd_Name'] == User_Input_Food].values.tolist())
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
print(A)
b = np.array([Total_Kcal]+list(daily_nutrient.values()))

print(food_row)
print(b)

b = b/3
# list to numpy
A = np.array(A).T
#Todo: 비전을 통해 도출된 음식이름이 우리 DB의 Food_Name 칼럼에 있는지 혹은 같은 음식인데 이름이 다른지 비교하여 DB를 업데이트해야함 
x = cp.Variable((len(input_list),1), nonneg=True)

prob = cp.Problem(cp.Minimize((1/2)*cp.quad_form(x, A.T @ A) - b @ A @ x), [ -x <= 0 ])
prob.solve()

print(x.value)

print("-----------")
for i in range(len(input_list)):
  if x.value[i][0] < 0.01:
    x.value[i][0] = 0
  print('{0}의 권장 섭취량은 {1}g 입니다.'.format(input_list[i], x.value[i][0] * 100))

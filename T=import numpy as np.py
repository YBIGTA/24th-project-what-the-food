import numpy as np
A=np.array([[1,2,3][]])
# 변환 행렬 T 생성
T = np.array([[1, 2], [3, 4]])

# A를 numpy 배열로 변환
A_np = A.values

# 행렬 곱셈을 통해 A를 T로 변환
A_transformed = np.dot(A_np, T)00




#Task1 Xdata 정리
def optimization_nutrient(User_Input_Food, daily_nutrient):
    #A data 정리
    df_user_input = df[df['Fd_Name']==User_Input_Food] #사용자가 입력한 음식의 정보를 저장
    A=df_user_input[[
        'Fd_Protein',
        'Fd_cbhyd',
        'Fd_fat',
        'Fd_sugar',
        'Fd_natrium']].values
    #X data 정리 
    A=A.T #A값 변환
    #b값 받아오기
    b = np.array(list(daily_nutrient.values()))
    return A, b
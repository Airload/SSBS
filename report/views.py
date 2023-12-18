from django.shortcuts import render
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import pandas as pd 
import numpy as np 
import plotly.express as px
import plotly.graph_objects as go
import os, json
from django.conf import settings

# 데이터 불러오기
xlsx_file_path = os.path.join(settings.BASE_DIR, 'static', 'data/20_21_totaldata.xlsx')
data20_21 = pd.read_excel(xlsx_file_path)
xlsx_file_path1 = os.path.join(settings.BASE_DIR, 'static', 'data/20_21_읍면동_인구추이.xlsx')
data20_21_pop = pd.read_excel(xlsx_file_path1)
xlsx_file_path2 = os.path.join(settings.BASE_DIR, 'static', 'data/상단순위.xlsx')
data21_rank = pd.read_excel(xlsx_file_path2)
data21_rank_df = pd.DataFrame(data21_rank)

##리스트 한명과 영문 일치시키기##
gu = ['고운동','금남면','다정동','대평동','도담동','보람동','부강면','새롬동','소담동',
'소정면','아름동','연기면','연동면','연서면','장군면','전동면','전의면','조치원읍','종촌동','한솔동']
gu1 = ['goun','gemnam','dajeung','depyeung','dodam','boram','bugang','serom','sodam',
       'sojeung','areum','yeongi','yeondong','yeonseo','janggun','jeondong','jeonui','jochiwon','jongchong','hansol']

    # 리스트들을 zip으로 압축
zipped_lists =list(zip(gu, gu1))


## 각 순위 디렉토리 뽑기##
# 데이터프레임 생성
df_grouped_population = data21_rank_df.groupby('읍면동')['인구'].sum().reset_index()
df_sorted_population = df_grouped_population.sort_values(by='인구', ascending=False).reset_index(drop=True)
df_sorted_population['순위_인구'] = df_sorted_population.index + 1

df_grouped_sal = data21_rank_df.groupby('읍면동')['총매출'].sum().reset_index()
df_sorted_sal = df_grouped_sal.sort_values(by='총매출', ascending=False).reset_index(drop=True)
df_sorted_sal['순위_총매출'] = df_sorted_sal.index + 1

# 순위 정보를 딕셔너리로 저장
rank_info_dict = {}
for idx, row in df_sorted_population.iterrows():
    rank_info_dict[row['읍면동']] = {'순위_인구': row['순위_인구'], '순위_총매출': df_sorted_sal.loc[df_sorted_sal['읍면동'] == row['읍면동'], '순위_총매출'].values[0]}

# 읍면동 순위를 저장할 딕셔너리 초기화
rank_dict = {'읍면동': [], '최다연령층': []}

# 각 읍면동에 대해 최대값의 열 이름을 찾아서 저장
for index, row in data21_rank_df.iterrows():
    max_column = row[['유년기', '청장년기', '중년기', '노년기']].idxmax()
    rank_dict['읍면동'].append(row['읍면동'])
    rank_dict['최다연령층'].append(max_column)

    # 새로운 키로 딕셔너리에 추가
    rank_info_dict[row['읍면동']]['최다연령층'] = max_column


rank_dict = {'읍면동': [], '최고매출업종': []}

# 각 읍면동에 대해 최대값의 열 이름을 찾아서 저장
for index, row in data21_rank_df.iterrows():
    store_column = row[['슈퍼마켓', '치킨전문점', '커피-음료', '편의점','한식음식점']].idxmax()
    rank_dict['읍면동'].append(row['읍면동'])
    rank_dict['최고매출업종'].append(store_column)

    # 새로운 키로 딕셔너리에 추가
    rank_info_dict[row['읍면동']]['최고매출업종'] = store_column

## 각순위 디렉토리 뽑기 종료##

## 그래프 그리기 ##
# X축 설정
x_values = ['20_1sales', '20_2sales', '20_3sales', '20_4sales', '21_1sales', '21_2sales', '21_3sales', '21_4sales']
fig_list = []
# 각 행 별로 그래프 생성
for index, row in data20_21.iterrows():
    # Y축 설정
    y_values = row[x_values].tolist()

    # 그래프 생성
    fig = go.Figure()
    fig.update_layout(width=1000,height=500)
    fig.add_trace(go.Scatter(x=x_values, y=y_values, mode='lines+markers', name=f'행 {index + 1}'))
    fig.update_layout(yaxis_range=[0, max(y_values) * 1.1])
    fig_list.append(fig)
    # 레이아웃 설정
    fig.update_layout(title=f"{row['region']}- {row['store']} 매출",
                      xaxis_title='분기',
                      yaxis_title='매출액')


selected_columns = data20_21_pop.columns[1:]
selected_columns=selected_columns.tolist()
x_values_pop = selected_columns
fig_pop_list = []
for index_pop, row_pop in data20_21_pop.iterrows():
    # Y축 설정
    y_values_pop= row_pop[x_values_pop].tolist()

    # 그래프 생성
    fig_pop = go.Figure()
    fig_pop.update_layout(width=1000,height=500)
    fig_pop.add_trace(go.Scatter(x=x_values_pop, y=y_values_pop, mode='lines+markers'))
    fig_pop_list.append(fig_pop)
    # 레이아웃 설정
    fig_pop.update_layout(title=f"{row_pop['읍면동']} 인구추이",
                      xaxis_title='년_월',
                      yaxis_title='인구수')

# for문을 통해 각 그래프의 위치와 읍면동명 넣기
for prefix in gu1:
    for i in range(1, 6):
        variable_name = f"{prefix}{i}"
        index = (i - 1) * 20 + gu1.index(prefix) * 1
        globals()[variable_name] = fig_list[index].to_html(full_html=False)

##그래프그리기 종료##



def index(request):
    
     return render(request, 'report/report.html',{'zipped_lists': zipped_lists,'rank_info_dict': rank_info_dict})

def goun(request):
    gounpop = fig_pop_list[0].to_html(full_html=False)
    return render(request, 'report/goun.html', {'goun1': goun1, 'goun2': goun2, 'goun3': goun3, 'goun4': goun4, 'goun5': goun5, 'gounpop': gounpop, 'rank_info': rank_info_dict['고운동']})

def gemnam(request):
    gemnampop = fig_pop_list[1].to_html(full_html=False)
    return render(request, 'report/gemnam.html', {'gemnam1': gemnam1, 'gemnam2': gemnam2, 'gemnam3': gemnam3, 'gemnam4': gemnam4, 'gemnam5': gemnam5, 'gemnampop': gemnampop, 'rank_info': rank_info_dict['금남면']})

def dajeung(request):
    dajeungpop = fig_pop_list[2].to_html(full_html=False)
    return render(request, 'report/dajeung.html', {'dajeung1': dajeung1, 'dajeung2': dajeung2, 'dajeung3': dajeung3, 'dajeung4': dajeung4, 'dajeung5': dajeung5, 'dajeungpop': dajeungpop, 'rank_info': rank_info_dict['다정동']})

def depyeung(request):
    depyeungpop = fig_pop_list[3].to_html(full_html=False)
    return render(request, 'report/depyeung.html', {'depyeung1': depyeung1, 'depyeung2': depyeung2, 'depyeung3': depyeung3, 'depyeung4': depyeung4, 'depyeung5': depyeung5, 'depyeungpop': depyeungpop, 'rank_info': rank_info_dict['대평동']})

def dodam(request):
    dodampop = fig_pop_list[4].to_html(full_html=False)
    return render(request, 'report/dodam.html', {'dodam1': dodam1, 'dodam2': dodam2, 'dodam3': dodam3, 'dodam4': dodam4, 'dodam5': dodam5, 'dodampop': dodampop, 'rank_info': rank_info_dict['도담동']})

def boram(request):
    borampop = fig_pop_list[5].to_html(full_html=False)
    return render(request, 'report/boram.html', {'boram1': boram1, 'boram2': boram2, 'boram3': boram3, 'boram4': boram4, 'boram5': boram5, 'borampop': borampop, 'rank_info': rank_info_dict['보람동']})

def bugang(request):
    bugangpop = fig_pop_list[6].to_html(full_html=False)
    return render(request, 'report/bugang.html', {'bugang1': bugang1, 'bugang2': bugang2, 'bugang3': bugang3, 'bugang4': bugang4, 'bugang5': bugang5, 'bugangpop': bugangpop, 'rank_info': rank_info_dict['부강면']})

def serom(request):
    serompop = fig_pop_list[7].to_html(full_html=False)
    return render(request, 'report/serom.html', {'serom1': serom1, 'serom2': serom2, 'serom3': serom3, 'serom4': serom4, 'serom5': serom5, 'serompop': serompop, 'rank_info': rank_info_dict['새롬동']})

def sodam(request):
    sodampop = fig_pop_list[8].to_html(full_html=False)
    return render(request, 'report/sodam.html', {'sodam1': sodam1, 'sodam2': sodam2, 'sodam3': sodam3, 'sodam4': sodam4, 'sodam5': sodam5, 'sodampop': sodampop, 'rank_info': rank_info_dict['소담동']})

def sojeung(request):
    sojeungpop = fig_pop_list[9].to_html(full_html=False)
    return render(request, 'report/sojeung.html', {'sojeung1': sojeung1, 'sojeung2': sojeung2, 'sojeung3': sojeung3, 'sojeung4': sojeung4, 'sojeung5': sojeung5, 'sojeungpop': sojeungpop, 'rank_info': rank_info_dict['소정면']})

def areum(request):
    areumpop = fig_pop_list[10].to_html(full_html=False)
    return render(request, 'report/areum.html', {'areum1': areum1, 'areum2': areum2, 'areum3': areum3, 'areum4': areum4, 'areum5': areum5, 'areumpop': areumpop, 'rank_info': rank_info_dict['아름동']})

def yeongi(request):
    yeongipop = fig_pop_list[11].to_html(full_html=False)
    return render(request, 'report/yeongi.html', {'yeongi1': yeongi1, 'yeongi2': yeongi2, 'yeongi3': yeongi3, 'yeongi4': yeongi4, 'yeongi5': yeongi5, 'yeongipop': yeongipop, 'rank_info': rank_info_dict['연기면']})

def yeondong(request):
    yeondongpop = fig_pop_list[12].to_html(full_html=False)
    return render(request, 'report/yeondong.html', {'yeondong1': yeondong1, 'yeondong2': yeondong2, 'yeondong3': yeondong3, 'yeondong4': yeondong4, 'yeondong5': yeondong5, 'yeondongpop': yeondongpop, 'rank_info': rank_info_dict['연동면']})

def yeonseo(request):
    yeonseopop = fig_pop_list[13].to_html(full_html=False)
    return render(request, 'report/yeonseo.html', {'yeonseo1': yeonseo1, 'yeonseo2': yeonseo2, 'yeonseo3': yeonseo3, 'yeonseo4': yeonseo4, 'yeonseo5': yeonseo5, 'yeonseopop': yeonseopop, 'rank_info': rank_info_dict['연서면']})

def janggun(request):
    janggunpop = fig_pop_list[14].to_html(full_html=False)
    return render(request, 'report/janggun.html', {'janggun1': janggun1, 'janggun2': janggun2, 'janggun3': janggun3, 'janggun4': janggun4, 'janggun5': janggun5, 'janggunpop': janggunpop, 'rank_info': rank_info_dict['장군면']})

def jeondong(request):
    jeondongpop = fig_pop_list[15].to_html(full_html=False)
    return render(request, 'report/jeondong.html', {'jeondong1': jeondong1, 'jeondong2': jeondong2, 'jeondong3': jeondong3, 'jeondong4': jeondong4, 'jeondong5': jeondong5, 'jeondongpop': jeondongpop, 'rank_info': rank_info_dict['전동면']})

def jeonui(request):
    jeonuipop = fig_pop_list[16].to_html(full_html=False)
    return render(request, 'report/jeonui.html', {'jeonui1': jeonui1, 'jeonui2': jeonui2, 'jeonui3': jeonui3, 'jeonui4': jeonui4, 'jeonui5': jeonui5, 'jeonuipop': jeonuipop, 'rank_info': rank_info_dict['전의면']})

def jochiwon(request):
    jochiwonpop = fig_pop_list[17].to_html(full_html=False)
    return render(request, 'report/jochiwon.html', {'jochiwon1': jochiwon1, 'jochiwon2': jochiwon2, 'jochiwon3': jochiwon3, 'jochiwon4': jochiwon4, 'jochiwon5': jochiwon5, 'jochiwonpop': jochiwonpop, 'rank_info': rank_info_dict['조치원읍']})

def jongchong(request):
    jongchongpop = fig_pop_list[18].to_html(full_html=False)
    return render(request, 'report/jongchong.html', {'jongchong1': jongchong1, 'jongchong2': jongchong2, 'jongchong3': jongchong3, 'jongchong4': jongchong4, 'jongchong5': jongchong5, 'jongchongpop': jongchongpop, 'rank_info': rank_info_dict['종촌동']})

def hansol(request):
    hansolpop = fig_pop_list[19].to_html(full_html=False)
    return render(request, 'report/hansol.html', {'hansol1': hansol1, 'hansol2': hansol2, 'hansol3': hansol3, 'hansol4': hansol4, 'hansol5': hansol5, 'hansolpop': hansolpop, 'rank_info': rank_info_dict['한솔동']})


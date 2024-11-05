import numpy as np
import pandas as pd
from BoCheck import Checker

'''
Test on most frequency syllables in Kangyur, Tengyur, Tibetan news, magazine. 
We sellect 200 two-components syllable, 300 three-components syllable, 300 three-components syllable, 
300 four-components syllable, 300 five-components syllable, 200 six-components syllable, 12 siven-components syllable
'''
recog = Checker()
data = pd.read_csv("data/tibetan_frequency.csv", index_col=0)

syllable_1 = data[data['构件数量'] == 1]
syllable_2 = data[data['构件数量'] == 2]
syllable_3 = data[data['构件数量'] == 3]
syllable_4 = data[data['构件数量'] == 4]
syllable_5 = data[data['构件数量'] == 5]
syllable_6 = data[data['构件数量'] == 6]
syllable_7 = data[data['构件数量'] == 7]

tibetan_components_2 = []
for i in range(min(len(syllable_2), 200)):
    syllable = syllable_2.iloc[i, 0]
    result = recog.recognization_syllable(syllable)
    tibetan_components_2.append(list(result.values()))
tibetan_components_2 = pd.DataFrame(tibetan_components_2, columns=result.keys())
tibetan_components_2.to_csv("syllable_with_2_components.csv")

tibetan_components_3 = []
for i in range(min(len(syllable_3), 300)):
    syllable = syllable_3.iloc[i, 0]
    result = recog.recognization_syllable(syllable)
    tibetan_components_3.append(list(result.values()))
tibetan_components_3 = pd.DataFrame(tibetan_components_3, columns=result.keys())
tibetan_components_3.to_csv("syllable_with_3_components.csv")

tibetan_components_4 = []
for i in range(min(len(syllable_4), 300)):
    syllable = syllable_4.iloc[i, 0]
    result = recog.recognization_syllable(syllable)
    tibetan_components_4.append(list(result.values()))
tibetan_components_4 = pd.DataFrame(tibetan_components_4, columns=result.keys())
tibetan_components_4.to_csv("syllable_with_4_components.csv")

tibetan_components_5 = []
for i in range(min(len(syllable_5), 300)):
    syllable = syllable_5.iloc[i, 0]
    result = recog.recognization_syllable(syllable)
    tibetan_components_5.append(list(result.values()))
tibetan_components_5 = pd.DataFrame(tibetan_components_5, columns=result.keys())
tibetan_components_5.to_csv("syllable_with_5_components.csv")

tibetan_components_6 = []
for i in range(min(len(syllable_6), 200)):
    syllable = syllable_6.iloc[i, 0]
    result = recog.recognization_syllable(syllable)
    tibetan_components_6.append(list(result.values()))
tibetan_components_6 = pd.DataFrame(tibetan_components_6, columns=result.keys())
tibetan_components_6.to_csv("syllable_with_6_components.csv")

tibetan_components_7 = []
for i in range(min(len(syllable_7), 200)):
    syllable = syllable_7.iloc[i, 0]
    result = recog.recognization_syllable(syllable)
    tibetan_components_7.append(list(result.values()))
tibetan_components_7 = pd.DataFrame(tibetan_components_7, columns=result.keys())
tibetan_components_7.to_csv("syllable_with_7_components.csv")


# (3+2+2+8+3+1) / (200+300+300+300+161+13)
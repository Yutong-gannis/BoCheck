import numpy as np
import pandas as pd
from BoCheck import Checker
from sklearn.metrics import precision_score, recall_score, f1_score


def calculate_metrics(y_true, y_pred):
    """
    Calculate precision, recall, and F1-score based on true labels and predicted labels.

    Parameters:
    y_true (list or array): Ground truth (correct) labels.
    y_pred (list or array): Predicted labels by the model.

    Returns:
    tuple: Precision, recall, and F1-score.
    """
    precision = precision_score(y_true, y_pred, average='binary')
    recall = recall_score(y_true, y_pred, average='binary')
    f1 = f1_score(y_true, y_pred, average='binary')

    return precision, recall, f1


syllable_constraint_error_syllables = ["པདང", "རཀ", "བྷལཀྲི", "སརྦ", "བྱེདཔ", "ལུསག", "སོསག", "ཞུསག", "པཔའི", "འིཔ"]
more_vowel_error_syllables = ["རྒྱུུ", "གྱིི", "རྑྱུུར", "རྒྱུུན", "སྒྱུུར", "ཀྱིི", "བསྒྱུུར", "ཀྲུུའུ"]
more_upright_unit_error_syllables = ["འདུགཁོང", "འདུགའོན", "འདུགངས", "འདུགའདི", "འདུགཡིན", "གཅིགཐེངས", "ཀྲུངདབང", "རེའིཚགས", "གསརའགོད", "འཕྲིནལྟར"]
upright_unit_wrong_error_syllables = ["བྷ", "བྷང", "བཪྙན", "ཏྰ", "ཙྰ", "ཪྙིང", "ལྫོངས", "ཨོཾ", "རྒྱུུ", "གོི"]

error_syllables = syllable_constraint_error_syllables + more_vowel_error_syllables + more_upright_unit_error_syllables + upright_unit_wrong_error_syllables
error_labels = list(np.zeros((len(error_syllables),)))

data = pd.read_csv("evaluation/data/tibetan_frequency.csv", index_col=0)

syllable_1 = list(data[data['构件数量'] == 1].values[:20, 0])
syllable_2 = list(data[data['构件数量'] == 2].values[:40, 0])
syllable_3 = list(data[data['构件数量'] == 3].values[:40, 0])
syllable_4 = list(data[data['构件数量'] == 4].values[:40, 0])
syllable_5 = list(data[data['构件数量'] == 5].values[:40, 0])
syllable_6 = list(data[data['构件数量'] == 6].values[:40, 0])
syllable_7 = list(data[data['构件数量'] == 7].values[:10, 0])

correct_syllables = syllable_1 + syllable_2 + syllable_3 + syllable_4 + syllable_5 + syllable_6 + syllable_7
correct_labels = list(np.ones((len(correct_syllables),)))

X = correct_syllables + error_syllables
y = correct_labels + error_labels

y_pred = []
checker = Checker()
for x in X:
    result = checker.check_syllable(x)
    y_pred.append(result)
    
precision, recall, f1 = calculate_metrics(y, y_pred)

print(f"Precision: {precision:.3f}")
print(f"Recall: {recall:.3f}")
print(f"F1-score: {f1:.3f}")
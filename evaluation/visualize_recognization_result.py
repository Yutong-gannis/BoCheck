import numpy as np
import matplotlib.pyplot as plt

num_components = np.array([2, 3, 4, 5, 6, 7])
num_syllable = np.array([200, 300, 300, 300, 161, 13])
num_error = np.array([3, 2, 2, 8, 3, 1])
num_correct = num_syllable - num_error

accuracy = ((num_syllable - num_error) / num_syllable) * 100

'''
plt.figure(figsize=(4, 3))
bars = plt.bar(num_components, accuracy, color='k', width=0.3)
plt.xlabel("Number of Components")
plt.ylabel("Accuracy(%)")
plt.ylim(0, 100)

for bar, acc in zip(bars, accuracy):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 3, f"{acc:.1f}%", ha='center', color='black')
'''
fig, ax1 = plt.subplots(figsize=(6, 4))
bars_correct = ax1.bar(num_components, num_correct, label="Correct", color="darkgray", width=0.6)
bars_error = ax1.bar(num_components, num_error, bottom=num_correct, label="Error", color="black", width=0.6)

ax1.set_xlabel("Num of Components")
ax1.set_ylabel("Num of Sample")
#ax1.legend(loc="upper right", prop={'size': 10})
ax1.set_ylim(0, max(num_syllable) + 50)

#for bar, acc in zip(bars_correct, accuracy):
#    ax1.text(bar.get_x()+bar.get_width() / 2, acc, f"{acc:.1f}%", ha='center', color='k')

ax2 = ax1.twinx()
line, = ax2.plot(num_components, accuracy, color="k", marker="o", linestyle="-", label="Accuracy")
ax2.set_ylabel("Accuracy(%)", color="k")
ax2.tick_params(axis='y', labelcolor="k")
#ax2.legend(loc="upper right", prop={'size': 10})

bars = [bars_correct, bars_error, line]
labels = [bar.get_label() for bar in bars]
ax1.legend(bars, labels, loc="upper right", prop={'size': 9})

#for bar, acc in zip(bars_correct, accuracy):
#    ax2.text(bar.get_x()+bar.get_width() / 2, acc, f"{acc:.1f}%", ha='center', color='k')
    
plt.tight_layout()
#plt.show()
plt.savefig("recognization_result.png")

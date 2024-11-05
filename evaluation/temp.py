import numpy as np
import matplotlib.pyplot as plt

# 数据：总音节数和错误数
num_syllable = np.array([200, 300, 300, 300, 161, 13])
num_error = np.array([3, 2, 2, 8, 3, 1])
num_correct = num_syllable - num_error  # 计算正确数量

# 计算比例
correct_ratio = (num_correct / num_syllable) * 100
error_ratio = (num_error / num_syllable) * 100
accuracy = ((num_syllable - num_error) / num_syllable) * 100  # 计算正确率

# 创建图表
fig, ax1 = plt.subplots(figsize=(10, 6))

# 绘制堆叠柱状图
bars_correct = ax1.bar(range(len(num_syllable)), num_correct, label="正确数量", color="lightgray", width=0.6)
bars_error = ax1.bar(range(len(num_syllable)), num_error, bottom=num_correct, label="错误数量", color="darkgray", width=0.6)

# 设置左侧 y 轴标签和标题
ax1.set_xlabel("组别")
ax1.set_ylabel("数量")
ax1.set_title("各组正确和错误数量的比例及正确率折线图")
ax1.legend(loc="upper left")

# 在每个堆叠部分添加比例标签
for i, (correct, error) in enumerate(zip(correct_ratio, error_ratio)):
    ax1.text(i, num_correct[i] / 2, f"{correct:.1f}%", ha='center', color='black')  # 正确比例
    ax1.text(i, num_correct[i] + (num_error[i] / 2), f"{error:.1f}%", ha='center', color='white')  # 错误比例

# 创建右侧 y 轴用于正确率
ax2 = ax1.twinx()
ax2.plot(range(len(accuracy)), accuracy, color="blue", marker="o", linestyle="-", label="正确率")
ax2.set_ylabel("正确率 (%)", color="blue")
ax2.tick_params(axis='y', labelcolor="blue")

# 在每个折线图的点上添加正确率数值标签
for i, acc in enumerate(accuracy):
    ax2.text(i, acc + 2, f"{acc:.1f}%", ha='center', color='blue')

plt.show()

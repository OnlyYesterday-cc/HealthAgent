import matplotlib.pyplot as plt
import matplotlib
import numpy as np

matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Noto Sans CJK SC']
matplotlib.rcParams['axes.unicode_minus'] = False

schemes = [
    'PaddleOCR\nPP-OCRv4\n(CPU, 通用中英)',
    'PaddleOCR\n+ CLAHE/\n反色三变体',
    '百度云accurate\n通用OCR',
    '百度云numbers\n数字OCR\n+ bbox过滤',
    '分类先行\n双通路\n(本文方案)'
]

accuracy = [16.7, 20.0, 16.7, 3.3, 100.0]
time_cost = [1.54, 1.97, 0.64, 0.86, 1.00]
colors = ['#7f7f7f', '#7f7f7f', '#7f7f7f', '#7f7f7f', '#1f77b4']
x = np.arange(len(schemes))
width = 0.55

# === Figure 1: Accuracy only ===
fig1, ax1 = plt.subplots(figsize=(9, 4.5))
bars = ax1.bar(x, accuracy, width, color=colors, edgecolor='white', linewidth=0.5, zorder=3)
ax1.set_ylabel('字段准确率 (%)', fontsize=12)
ax1.set_ylim(0, 115)
ax1.set_yticks(np.arange(0, 121, 20))

for bar, val in zip(bars, accuracy):
    y_pos = val + 2.5
    ax1.text(bar.get_x() + bar.get_width() / 2, y_pos, f'{val}%',
             ha='center', va='bottom', fontsize=12, fontweight='bold',
             color='#1f77b4' if val == 100.0 else '#333333')

ax1.set_xticks(x)
ax1.set_xticklabels(schemes, fontsize=9)
ax1.set_title('OCR方案准确率对比', fontsize=15, fontweight='bold', pad=16)
ax1.set_xlim(-0.5, len(schemes) - 0.5)
ax1.grid(axis='y', alpha=0.3, zorder=0)
ax1.set_axisbelow(True)
fig1.tight_layout()
fig1.savefig(r'D:\HealthAgent\pic\pic2_accuracy.png', dpi=200, bbox_inches='tight',
             facecolor='white', edgecolor='none')
plt.close(fig1)
print('Saved pic2_accuracy.png')

# === Figure 2: Response time only ===
fig2, ax2 = plt.subplots(figsize=(9, 4.5))
line = ax2.plot(x, time_cost, 'o-', color='#333333', linewidth=2.5,
                markersize=10, markerfacecolor='#333333', zorder=3)
ax2.set_ylabel('平均耗时 (s)', fontsize=12)
ax2.set_ylim(0, 2.4)
ax2.set_yticks(np.arange(0, 2.6, 0.4))

for i, (xi, tc) in enumerate(zip(x, time_cost)):
    ax2.annotate(f'{tc}s', (xi, tc), textcoords="offset points",
                 xytext=(5, 14), ha='center', fontsize=11, color='#333333', fontweight='bold')

ax2.set_xticks(x)
ax2.set_xticklabels(schemes, fontsize=9)
ax2.set_title('OCR方案平均耗时对比', fontsize=15, fontweight='bold', pad=16)
ax2.set_xlim(-0.5, len(schemes) - 0.5)
ax2.grid(axis='y', alpha=0.3, zorder=0)
ax2.set_axisbelow(True)
fig2.tight_layout()
fig2.savefig(r'D:\HealthAgent\pic\pic2_time.png', dpi=200, bbox_inches='tight',
             facecolor='white', edgecolor='none')
plt.close(fig2)
print('Saved pic2_time.png')

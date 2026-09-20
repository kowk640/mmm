# -*- coding: utf-8 -*-
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Ellipse, Rectangle, Polygon

plt.rcParams['font.family'] = 'DejaVu Sans'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'figs')
os.makedirs(OUT, exist_ok=True)
GR = '#444444'
LG = '#e8e8e8'


def save(fig, name):
    fig.savefig(os.path.join(OUT, name + '.png'), dpi=200, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print('ok', name)


def blank(w=8, h=5):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    return fig, ax


def bx(ax, x, y, w, h, text, fc=LG, fs=8.5, bold=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=1.2', fc=fc, ec=GR, lw=1.0))
    ax.text(x + w / 2, y + h / 2, text, ha='center', va='center', fontsize=fs,
            color='#111111', fontweight='bold' if bold else 'normal')


def ar(ax, x1, y1, x2, y2, text=None, fs=7.5):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle='-|>', mutation_scale=12, lw=1.1, color=GR))
    if text:
        ax.text((x1 + x2) / 2 + 1.5, (y1 + y2) / 2, text, fontsize=fs, color=GR, ha='left', va='center')


# 11 arthro
fig, ax = blank(7.2, 3.6)
groups = [('Ракоподібні', 'головогруди + черевце\n5 пар ходильних ніг\n2 пари вусиків\nдихання зябрами'),
          ('Павукоподібні', 'головогруди + черевце\n4 пари ніг\nвусиків немає\nлегеневі мішки, трахеї'),
          ('Комахи', 'голова + груди + черевце\n3 пари ніг\n1 пара вусиків\nтрахеї')]
for i, (t, d) in enumerate(groups):
    x = 3 + i * 32.5
    bx(ax, x, 74, 29, 10, t, bold=True)
    bx(ax, x, 30, 29, 38, d, fc='white', fs=7.8)
ax.text(50, 14, 'Найшвидша діагностична ознака — число пар ходильних ніг і вусиків',
        ha='center', fontsize=8, color=GR)
save(fig, 'arthro')

# 12 heart
fig, ax = blank(6.4, 4.4)
ax.add_patch(Ellipse((50, 55), 54, 62, fc='white', ec=GR, lw=1.4))
ax.plot([50, 50], [26, 86], color=GR, lw=1.2)
ax.plot([26, 50], [58, 58], color=GR, lw=1.2)
ax.plot([50, 74], [58, 58], color=GR, lw=1.2)
ax.text(38, 70, 'Праве\nпередсердя', ha='center', fontsize=8)
ax.text(62, 70, 'Ліве\nпередсердя', ha='center', fontsize=8)
ax.text(38, 42, 'Правий\nшлуночок', ha='center', fontsize=8)
ax.text(62, 42, 'Лівий шлуночок\n(найтовща стінка)', ha='center', fontsize=8)
ax.annotate('', xy=(32, 86), xytext=(20, 95), arrowprops=dict(arrowstyle='->', color=GR))
ax.text(2, 99, 'порожнисті вени (венозна кров)', fontsize=7.4, color=GR, va='top')
ax.annotate('', xy=(68, 86), xytext=(80, 95), arrowprops=dict(arrowstyle='<-', color=GR))
ax.text(62, 99, 'аорта (артеріальна кров)', fontsize=7.4, color=GR, va='top')
ax.text(50, 12, 'Легенева артерія несе венозну кров, а легеневі вени — артеріальну',
        ha='center', fontsize=7.8, color=GR)
save(fig, 'heart')

# 13 nephron
fig, ax = blank(6.4, 4.4)
ax.add_patch(Circle((20, 78), 9, fc='white', ec=GR, lw=1.3))
ax.add_patch(Circle((20, 78), 5, fc=LG, ec=GR, lw=1.0))
ax.text(20, 93, 'Капсула та клубочок\n(фільтрація)', ha='center', fontsize=8)
ax.plot([29, 46, 46, 58, 58, 72], [76, 76, 28, 28, 76, 76], color=GR, lw=1.6)
ax.text(46, 86, 'Звивисті канальці\n(реабсорбція, секреція)', ha='center', fontsize=8)
ax.text(52, 20, 'Петля Генле (концентрування)', ha='center', fontsize=8)
ax.annotate('', xy=(84, 76), xytext=(72, 76), arrowprops=dict(arrowstyle='->', color=GR, lw=1.2))
ax.text(85, 76, 'збірна\nтрубочка', fontsize=8, va='center')
ax.text(50, 6, '≈170–180 л первинної сечі → ≈1,5 л вторинної (понад 99 % води повертається)',
        ha='center', fontsize=7.6, color=GR)
save(fig, 'nephron')

# 14 digest
fig, ax = blank(6.8, 4.8)
stages = [('Ротова порожнина', 'амілаза слини, pH ≈6,8: крохмаль → мальтоза'),
          ('Шлунок', 'пепсин, pH 1,5–2: білки → пептиди'),
          ('Дванадцятипала кишка', 'трипсин, ліпаза, pH ≈8; жовч емульгує жири'),
          ('Тонка кишка', 'пристінкове травлення, всмоктування ворсинками'),
          ('Товста кишка', 'всмоктування води, мікробіота, вітамін K')]
y = 86
for i, (t, d) in enumerate(stages):
    bx(ax, 4, y, 26, 9, t, bold=True, fs=8)
    bx(ax, 33, y, 63, 9, d, fc='white', fs=7.8)
    if i < len(stages) - 1:
        ar(ax, 17, y, 17, y - 7)
    y -= 16
save(fig, 'digest')

# 15 pyramid
fig, ax = blank(6.6, 4.0)
levels = [('Продуценти', '20 000 кДж', 70),
          ('Консументи I', '2 000 кДж', 54),
          ('Консументи II', '200 кДж', 38),
          ('Консументи III', '20 кДж', 22)]
y = 14
for name, val, w in reversed(levels):
    ax.add_patch(Rectangle((50 - w / 2, y), w, 14, fc=LG, ec=GR, lw=1.1))
    ax.text(50, y + 7, '%s — %s' % (name, val), ha='center', va='center', fontsize=8.4)
    y += 16
ax.text(50, 6, 'На кожному рівні передається ≈10 % енергії (правило десяти відсотків)',
        ha='center', fontsize=7.8, color=GR)
save(fig, 'pyramid')

# 16 growth
fig, ax = plt.subplots(figsize=(6.6, 3.3))
t = np.linspace(0, 20, 300)
ax.plot(t, 5 * np.exp(0.28 * t), ls='--', color='#111111', lw=1.5, label='J-подібна (експоненційна)')
K = 500.0
ax.plot(t, K / (1 + (K / 5 - 1) * np.exp(-0.45 * t)), color='#111111', lw=1.8, label='S-подібна (логістична)')
ax.axhline(K, ls=':', color=GR)
ax.text(0.4, K * 1.03, 'ємність середовища K', fontsize=7.6, color=GR)
ax.set_ylim(0, 700)
ax.set_xlabel('Час')
ax.set_ylabel('Чисельність популяції')
ax.set_title('Дві моделі зростання популяції', fontsize=10)
ax.legend(fontsize=7.6)
ax.grid(alpha=0.3, ls=':')
fig.tight_layout()
save(fig, 'growth')

# 17 exp
fig, ax = blank(7.0, 4.2)
bx(ax, 4, 86, 92, 9, 'Питання: як чинник X впливає на показник Y?', bold=True)
ar(ax, 50, 86, 50, 80)
bx(ax, 4, 68, 44, 10, 'Гіпотеза:\nзростання X збільшить Y', fc='white')
bx(ax, 52, 68, 44, 10, 'Передбачення:\nякщо …, то …', fc='white')
ar(ax, 50, 68, 50, 62)
bx(ax, 4, 46, 28, 14, 'Незалежна змінна\n(змінюємо X)')
bx(ax, 36, 46, 28, 14, 'Залежна змінна\n(вимірюємо Y)')
bx(ax, 68, 46, 28, 14, 'Контрольовані\nзмінні')
ar(ax, 50, 46, 50, 40)
bx(ax, 4, 26, 44, 12, 'Контрольна група\n(без впливу X)', fc='white')
bx(ax, 52, 26, 44, 12, 'Дослідні групи\n(різні рівні X), повторності', fc='white')
ar(ax, 50, 26, 50, 20)
bx(ax, 20, 8, 60, 10, 'Вимірювання → середнє значення → висновок і обмеження')
save(fig, 'exp')

# 18 key
fig, ax = blank(7.0, 4.2)
ax.text(50, 95, 'Фрагмент дихотомічного ключа: членистоногі', ha='center', fontsize=9.4, fontweight='bold')
bx(ax, 26, 80, 48, 9, '1. Чи є крила?', fc='white')
ar(ax, 34, 80, 20, 66, 'так')
ar(ax, 66, 80, 80, 66, 'ні')
bx(ax, 2, 56, 40, 9, '2. Крила покриті лусочками?', fc='white', fs=7.8)
bx(ax, 58, 56, 40, 9, '3. Скільки пар ніг?', fc='white', fs=7.8)
ar(ax, 10, 56, 8, 42, 'так')
ar(ax, 34, 56, 36, 42, 'ні')
ar(ax, 66, 56, 62, 42, '4 пари')
ar(ax, 90, 56, 92, 42, '5 пар')
for x, t in [(0, 'Лусокрилі'), (26, 'Двокрилі / інші'), (52, 'Павукоподібні'), (78, 'Ракоподібні')]:
    bx(ax, x + 1, 26, 21, 10, t, fs=7.8)
ax.text(50, 12, 'Рухайтеся по ключу послідовно; ніколи не вгадуйте за загальним виглядом',
        ha='center', fontsize=7.8, color=GR)
save(fig, 'key')

# 19 freq
fig, ax = plt.subplots(figsize=(6.8, 3.6))
labels = ['Зоологія', 'Ботаніка', 'Біологія людини',
          'Мікробіологія, гриби, віруси', 'Цитологія та біохімія',
          'Загальна біологія, методи', 'Екологія']
vals = [16, 13, 11, 6, 5, 4, 3]
y = np.arange(len(labels))[::-1]
ax.barh(y, vals, color='#d0d0d0', edgecolor='#333333')
for i, v in enumerate(vals):
    ax.text(v + 0.3, y[i], str(v), va='center', fontsize=8)
ax.set_yticks(y)
ax.set_yticklabels(labels, fontsize=8)
ax.set_xlabel('Кількість позицій (n = 58)')
ax.set_title('Розподіл завдань за розділами біології у проаналізованих роботах', fontsize=9.2)
ax.grid(axis='x', alpha=0.3, ls=':')
fig.tight_layout()
save(fig, 'freq')

# 20 plan
fig, ax = plt.subplots(figsize=(7.0, 3.6))
tasks = ['Діагностика та стратегія', 'Цитологія та біохімія', 'Ботаніка',
         'Зоологія', 'Біологія людини', 'Генетика та еволюція',
         'Екологія, мікробіологія', 'Пробні олімпіади та повторення']
starts = [0, 0.5, 1.5, 2.5, 3.5, 4.5, 5.0, 5.5]
durs = [0.5, 1.5, 1.0, 1.0, 1.0, 1.0, 0.8, 0.5]
y = np.arange(len(tasks))[::-1]
ax.barh(y, durs, left=starts, height=0.55, color='#d8d8d8', edgecolor='#333333')
ax.set_yticks(y)
ax.set_yticklabels(tasks, fontsize=8)
ax.set_xlabel('Тижні підготовки')
ax.set_xlim(0, 6.5)
ax.set_xticks(range(0, 7))
ax.set_title('Прискорений план на 6 тижнів (35–40 год на тиждень)', fontsize=9.4)
ax.grid(axis='x', alpha=0.3, ls=':')
fig.tight_layout()
save(fig, 'plan')

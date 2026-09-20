# -*- coding: utf-8 -*-
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle

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


# 1 algorithm
fig, ax = blank(7.2, 8.2)
steps = ['1. Прочитати умову двічі',
         '2. Підкреслити ключові слова',
         '3. Визначити розділ біології',
         '4. Згадати принцип, а не факт',
         '5. Виписати дані та одиниці',
         '6. Побудувати ланцюг міркування',
         '7. Відкинути хибні варіанти',
         '8. Перевірити на правдоподібність',
         '9. Сформулювати відповідь чітко',
         '10. Повернутися й перевірити']
y = 92
for i, s in enumerate(steps):
    bx(ax, 8, y, 84, 6.5, s, fc=LG if i % 2 == 0 else 'white')
    if i < len(steps) - 1:
        ar(ax, 50, y, 50, y - 2.5)
    y -= 9.2
save(fig, 'algorithm')

# 2 micro
fig, ax = blank(7, 4)
ax.text(50, 92, 'Шкала біологічних об’єктів (логарифмічна)', ha='center', fontsize=9.5, fontweight='bold')
ax.plot([6, 94], [45, 45], color=GR, lw=1.4)
for x, t in [(8, '0,1 нм\nатом'), (22, '2 нм\nДНК'), (36, '100 нм\nвірус'),
             (50, '1 мкм\nбактерія'), (64, '20 мкм\nклітина'),
             (78, '1 мм\nяйце'), (92, '1 м\nорганізм')]:
    ax.plot([x, x], [43, 47], color=GR, lw=1.1)
    ax.text(x, 52, t, ha='center', va='bottom', fontsize=7.6)
ax.annotate('', xy=(94, 36), xytext=(44, 36), arrowprops=dict(arrowstyle='<->', color=GR, lw=1))
ax.text(69, 30, 'видно у світловий мікроскоп (від ≈0,2 мкм)', ha='center', fontsize=7.6, color=GR)
save(fig, 'micro')

# 3 sav
fig, axs = plt.subplots(1, 2, figsize=(7.2, 3.3))
sides = np.arange(1, 11)
axs[0].plot(sides, 6.0 / sides, marker='o', color='#111111', lw=1.4)
axs[0].set_xlabel('Довжина ребра a, ум. од.')
axs[0].set_ylabel('S/V')
axs[0].set_title('S/V = 6/a', fontsize=9.5)
axs[0].grid(alpha=0.3, ls=':')
for i, a in enumerate([1, 2, 4]):
    axs[1].add_patch(Rectangle((2 + i * 11, 2), a * 3, a * 3, fc=LG, ec=GR))
    axs[1].text(2 + i * 11 + a * 1.5, 2 + a * 3 + 1.5, 'a=%d\nS/V=%.1f' % (a, 6.0 / a), ha='center', fontsize=8)
axs[1].set_xlim(0, 40)
axs[1].set_ylim(0, 22)
axs[1].axis('off')
axs[1].set_title('Зі зростанням розміру S/V падає', fontsize=9.5)
fig.tight_layout()
save(fig, 'sav')

# 4 osmosis
fig, ax = blank(7.2, 3.6)
titles = ['Гіпотонічний розчин', 'Ізотонічний розчин', 'Гіпертонічний розчин']
notes = ['вода входить → тургор', 'рівновага потоків', 'вода виходить → плазмоліз']
for i in range(3):
    cx = 18 + i * 32
    ax.add_patch(Rectangle((cx - 13, 30), 26, 42, fc='white', ec=GR, lw=1.3))
    if i == 0:
        ax.add_patch(Rectangle((cx - 10, 33), 20, 36, fc=LG, ec=GR))
    elif i == 1:
        ax.add_patch(Rectangle((cx - 10, 34), 20, 32, fc=LG, ec=GR))
    else:
        ax.add_patch(Rectangle((cx - 7, 40), 14, 20, fc=LG, ec=GR))
    ax.text(cx, 78, titles[i], ha='center', fontsize=8.4, fontweight='bold')
    ax.text(cx, 22, notes[i], ha='center', fontsize=7.8, color=GR)
ax.text(50, 8, 'Клітинна стінка рослини запобігає розриву; тваринна клітина лопає',
        ha='center', fontsize=7.8, color=GR)
save(fig, 'osmosis')

# 5 mitmei
fig, ax = blank(7.4, 4.4)
bx(ax, 4, 78, 30, 10, 'Материнська клітина 2n', bold=True)
ar(ax, 19, 78, 19, 63)
bx(ax, 4, 50, 30, 12, 'Мітоз:\n2 клітини 2n,\nгенетично ідентичні', fc='white')
ar(ax, 19, 50, 19, 36)
bx(ax, 4, 22, 30, 12, 'Ріст, регенерація,\nбезстатеве\nрозмноження')
bx(ax, 60, 78, 34, 10, 'Материнська клітина 2n', bold=True)
ar(ax, 77, 78, 77, 69)
bx(ax, 60, 57, 34, 11, 'Мейоз I: розходяться\nгомологи (кросинговер)', fc='white')
ar(ax, 77, 57, 77, 48)
bx(ax, 60, 36, 34, 11, 'Мейоз II: розходяться\nхроматиди', fc='white')
ar(ax, 77, 36, 77, 30)
bx(ax, 60, 18, 34, 11, '4 клітини n,\nгенетично різні')
ax.text(19, 94, 'МІТОЗ', ha='center', fontsize=10, fontweight='bold')
ax.text(77, 94, 'МЕЙОЗ', ha='center', fontsize=10, fontweight='bold')
save(fig, 'mitmei')

# 6 enzyme
fig, axs = plt.subplots(1, 2, figsize=(7.2, 3.2))
t = np.linspace(0, 70, 300)
v = np.where(t <= 37, np.exp(-((t - 37) ** 2) / 260.0), np.exp(-((t - 37) ** 2) / 45.0))
axs[0].plot(t, v, color='#111111', lw=1.5)
axs[0].axvline(37, ls=':', color=GR)
axs[0].text(38.5, 0.45, 'оптимум ≈37 °C', fontsize=7.6, color=GR)
axs[0].set_xlabel('Температура, °C')
axs[0].set_ylabel('Відносна активність')
axs[0].set_title('Вплив температури', fontsize=9.5)
axs[0].grid(alpha=0.3, ls=':')
ph = np.linspace(0, 12, 300)
for opt, lab, st in [(2, 'пепсин (pH 1,5–2)', '-'), (6.8, 'амілаза (pH ≈6,8)', '--'), (8, 'трипсин (pH ≈8)', ':')]:
    axs[1].plot(ph, np.exp(-((ph - opt) ** 2) / 2.2), ls=st, color='#111111', lw=1.4, label=lab)
axs[1].set_xlabel('pH')
axs[1].set_ylabel('Відносна активність')
axs[1].set_title('Вплив pH', fontsize=9.5)
axs[1].legend(fontsize=6.8)
axs[1].grid(alpha=0.3, ls=':')
fig.tight_layout()
save(fig, 'enzyme')

# 7 limiting
fig, ax = plt.subplots(figsize=(6.6, 3.3))
x = np.linspace(0, 100, 300)
for cap, lab, st in [(1.0, 'низька [CO$_2$]', '--'), (1.6, 'висока [CO$_2$]', '-')]:
    ax.plot(x, cap * (1 - np.exp(-x / 22.0)), ls=st, color='#111111', lw=1.5, label=lab)
ax.set_xlabel('Інтенсивність світла, ум. од.')
ax.set_ylabel('Швидкість фотосинтезу')
ax.set_title('Лімітувальні чинники фотосинтезу', fontsize=10)
ax.legend(fontsize=8)
ax.grid(alpha=0.3, ls=':')
ax.annotate('обмежує світло', xy=(9, 0.42), xytext=(20, 0.15), fontsize=7.6, color=GR,
            arrowprops=dict(arrowstyle='->', color=GR))
ax.annotate('обмежує CO$_2$ або температура', xy=(80, 1.0), xytext=(34, 1.32), fontsize=7.6, color=GR,
            arrowprops=dict(arrowstyle='->', color=GR))
fig.tight_layout()
save(fig, 'limiting')

# 8 pedigree
fig, ax = blank(6.6, 3.6)


def male(x, y, filled):
    ax.add_patch(Rectangle((x - 3, y - 3), 6, 6, fc=('#555555' if filled else 'white'), ec=GR, lw=1.2))


def female(x, y, filled):
    ax.add_patch(Circle((x, y), 3.2, fc=('#555555' if filled else 'white'), ec=GR, lw=1.2))


male(30, 80, False)
female(55, 80, False)
ax.plot([33, 52], [80, 80], color=GR, lw=1)
ax.plot([42.5, 42.5], [80, 66], color=GR, lw=1)
ax.plot([22, 68], [66, 66], color=GR, lw=1)
for x, f, isM in [(22, True, True), (45, False, False), (68, False, True)]:
    ax.plot([x, x], [66, 58], color=GR, lw=1)
    (male if isM else female)(x, 55, f)
ax.text(24, 86, 'I', fontsize=8, color=GR)
ax.text(12, 55, 'II', fontsize=8, color=GR)
ax.text(50, 34, 'Обидва батьки здорові, але є уражена дитина\n→ ознака рецесивна', ha='center', fontsize=8.4)
ax.text(50, 14, '□ чоловік    ○ жінка    залите = уражений фенотип', ha='center', fontsize=7.6, color=GR)
save(fig, 'pedigree')

# 9 clado
fig, ax = plt.subplots(figsize=(7.0, 4.0))
ax.set_xlim(0, 130)
ax.set_ylim(0, 100)
ax.axis('off')
labels = ['Хрящові риби', 'Променепері риби', 'Земноводні', 'Лускаті', 'Крокодили', 'Птахи', 'Ссавці']
syn = ['щелепи', 'кістковий скелет', 'чотири кінцівки', 'амніотичне яйце', 'архозаври', 'пір’я']
for i, lab in enumerate(labels):
    yy = 8 + i * 13
    ax.plot([18 + i * 9, 88], [yy, yy], color=GR, lw=1.1)
    ax.text(90, yy, lab, fontsize=8, va='center')
for i in range(len(labels) - 1):
    x = 18 + i * 9
    ax.plot([x, x], [8 + i * 13, 8 + (i + 1) * 13], color=GR, lw=1.1)
    ax.text(x + 1.2, 8 + i * 13 + 6.5, syn[i], fontsize=6.8, color=GR, rotation=90, va='center')
ax.plot([10, 18], [8, 8], color=GR, lw=1.3)
ax.text(4, 96, 'Гілки — спільні предки; підписи на вузлах — синапоморфії', fontsize=8.2, color=GR)
save(fig, 'clado')

# 10 altern
fig, ax = blank(6.8, 4.2)
bx(ax, 34, 84, 32, 9, 'Спорофіт (2n)', bold=True)
ar(ax, 66, 88, 82, 68, 'мейоз')
bx(ax, 64, 56, 32, 9, 'Спори (n)')
ar(ax, 78, 56, 62, 38)
bx(ax, 34, 26, 32, 9, 'Гаметофіт (n)', bold=True)
ar(ax, 34, 31, 18, 56)
bx(ax, 4, 56, 30, 9, 'Гамети (n)')
ar(ax, 20, 65, 36, 84, 'запліднення')
ax.text(50, 12, 'У мохів переважає гаметофіт, у папоротей і насінних — спорофіт',
        ha='center', fontsize=8, color=GR)
save(fig, 'altern')

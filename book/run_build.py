import glob, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import builder

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, 'src')
FIG = os.path.join(BASE, 'figs')
OUT = os.path.join(BASE, 'Biolohiia_Olimpiada_9_klas_Povnyi_Posibnyk.pdf')

files = sorted(glob.glob(os.path.join(SRC, 'c*.md')))
print('files:', len(files))

meta = {
    'title': 'Біологія. Олімпіадний посібник для 9 класу',
    'subtitle': 'Поглиблена підготовка до шкільного та міського (районного) етапів',
    'footer': 'Авторський навчальний посібник. Складено на основі завантажених матеріалів учня.',
    'notice': [
        'Цей посібник створено як навчальний матеріал для самостійної підготовки до Всеукраїнської учнівської олімпіади з біології на рівні 9 класу.',
        'Посібник не є офіційним виданням організаційного комітету олімпіади. Він не містить і не відтворює повністю жодного захищеного авторським правом видання: завдання минулих олімпіад використано лише фрагментарно з метою навчального аналізу, а переважна більшість завдань є оригінальними або істотно переробленими.',
        'Жодна методика підготовки не гарантує певного результату на змаганні. Посібник допомагає системно опрацювати матеріал і відпрацювати алгоритми міркування.',
        'Там, де офіційна відповідь виглядає науково спірною, це окремо позначено й пояснено, а не приховано.',
    ],
}

front = builder.title_pages(meta)
figs, tabs, ch = builder.build(files, OUT, FIG, front_flowables=front)
print('figs', figs, 'tabs', tabs, 'chapters', ch)
print('bytes', os.path.getsize(OUT))

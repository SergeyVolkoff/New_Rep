class Bird:
    def __init__(self, name, size):
        self.name = name
        self.size = size

    def describe(self, full=False):
        return f'Размер птицы {self.name} — {self.size}.'


class Parrot(Bird):
    def __init__(self, name, size, color):
        super().__init__(name, size)
        self.color = color

    # Переопределите метод describe().
    def describe(self, full=False):
        if full == False:
            return Bird.describe(self)
        else:
            if full == True:
                return (f'Попугай {self.name} — заметная птица, окрас её перьев — {self.color},'
                        f'а размер — {self.size}. Интересный факт: попугаи чувствуют ритм, '
                        f'а вовсе не бездумно двигаются под музыку. Если сменить композицию,'
                        f' то и темп движений птицы изменится.')


class Penguin(Bird):
    def __init__(self, name, size, genus):
        super().__init__(name, size)
        self.genus = genus

    # Переопределите метод describe().
    def describe(self, full=False):
        if full == False:
            return Bird.describe(self)
        else:
            if full == True:
                return (f'Размер пингвина {self.name} из рода genus — {self.size}. '
                        f'Интересный факт: однажды группа геологов-разведчиков похитила пингвинье яйцо, '
                        f'и их принялась преследовать вся стая, не пытаясь, впрочем, при этом нападать. '
                        f'Посовещавшись, похитители вернули птицам яйцо, и те отстали.')


kesha = Parrot('Ара', 'средний', 'красный')
kowalski = Penguin('Королевский', 'большой', 'Aptenodytes')

# Вызов метода у созданных объектов.
print(kesha.describe())
print(kowalski.describe(True))

from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random


class Constants(BaseConstants):
    name_in_url = 'survey'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    def set_payoff(self):
        """Calculate payoff, which is zero for the survey"""
        self.payoff = 0

    age = models.PositiveIntegerField(verbose_name='Ваш возраст (полных лет)',
                                        choices=range(13, 95),
                                        initial=None)

    gender = models.BooleanField(initial=None,
                                choices=[[0,'Мужской'],[1,'Женский']],
                                verbose_name='Ваш пол',
                                widget=widgets.RadioSelect())

    heigth = models.PositiveIntegerField(verbose_name='Ваш рост (в сантиметрах)',
                                        choices=range(100, 230),
                                        initial=None)

    city = models.PositiveIntegerField(
        verbose_name='''
    Сколько человек (приблизительно) проживало в том населенном пункте, где Вы жили в возрасте 16 лет.''',
        choices = range(1, 30000000),
              initial = None)

    yearsinmsc = models.PositiveIntegerField(
        verbose_name='''
    Укажите, сколько лет Вы живете в Москве. Впишите число, округленное до ближайшего целого числа лет.''',
    choices = range(0, 95),
              initial = None)

    mscyourcity = models.PositiveIntegerField(
        verbose_name='''
    Можете ли вы сказать, что Москва – это ваш город?''',
        choices=[
            [1, 'Полностью не согласен'],
            [2, 'Не согласен'],
            [3, 'Затрудняюсь ответить'],
            [4, 'Согласен'],
            [5, 'Полностью согласен'],
        ],
        widget=widgets.RadioSelect()
    )

    achieve= models.CharField(
        verbose_name= '''Какие значимые достижения/решения московских властей последних 3 лет Вы можете
    назвать? Напишите не более 5.'''
    )

    deput= models.CharField(
        verbose_name= '''Знаете ли Вы по именам кого-нибудь из муниципальных депутатов Москвы или Московской городской
    думы? Напишите не более 5 имен.
    '''
    )

    univ= models.CharField(
        verbose_name= '''Укажите ВУЗ, в котором учитесь(или который окончили).'''
    )

    study= models.CharField(
        verbose_name= '''Укажите
    направление
    подготовки, на
    котором
    Вы
    обучаетесь(или
    обучались).'''
    )

    riskat=models.PositiveIntegerField(
        verbose_name='''Вы любите риск или боитесь риска?''',
               choices = [
                             [1, 'Очень люблю рисковать'],
                             [2, 'Люблю рисковать'],
                             [3, 'Нейтрален к риску'],
                             [4, 'Боюсь рисковать'],
                             [5, 'Очень боюсь рисковать'],
                         ],
                         widget = widgets.RadioSelect()
    )

    income = models.PositiveIntegerField(
        verbose_name='''Какое высказывание наиболее точно описывает финансовое положение вашей семьи?''',
        choices=[
            [1, 'Едва сводим концы с концами, денег не хватает на выживание;'],
            [2, 'Живем от зарплаты до зарплаты, денег хватает только на неотложные нужды;'],
            [3, 'На ежедневные расходы хватает денег, но уже покупка одежды требует накоплений;'],
            [4, 'Вполне хватает денег, даже имеются некоторые накопления, но крупные покупки требуется планировать заранее;'],
            [5, 'Можем позволить себе крупные траты при первой необходимости.'],
        ],
        widget=widgets.RadioSelect()
    )

    satis=models.PositiveIntegerField(
        verbose_name='''Учитывая все обстоятельства, насколько Вы удовлетворены вашей жизнью в целом в эти дни? (от 1 «полностью не удовлетворен» до 10 «полностью удовлетворен»)''',
          choices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                    widget = widgets.RadioSelectHorizontal()
    )

    trust = models.BooleanField(
        verbose_name ='''Как Вы считаете, в целом большинству людей можно доверять, или же при общении с другими людьми осторожность никогда не повредит? Пожалуйста, отметьте позицию на шкале, где 1 означает "Нужно быть очень осторожным с другими людьми" и 10
        означает "Большинству людей можно вполне доверять" ''',
        choices=[1,2,3,4,5,6,7,8,9,10],
        widget=widgets.RadioSelectHorizontal()
    )

    freedom = models.PositiveIntegerField(
        verbose_name='''Некоторые люди чувствуют, что они обладают полной свободой выбора и контролируют свою жизнь, в
    то время как другие люди чувствуют, что то, что они делают, не имеет реального влияния на происходящее с ними. До какой степени эти
    характеристики применимы к Вам и Вашей жизни? Пожалуйста, отметьте позицию на шкале, где 1 означает "у меня нет свободы выбора" и 10
    означает "у меня полная свобода выбора".
    ''',
        choices=[1,2,3,4,5,6,7,8,9,10],
        widget=widgets.RadioSelectHorizontal()
    )


    politics=models.PositiveIntegerField(
        verbose_name='''До какой степени Вы интересуетесь политикой? (от 1 «Вообще не интересуюсь» до 10 «Очень интересуюсь»)''',
    choices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
              widget = widgets.RadioSelectHorizontal()
    )

    leftright = models.PositiveIntegerField(
        verbose_name='''В
    политических
    вопросах, люди
    говорят
    о
    "левых" (сторонники равенства и социальной справедливости)
    и
    "правых" (сторонники либерализма и конкуренции). Как
    бы
    Вы
    охарактеризовали
    свои
    взгляды
    на
    шкале
    от
    1 «левые» до
    10 «правые»?''',
        choices=[1,2,3,4,5,6,7,8,9,10],
        widget=widgets.RadioSelectHorizontal()
    )

    owner=models.PositiveIntegerField(
        verbose_name='''До какой степени Вы согласны с утверждением: «Право собственности непоколебимо».''',
                choices = [
                              [1, 'Полностью не согласен'],
                              [2, 'Не согласен'],
                              [3, 'Затрудняюсь ответить'],
                              [4, 'Согласен'],
                              [5, 'Полностью согласен'],
                          ],
                          widget = widgets.RadioSelect()
    )

    ownership=models.PositiveIntegerField(
        verbose_name='''Как Вы относитесь к утверждению  «Доля государственной собственности в экономике нашей страны должна быть увеличена»?
        Отметьте на шкале, где 1 означает, что Вы полностью не согласны с утверждением, 10 - что полностью согласны''',
           choices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                     widget = widgets.RadioSelectHorizontal()
    )

    responsibility = models.PositiveIntegerField(
        verbose_name='''Как Вы относитесь к утверждению  ««Правительство должно нести ответственность за благосостояние людей»?
        Отметьте на шкале, где 1 означает, что Вы полностью не согласны с этим утверждением, 10 - что полностью согласны''',
           choices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                     widget = widgets.RadioSelectHorizontal()
    )

    democracy = models.PositiveIntegerField(
        verbose_name=''' Насколько
    важно
    для
    Вас
    жить
    в
    стране, которая
    управляется
    по
    принципам
    демократии? Отметьте на шкале, где 1 означает «не
    важно», 10 «очень
    важно» ''',
        choices=[1,2,3,4,5,6,7,8,9,10],
        widget=widgets.RadioSelectHorizontal()
    )

    democracy_today=models.PositiveIntegerField(
        verbose_name='''Можете ли Вы сказать, что политическая система в нашей стране на сегодняшний день является демократической? Отметьте на шкале, где 1 означает «совсем не демократическая» до 10 «полностью демократическая»''',
            choices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                      widget = widgets.RadioSelectHorizontal()
    )


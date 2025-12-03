:- encoding(utf8).
:- use_module(library(readutil)).

:- dynamic known/2.

start :-
    retractall(known(_,_)),
    nl,
    write('Экспертная система: подбор домашнего растения.'), nl,
    write('Отвечайте одним словом из списка (например: low, yes).'), nl,
    write('Без точки в конце.'), nl, nl,
    ask_all,
    nl,
    choose_plant(Plant),
    format('Рекомендуемое растение: ~w.~n', [Plant]),
    explain(Plant).

% ---------- задаём все вопросы один раз ----------

ask_all :-
    ask_param(light,
        'Какое освещение в месте, где будет стоять растение? (low/medium/bright)',
        [low, medium, bright]),
    ask_param(humidity,
        'Какой уровень влажности в квартире? (low/normal/high)',
        [low, normal, high]),
    ask_param(time_for_care,
        'Сколько времени вы готовы уделять уходу за растением? (low/medium/high)',
        [low, medium, high]),
    ask_param(space,
        'Сколько места есть под растение? (small/medium/large)',
        [small, medium, large]),
    ask_param(has_pets,
        'Есть ли дома животные, которые могут грызть листья? (yes/no)',
        [yes, no]),
    ask_param(non_toxic_required,
        'Важно ли, чтобы растение было нетоксичным для животных и детей? (yes/no)',
        [yes, no]).

ask_param(Key, Question, Allowed) :-
    repeat,
        nl,
        write(Question), nl,
        write('Допустимые ответы: '), write(Allowed), nl,
        write('> '),
        read_line_to_string(user_input, Line0),
        string_lower(Line0, Line1),
        string_trim(Line1, Clean),
        (   Clean = ""
        ->  nl, write('Пустой ввод, повторите.'), nl, fail
        ;   atom_string(Atom, Clean),
            (   member(Atom, Allowed)
            ->  retractall(known(Key,_)),
                assertz(known(Key, Atom)),
                !
            ;   nl,
                write('Некорректный ввод. Введите одно из: '),
                write(Allowed), nl,
                fail
            )
        ).

% обрезка пробелов/служебных символов по краям
string_trim(In, Out) :-
    string_codes(In, Codes),
    trim_left(Codes, NoLeft),
    reverse(NoLeft, Rev),
    trim_left(Rev, RevNoLeft),
    reverse(RevNoLeft, Trimmed),
    string_codes(Out, Trimmed).

trim_left([C|Cs], R) :-
    (   code_type(C, space)
    ->  trim_left(Cs, R)
    ;   R = [C|Cs]
    ).
trim_left([], []).

% ---------- выбор растения ----------

choose_plant(Plant) :-
    plant(Plant), !.

% более конкретные правила вперёд

plant(succulent) :-
    known(light, bright),
    known(time_for_care, low),
    ( known(humidity, low)
    ; known(humidity, normal)
    ).

plant(ficus) :-
    known(light, medium),
    known(time_for_care, medium),
    known(humidity, normal),
    ( known(non_toxic_required, no)
    ; known(has_pets, no)
    ).

plant(spathiphyllum) :-
    ( known(light, low)
    ; known(light, medium)
    ),
    known(humidity, high),
    ( known(time_for_care, medium)
    ; known(time_for_care, high)
    ),
    known(has_pets, no).

plant(monstera) :-
    known(space, large),
    known(light, medium),
    ( known(time_for_care, medium)
    ; known(time_for_care, high)
    ),
    known(has_pets, no).

plant(zamioculcas) :-
    ( known(light, low)
    ; known(light, medium)
    ),
    known(time_for_care, low),
    ( known(humidity, low)
    ; known(humidity, normal)
    ).

plant(orchid) :-
    known(light, bright),
    known(humidity, high),
    ( known(time_for_care, medium)
    ; known(time_for_care, high)
    ).

plant(chlorophytum) :-
    ( known(light, low)
    ; known(light, medium)
    ),
    ( known(time_for_care, low)
    ; known(time_for_care, medium)
    ),
    known(non_toxic_required, yes).


explain(succulent) :-
    nl,
    write('Пояснение:'), nl,
    write('- Много света и мало времени на уход подходят для суккулентов и кактусов.'), nl,
    write('- Они переносят пересушку почвы и не требуют частого полива.'), nl.

explain(ficus) :-
    nl,
    write('Пояснение:'), nl,
    write('- Фикус любит рассеянный свет и регулярный, но не чрезмерный полив.'), nl,
    write('- Подходит для квартир со стабильным уходом.'), nl.

explain(spathiphyllum) :-
    nl,
    write('Пояснение:'), nl,
    write('- Спатифиллум хорошо чувствует себя в тени/полутени и при высокой влажности.'), nl,
    write('- Требует регулярного полива и опрыскивания.'), nl.

explain(monstera) :-
    nl,
    write('Пояснение:'), nl,
    write('- Монстере нужно достаточно пространства и хороший рассеянный свет.'), nl,
    write('- Подходит, если вы готовы ухаживать за крупным растением.'), nl.

explain(zamioculcas) :-
    nl,
    write('Пояснение:'), nl,
    write('- Замиокулькас неприхотлив, переносит тень и редкий полив.'), nl,
    write('- Хороший вариант для занятых людей.'), nl.

explain(orchid) :-
    nl,
    write('Пояснение:'), nl,
    write('- Орхидее нужен яркий рассеянный свет и высокая влажность.'), nl,
    write('- Требует более внимательного ухода, но за это радует цветением.'), nl.

explain(chlorophytum) :-
    nl,
    write('Пояснение:'), nl,
    write('- Хлорофитум нетребователен, подходит при разном освещении.'), nl,
    write('- Считается безопасным для животных и детей и хорошо очищает воздух.'), nl,
    write('- В том числе выбран как универсальный вариант, если других идеальных совпадений нет.'), nl.

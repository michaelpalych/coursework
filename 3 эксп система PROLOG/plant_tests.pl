:- encoding(utf8).

:- use_module(library(plunit)).

% подключаем экспертную систему в модуль user
:- ['1.pl'].

% сброс ответов в модуле user
clear_known :-
    user:retractall(known(_,_)).

:- begin_tests(plants).

% 1) succulent
% правило:
%   light = bright, time_for_care = low, humidity = low/normal
test(succulent, [setup(clear_known)]) :-
    user:assertz(known(light, bright)),
    user:assertz(known(humidity, low)),
    user:assertz(known(time_for_care, low)),
    user:assertz(known(space, small)),
    user:assertz(known(has_pets, yes)),
    user:assertz(known(non_toxic_required, no)),
    user:choose_plant(P),
    assertion(P == succulent).

% 2) ficus
%   light = medium, time_for_care = medium, humidity = normal,
%   (non_toxic_required = no ; has_pets = no)
test(ficus, [setup(clear_known)]) :-
    user:assertz(known(light, medium)),
    user:assertz(known(humidity, normal)),
    user:assertz(known(time_for_care, medium)),
    user:assertz(known(space, medium)),
    user:assertz(known(has_pets, no)),
    user:assertz(known(non_toxic_required, no)),
    user:choose_plant(P),
    assertion(P == ficus).

% 3) spathiphyllum
%   light = low/medium, humidity = high,
%   time_for_care = medium/high, has_pets = no
test(spathiphyllum, [setup(clear_known)]) :-
    user:assertz(known(light, low)),
    user:assertz(known(humidity, high)),
    user:assertz(known(time_for_care, medium)),
    user:assertz(known(space, medium)),
    user:assertz(known(has_pets, no)),
    user:assertz(known(non_toxic_required, no)),
    user:choose_plant(P),
    assertion(P == spathiphyllum).

% 4) monstera
%   space = large, light = medium,
%   time_for_care = medium/high, has_pets = no
test(monstera, [setup(clear_known)]) :-
    user:assertz(known(light, medium)),
    user:assertz(known(humidity, low)),
    user:assertz(known(time_for_care, medium)),
    user:assertz(known(space, large)),
    user:assertz(known(has_pets, no)),
    user:assertz(known(non_toxic_required, no)),
    user:choose_plant(P),
    assertion(P == monstera).

% 5) zamioculcas
%   light = low/medium, time_for_care = low, humidity = low/normal
test(zamioculcas, [setup(clear_known)]) :-
    user:assertz(known(light, low)),
    user:assertz(known(humidity, normal)),
    user:assertz(known(time_for_care, low)),
    user:assertz(known(space, small)),
    user:assertz(known(has_pets, yes)),
    user:assertz(known(non_toxic_required, no)),
    user:choose_plant(P),
    assertion(P == zamioculcas).

% 6) orchid
%   light = bright, humidity = high, time_for_care = medium/high
test(orchid, [setup(clear_known)]) :-
    user:assertz(known(light, bright)),
    user:assertz(known(humidity, high)),
    user:assertz(known(time_for_care, medium)),
    user:assertz(known(space, medium)),
    user:assertz(known(has_pets, yes)),
    user:assertz(known(non_toxic_required, no)),
    user:choose_plant(P),
    assertion(P == orchid).

% 7) chlorophytum
%   light = low/medium, time_for_care = low/medium,
%   non_toxic_required = yes
test(chlorophytum, [setup(clear_known)]) :-
    user:assertz(known(light, medium)),
    user:assertz(known(humidity, high)),       % ломаем zamioculcas
    user:assertz(known(time_for_care, low)),
    user:assertz(known(space, medium)),
    user:assertz(known(has_pets, yes)),
    user:assertz(known(non_toxic_required, yes)),
    user:choose_plant(P),
    assertion(P == chlorophytum).

:- end_tests(plants).

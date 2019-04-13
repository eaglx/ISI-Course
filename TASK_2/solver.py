#import os
import sys
import re
import operator

#os.system("xzcat")

def fun():
    file_in = open(sys.argv[1], 'r')
    file_out = open(sys.argv[2], 'w')

    for text in file_in.readlines():
        wordList = text.split(" ")
        yearSet = set()
        temp_yearScore = yearScore.copy()
        for w in wordList:
            match = re.match(r'[1-2][0-9][0-9][0-9]', w)
            if match is not None:
                if (int(match.group()) >= 1814) and (int(match.group()) <= 2014):
                    yearSet.add(match.group())
        if len(yearSet) != 0:
            file_out.write(yearSet.pop() + ".0\n")
        else:
            for w in wordList:
                ww = w.lower()
                for k in temp_yearScore.keys():
                    for v in yearDict[k]:
                        if v in w:
                            temp_yearScore[k] += 1/len(yearDict[k])
            year_toSave = max(temp_yearScore.items(), key=operator.itemgetter(1))[0]
            if temp_yearScore[year_toSave] < 0.2:
                year_toSave = 1914
            file_out.write(str(year_toSave) + ".0\n")

    file_in.close()
    file_out.close()


yearDict = {
1934: ["hitler", "mussolini", "beck", "ribbentrop" "bombard", "dmowski", "sławek", "śmigły", "rydz", "schleswig", "holstein", "mościcki", "mobilizacja", "westerplatte", "luftwaffe", "raginis", "orzeł", "raczkiewicz", "sikorski", "wermacht", "generalne", "gubernator"],
1924: ["narutowicz", "zamach", "wojciechowski", "powstanie", "śląsk", "złoty", "port", "gdyni", "bolsz", "piłsudski", "witos", "pucz", "przewrót", "konkordat", "gdańsk", "westerplatte", "stresseman", "grabski", "skrzyński", "locarno"],
1914: ["zamach", "arcyksięcia", "habsburg", "weimarska", "lenin", "car", "mikołaj", "wojna"],
1904: ["nobel", "curie", "skłodowska", "einstein", "wiktoria", "edward", "królestwo", "car", "dmowski", "piłsudski"],
1894: ["piłsudski", "witos", "dmowski", "partia", "socjalistyczna", "igrzyska", "aten", "romanow"],
1884: ["mickiewicz", "caprivi", "kanclerz", "bismarck", "romanow", "hohenzollern", "franciszek", "józef"],
1874: ["zjednoczenie", "hohenzollern", "bismarck", "napoleon", "bonaparte", "bell", "edison", "sobór", "pius"],
1864: ["branka", "wielopolski", "powstanie", "manifest", "tymczasowy", "rząd", "romuald", "traugutt", "uwłaszczenie", "romanow", "sobór", "pius"],
1854: ["beaufort", "naftowa", "krym", "osmań", "wojna"],
1844: ["rzeź", "galic", "kraków", "tyssowski", "dembowski", "zjazd", "wiosna"],
1834: ["fryderyk", "opium", "królestwo", "grzegorz", "olszynka", "groch", "wysocki", "mochnacki", "chłopicki", "dybicz", "romanow", "habsburg", "hohenzollern", "metternich", "wilhelmem", "lelewel", "towarzystwo", "patriotyczne"],
1824: ["bonaparte", "romanow", "cytadela", "mikołaj"],
1814: ["poniatowski", "wiedeń", "kongres", "napoleon", "bonaparte", "matecki", "kielc", "akademia", "agh", "staszic", "filomat", "ossoliński"],
2012: ["acta", "madzia", "rutkowski", "stadion", "narodowy", "emerytalna", "67", "komorowski", "uefa", "euro"],
2010: ["elton", "bemowo", "belka", "nbp", "krzyż", "katastrofa", "smoleńsk", "palenia", "tytoniu", "ac/dc", "lech", "poznań", "kaczyński", "erupcja", "grunwald", "komorowski", "sikorski"],
2004: ["putin", "euro", "bush", "zamach", "world", "trade", "miller", "unia", "belka", "platforma", "obywatelska"],
1995: ["szymborska", "nobla", "oleksy", "lech", "wałęsa", "aleksander", "kwaśniewski", "nato", "losowanie", "polsat", "afera", "alkohol", "michael", "jackson", "cimoszewicz"],
1984: ["inflacja", "okrągły", "popiełuszko", "solidarność", "nobel", "czesław", "miłosz", "wałęsa", "balcerowicz", "stan", "wojenny"],
1974: ["gierek", "wojtyła", "jan", "paweł"],
1964: ["kennedy", "apollo", "armstrong"],
1954: ["bierut", "stalin", "gomułka", "strajk", "układ", "sputnik"],
1950: ["ameryka", "usa", "stonk", "ziemniacz"],
1944: ["stalin", "churchill", "roosevelt", "radziecki", "pearl", "harbor", "marshall", "jałta", "komitet", "wyzwolenia", "bierut", "osóbka", "morawski", "tymczasowy", "rząd", "cyrankiewicz", "szklarska", "poręba"]
}


yearScore = {
1934: 0,
1924: 0,
1914: 0,
1904: 0,
1894: 0,
1884: 0,
1874: 0,
1864: 0,
1854: 0,
1844: 0,
1834: 0,
1824: 0,
1814: 0,
2012: 0,
2010: 0,
2004: 0,
1995: 0,
1984: 0,
1974: 0,
1964: 0,
1954: 0,
1950: 0,
1944: 0
}

if len(sys.argv) < 3:
    print("MORE ARGS!!")
    print("solver.py in.tsv out.tsv")
    exit()
fun()

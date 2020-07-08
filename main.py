import copy
import time

etapa = 1    #etapa curenta
nrMiscariFaraStergere = 0
euristica = 0
nrMiscariJMIN = 0
nrMiscariJMAX = 0

class Joc:
    """
    Clasa care defineste jocul. Se va schimba de la un joc la altul.
    """
    SIMBOLURI_JUC = ['X', 'O']
    JMIN = None
    JMAX = None
    GOL = '#'

    def __init__(self, tabla=None):
        self.config = tabla or [Joc.GOL] * 24
        self.liniiMori = [
            [0,1,2], [2,4,7], [5,6,7], [0,3,5], [8,9,10], [10,12,15], [13,14,15], [8,11,13], [16,17,18], [18,20,23],
            [21,22,23], [16,19,21], [1,9,17], [4,12,20], [6,14,22], [3,11,19]
        ]


    def numarPiese(self, piesa):         #functie care numara cate piese de un anumit fel sunt pe tabla
        return self.config.count(piesa)


    def pozitiiVecine(self, poz):       #functie care primeste ca parametru o pozitie si intoarce o lista cu
        vecini = [                        #pozitiile vecine acelei pozitii
            [1, 3],           #0
            [0, 2, 9],        #1
            [1, 4],           #2
            [0, 5, 11],       #3
            [2, 7, 12],       #4
            [3, 6],           #5
            [5, 7, 14],       #6
            [4, 6],           #7
            [9, 11],          #8
            [1, 8, 10, 17],   #9
            [9, 12],          #10
            [3, 8, 13, 19],   #11
            [4, 10, 15, 20],  #12
            [11, 14],         #13
            [6, 13, 15, 22],  #14
            [12, 14],         #15
            [17, 19],         #16
            [9, 16, 18],      #17
            [17, 20],         #18
            [11, 16, 21],     #19
            [12, 18, 23],     #20
            [19, 22],         #21
            [14, 21, 23],     #22
            [20, 22],         #23
        ]

        return vecini[poz]


    def verifica2Pozitii(self, tabla, piesaJucator, p1, p2):                               #verifica daca pe cele 2 pozitii p1, p2 se
        if (tabla[p1] == piesaJucator and tabla[p2] == piesaJucator):        #afla piese care apartin aceluiasi jucator
            return True
        return False


    def verificaVecini(self, tabla, piesaJucator, poz):                                    #verifica daca exista 2 pozitii pe aceeasi linie
                                                                                    #cu poz in care sa fie piese ale aceluiasi jucator
        lista = [
            (self.verifica2Pozitii(tabla, piesaJucator, 1, 2) or self.verifica2Pozitii(tabla, piesaJucator, 3, 5)),        #0
            (self.verifica2Pozitii(tabla, piesaJucator, 0, 2) or self.verifica2Pozitii(tabla, piesaJucator, 9, 17)),       #1
            (self.verifica2Pozitii(tabla, piesaJucator, 0, 1) or self.verifica2Pozitii(tabla, piesaJucator, 4, 7)),        #2
            (self.verifica2Pozitii(tabla, piesaJucator, 0, 5) or self.verifica2Pozitii(tabla, piesaJucator, 11, 19)),      #3
            (self.verifica2Pozitii(tabla, piesaJucator, 2, 7) or self.verifica2Pozitii(tabla, piesaJucator, 12, 20)),      #4
            (self.verifica2Pozitii(tabla, piesaJucator, 0, 3) or self.verifica2Pozitii(tabla, piesaJucator, 6, 7)),        #5
            (self.verifica2Pozitii(tabla, piesaJucator, 5, 7) or self.verifica2Pozitii(tabla, piesaJucator, 14, 22)),      #6
            (self.verifica2Pozitii(tabla, piesaJucator, 2, 4) or self.verifica2Pozitii(tabla, piesaJucator, 5, 6)),        #7
            (self.verifica2Pozitii(tabla, piesaJucator, 9, 10) or self.verifica2Pozitii(tabla, piesaJucator, 11, 13)),     #8
            (self.verifica2Pozitii(tabla, piesaJucator, 8, 10) or self.verifica2Pozitii(tabla, piesaJucator, 1, 17)),      #9
            (self.verifica2Pozitii(tabla, piesaJucator, 8, 9) or self.verifica2Pozitii(tabla, piesaJucator, 12, 15)),      #10
            (self.verifica2Pozitii(tabla, piesaJucator, 3, 19) or self.verifica2Pozitii(tabla, piesaJucator, 8, 13)),      #11
            (self.verifica2Pozitii(tabla, piesaJucator, 20, 4) or self.verifica2Pozitii(tabla, piesaJucator, 10, 15)),     #12
            (self.verifica2Pozitii(tabla, piesaJucator, 8, 11) or self.verifica2Pozitii(tabla, piesaJucator, 14, 15)),     #13
            (self.verifica2Pozitii(tabla, piesaJucator, 13, 15) or self.verifica2Pozitii(tabla, piesaJucator, 6, 22)),     #14
            (self.verifica2Pozitii(tabla, piesaJucator, 13, 14) or self.verifica2Pozitii(tabla, piesaJucator, 10, 12)),    #15
            (self.verifica2Pozitii(tabla, piesaJucator, 17, 18) or self.verifica2Pozitii(tabla, piesaJucator, 19, 21)),    #16
            (self.verifica2Pozitii(tabla, piesaJucator, 1, 9) or self.verifica2Pozitii(tabla, piesaJucator, 16, 18)),      #17
            (self.verifica2Pozitii(tabla, piesaJucator, 16, 17) or self.verifica2Pozitii(tabla, piesaJucator, 20, 23)),    #18
            (self.verifica2Pozitii(tabla, piesaJucator, 16, 21) or self.verifica2Pozitii(tabla, piesaJucator, 3, 11)),     #19
            (self.verifica2Pozitii(tabla, piesaJucator, 12, 4) or self.verifica2Pozitii(tabla, piesaJucator, 18, 23)),     #20
            (self.verifica2Pozitii(tabla, piesaJucator, 16, 19) or self.verifica2Pozitii(tabla, piesaJucator, 22, 23)),    #21
            (self.verifica2Pozitii(tabla, piesaJucator, 6, 14) or self.verifica2Pozitii(tabla, piesaJucator, 21, 23)),     #22
            (self.verifica2Pozitii(tabla, piesaJucator, 18, 20) or self.verifica2Pozitii(tabla, piesaJucator, 21, 22)),    #23
        ]

        return lista[poz]


    def esteMoara(self, tabla, poz):                                       #verifica daca exista o moara pentru un jucator
                                                                    #in pozitia poz
        piesaJucator = tabla[poz]

        if(piesaJucator == '#'):
            return False

        return self.verificaVecini(tabla, piesaJucator, poz)

    def toatePieseleInMoara(self, jucator):           #verifica daca toate piesele unui jucator se afla in mori
        toateMoara = True
        for i in range(0,24):
            if self.config[i] == jucator:
                if not self.esteMoara(self.config, i):
                    toateMoara = False
                    break

        return toateMoara

    def jucatorOpus(self, jucator):
        if jucator == Joc.JMIN:
            return Joc.JMAX
        else:
            return Joc.JMIN


    def nrValoriPeLinieDeschisa(self, jucator, n):        #returneaza numarul de linii in care nu exista piese apartinand oponentului si in care
                                                                #se afla n piese ale jucatorului
        count = 0
        adversar = self.jucatorOpus(jucator)
        for linie in self.liniiMori:
            valori = [self.config[linie[0]], self.config[linie[1]], self.config[linie[2]]]
            if adversar not in valori:
                nr = valori.count(jucator)
                if nr == n:
                    count += 1

        return count


    def final(self):
        if etapa != 1:
            nrPieseJMIN = self.numarPiese(Joc.JMIN)
            nrPieseJMAX = self.numarPiese(Joc.JMAX)

            nrMutariJMIN = len(self.mutari_joc(Joc.JMIN))
            nrMutariJMAX = len(self.mutari_joc(Joc.JMAX))

            if nrPieseJMIN <= 2 or nrMutariJMIN == 0:
                return Joc.JMAX
            elif nrPieseJMAX <= 2 or nrMutariJMAX == 0:
                return Joc.JMIN
            elif nrMiscariFaraStergere == 20:
                if nrPieseJMAX > nrPieseJMIN:
                    return Joc.JMAX
                elif nrPieseJMAX < nrPieseJMIN:
                    return Joc.JMIN
                else:
                    return 'remiza'
            else:
                return False
        else:
            return False


    def mutari_joc(self, jucator):
        """
        Pentru configuratia curenta de joc "self.config" (de tip lista, cu 24 elemente),
        trebuie sa returnati o lista "l_mutari" cu elemente de tip Joc,
        corespunzatoare tuturor configuratiilor-succesor posibile.

        "jucator" este simbolul jucatorului care face mutarea
        """
        l_mutari = []

        if etapa == 1:                                     #etapa 1: plasarea pieselor fara restrictii
            for i in range(len(self.config)):
                if self.config[i] == Joc.GOL:
                    copieTabla = copy.deepcopy(self.config)
                    copieTabla[i] = jucator

                    if self.esteMoara(copieTabla, i):
                        for j in range(len(copieTabla)):
                            if copieTabla[j] == self.jucatorOpus(jucator) and not self.esteMoara(copieTabla, j):
                                copieTablaStergere = copy.deepcopy(copieTabla)
                                copieTablaStergere[j] = Joc.GOL
                                l_mutari.append(Joc(copieTablaStergere))
                    else:
                        l_mutari.append(Joc(copieTabla))

        else:
            if self.numarPiese(jucator) != 3:            #etapa 2: mutarea de piese in pozitii adiacente
                for i in range(len(self.config)):
                    if self.config[i] == jucator:
                        pozitiiAdiacente = self.pozitiiVecine(i)

                        for poz in pozitiiAdiacente:
                            if self.config[poz] == Joc.GOL:
                                copieTabla = copy.deepcopy(self.config)
                                copieTabla[i] = Joc.GOL
                                copieTabla[poz] = jucator

                                if self.esteMoara(copieTabla, poz):
                                    for j in range(len(copieTabla)):
                                        if copieTabla[j] == self.jucatorOpus(jucator) and not self.esteMoara(copieTabla, j):
                                            copieTablaStergere = copy.deepcopy(copieTabla)
                                            copieTablaStergere[j] = Joc.GOL
                                            l_mutari.append(Joc(copieTablaStergere))
                                else:
                                    l_mutari.append(Joc(copieTabla))

            else:
                for i in range(len(self.config)):            #etapa 3: mutarea de piese in orice pozitie libera cand jucatorul ajunge la 3 piese
                    if self.config[i] == jucator:
                        for j in range(len(self.config)):
                            if self.config[j] == Joc.GOL:
                                copieTabla = copy.deepcopy(self.config)
                                copieTabla[i] = Joc.GOL
                                copieTabla[j] = jucator

                                if self.esteMoara(copieTabla, j):
                                    for k in range(len(copieTabla)):
                                        if copieTabla[k] == self.jucatorOpus(jucator) and not self.esteMoara(copieTabla, k):
                                            copieTablaStergere = copy.deepcopy(copieTabla)
                                            copieTablaStergere[k] = Joc.GOL
                                            l_mutari.append(Joc(copieTablaStergere))
                                else:
                                    l_mutari.append(Joc(copieTabla))

        return l_mutari

    def euristicaNrPiese(self):                         #euristica care se foloseste de numarul de piese ale jucatorilor
        nrPieseJMIN = self.numarPiese(Joc.JMIN)
        nrPieseJMAX = self.numarPiese(Joc.JMAX)

        return nrPieseJMAX - nrPieseJMIN


    def eursiticaNrLiniiDeschise(self):
        linii2PieseJMAX = self.nrValoriPeLinieDeschisa(Joc.JMAX, 2)
        linii2PieseJMIN = self.nrValoriPeLinieDeschisa(Joc.JMIN, 2)
        linii1PiesaJMAX = self.nrValoriPeLinieDeschisa(Joc.JMAX, 1)
        linii1PiesaJMIN = self.nrValoriPeLinieDeschisa(Joc.JMIN, 1)

        return  (2 * linii2PieseJMAX + linii1PiesaJMAX + self.numarPiese(Joc.JMAX)) - (2 * linii2PieseJMIN + linii1PiesaJMIN + self.numarPiese(Joc.JMIN))


    def estimeaza_scor(self, adancime):
        t_final = self.final()
        if t_final == Joc.JMAX:
            return (99 + adancime)
        elif t_final == Joc.JMIN:
            return (-99 - adancime)
        elif t_final == 'remiza':
            return 0
        else:
            if euristica == 1:
                return self.euristicaNrPiese()
            if euristica == 2:
                return self.eursiticaNrLiniiDeschise()

    def __str__(self):
        sir = (
                "[00]" + self.config[0] + "------------------------[01]" + self.config[1] + "------------------------[02]" + self.config[2] + "\n" +
                "  |                            |                            |" + "\n" +
                "  |                            |                            |" + "\n" +
                "  |       [08]" + self.config[8] + "--------------[09]" + self.config[9] + "--------------[10]" + self.config[10] + "       |" + "\n" +
                "  |         |                  |                  |         |" + "\n" +
                "  |         |                  |                  |         |" + "\n" +
                "  |         |       [16]" + self.config[16] + "----[17]" + self.config[17] + "----[18]" + self.config[18] + "       |         |" + "\n" +
                "  |         |         |                 |         |         |" + "\n" +
                "  |         |         |                 |         |         |" + "\n" +
                "[03]" + self.config[3] + "-----[11]" + self.config[11] + "-----[19]" + self.config[19] + "             [20]" + self.config[20] + "-----[12]" + self.config[12] + "-----[04]" +self.config[4] + "\n" +
                "  |         |         |                 |         |         |" + "\n" +
                "  |         |         |                 |         |         |" + "\n" +
                "  |         |       [21]" + self.config[21] + "----[22]" + self.config[22] + "----[23]" + self.config[23] + "       |         |" + "\n" +
                "  |         |                  |                  |         |" + "\n" +
                "  |         |                  |                  |         |" + "\n" +
                "  |       [13]" + self.config[13] + "--------------[14]" + self.config[14] + "--------------[15]" + self.config[15] + "       |" + "\n" +
                "  |                            |                            |" + "\n" +
                "  |                            |                            |" + "\n" +
                "[05]" + self.config[5] + "------------------------[06]" + self.config[6] + "------------------------[07]" + self.config[7] + "\n"
        )

        return sir


class Stare:
    """
    Clasa folosita de algoritmii minimax si alpha-beta
    Are ca proprietate tabla de joc
    Functioneaza cu conditia ca in cadrul clasei Joc sa fie definiti JMIN si JMAX (cei doi jucatori posibili)
    De asemenea cere ca in clasa Joc sa fie definita si o metoda numita mutari_joc() care ofera lista cu
    configuratiile posibile in urma mutarii unui jucator
    """

    ADANCIME_MAX = None

    def __init__(self, tabla_joc, j_curent, adancime, parinte=None, scor=None):
        self.tabla_joc = tabla_joc  # un obiect de tip Joc => „tabla_joc.matr”
        self.j_curent = j_curent  # simbolul jucatorului curent

        # adancimea in arborele de stari
        #	(scade cu cate o unitate din „tata” in „fiu”)
        self.adancime = adancime

        # scorul starii (daca e finala, adica frunza a arborelui)
        # sau scorul celei mai bune stari-fiice (pentru jucatorul curent)
        self.scor = scor

        # lista de mutari posibile din starea curenta
        self.mutari_posibile = []  # lista va contine obiecte de tip Stare

        # cea mai buna mutare din lista de mutari posibile pentru jucatorul curent
        self.stare_aleasa = None

    def jucator_opus(self):
        if self.j_curent == Joc.JMIN:
            return Joc.JMAX
        else:
            return Joc.JMIN

    def mutari_stare(self):
        l_mutari = self.tabla_joc.mutari_joc(self.j_curent)
        juc_opus = self.jucator_opus()

        l_stari_mutari = [Stare(mutare, juc_opus, self.adancime - 1, parinte=self) for mutare in l_mutari]
        return l_stari_mutari

    def __str__(self):
        sir = str(self.tabla_joc) + "(Juc curent:" + self.j_curent + ")\n"
        return sir


""" Algoritmul MinMax """


def min_max(stare):
    # Daca am ajuns la o frunza a arborelui, adica:
    # - daca am expandat arborele pana la adancimea maxima permisa
    # - sau daca am ajuns intr-o configuratie finala de joc
    if stare.adancime == 0 or stare.tabla_joc.final():
        # calculam scorul frunzei apeland "estimeaza_scor"
        stare.scor = stare.tabla_joc.estimeaza_scor(stare.adancime)
        return stare

    # Altfel, calculez toate mutarile posibile din starea curenta
    stare.mutari_posibile = stare.mutari_stare()

    # aplic algoritmul minimax pe toate mutarile posibile (calculand astfel subarborii lor)
    mutari_scor = [min_max(mutare) for mutare in stare.mutari_posibile]

    if stare.j_curent == Joc.JMAX:
        # daca jucatorul e JMAX aleg starea-fiica cu scorul maxim
        stare.stare_aleasa = max(mutari_scor, key=lambda x: x.scor)
    else:
        # daca jucatorul e JMIN aleg starea-fiica cu scorul minim
        stare.stare_aleasa = min(mutari_scor, key=lambda x: x.scor)

    # actualizez scorul „tatalui” = scorul „fiului” ales
    stare.scor = stare.stare_aleasa.scor
    return stare


def alpha_beta(alpha, beta, stare):
    # Daca am ajuns la o frunza a arborelui, adica:
    # - daca am expandat arborele pana la adancimea maxima permisa
    # - sau daca am ajuns intr-o configuratie finala de joc
    if stare.adancime == 0 or stare.tabla_joc.final():
        # calculam scorul frunzei apeland "estimeaza_scor"
        stare.scor = stare.tabla_joc.estimeaza_scor(stare.adancime)
        return stare

    # Conditia de retezare:
    if alpha >= beta:
        return stare  # este intr-un interval invalid, deci nu o mai procesez

    # Calculez toate mutarile posibile din starea curenta (toti „fiii”)
    stare.mutari_posibile = stare.mutari_stare()

    if stare.j_curent == Joc.JMAX:
        scor_curent = float('-inf')  # scorul „tatalui” de tip MAX

        # pentru fiecare „fiu” de tip MIN:
        for mutare in stare.mutari_posibile:
            # calculeaza scorul fiului curent
            stare_noua = alpha_beta(alpha, beta, mutare)

            # incerc sa imbunatatesc (cresc) scorul si alfa
            # „tatalui” de tip MAX, folosind scorul fiului curent
            if scor_curent < stare_noua.scor:
                stare.stare_aleasa = stare_noua
                scor_curent = stare_noua.scor

            if alpha < stare_noua.scor:
                alpha = stare_noua.scor
                if alpha >= beta:  # verific conditia de retezare
                    break  # NU se mai extind ceilalti fii de tip MIN


    elif stare.j_curent == Joc.JMIN:
        scor_curent = float('inf')  # scorul „tatalui” de tip MIN

        # pentru fiecare „fiu” de tip MAX:
        for mutare in stare.mutari_posibile:
            stare_noua = alpha_beta(alpha, beta, mutare)

            # incerc sa imbunatatesc (scad) scorul si beta
            # „tatalui” de tip MIN, folosind scorul fiului curent
            if scor_curent > stare_noua.scor:
                stare.stare_aleasa = stare_noua
                scor_curent = stare_noua.scor

            if beta > stare_noua.scor:
                beta = stare_noua.scor
                if alpha >= beta:  # verific conditia de retezare
                    break  # NU se mai extind ceilalti fii de tip MAX

    # actualizez scorul „tatalui” = scorul „fiului” ales
    stare.scor = stare.stare_aleasa.scor

    return stare


def afis_daca_final(stare_curenta):
    final = stare_curenta.tabla_joc.final()
    if (final):
        if (final == "remiza"):
            print("Remiza!")
            print("Scor jucator: " + str(stare_curenta.tabla_joc.numarPiese(Joc.JMIN)))
            print("Scor calculator: " + str(stare_curenta.tabla_joc.numarPiese(Joc.JMAX)))
        else:
            print("A castigat " + final)
            print("Scor jucator: " + str(stare_curenta.tabla_joc.numarPiese(Joc.JMIN)))
            print("Scor calculator: " + str(stare_curenta.tabla_joc.numarPiese(Joc.JMAX)))

        return True

    return False


def main():
    # initializare algoritm
    global etapa, nrMiscariFaraStergere, euristica, nrMiscariJMIN, nrMiscariJMAX
    raspuns_valid = False
    while not raspuns_valid:
        tip_algoritm = input("Algorimul folosit? (raspundeti cu 1 sau 2)\n 1.Minimax\n 2.Alpha-Beta\n ")
        if tip_algoritm in ['1', '2']:
            raspuns_valid = True
        else:
            print("Nu ati ales o varianta corecta!")

    # initializare dificultate
    raspuns_valid = False
    nivel = [1, 2, 3]
    while not raspuns_valid:
        n = int(input("Nivelul de dificultate:\n 1.Usor\n 2.Mediu\n 3.Avansat\n "))
        if n in nivel:
            if n == 1:
                Stare.ADANCIME_MAX = 2
            if n == 2:
                Stare.ADANCIME_MAX = 4
            if n == 3:
                Stare.ADANCIME_MAX = 6
            raspuns_valid = True
        else:
            print("Trebuie sa introduceti un numar natural intre 1 si 3!")

    raspuns_valid = False
    while not raspuns_valid:
        tip_euristica = input("Euristica folosita? \n 1.Numar de piese\n 2.Numar de linii deschise\n ")
        if tip_euristica in ['1', '2']:
            euristica = int(tip_euristica)
            raspuns_valid = True
        else:
            print("Nu ati ales o varianta corecta!")

    # initializare jucatori
    raspuns_valid = False
    while not raspuns_valid:
        Joc.JMIN = input("Doriti sa jucati cu X sau cu O? ")
        if (Joc.JMIN in Joc.SIMBOLURI_JUC):
            raspuns_valid = True
        else:
            print("Raspunsul trebuie sa fie X sau O.")
    Joc.JMAX = 'O' if Joc.JMIN == 'X' else 'X'

    # initializare tabla
    tabla_curenta = Joc()
    print("Tabla initiala")
    print(str(tabla_curenta))

    # creare stare initiala
    stare_curenta = Stare(tabla_curenta, Joc.JMIN, Stare.ADANCIME_MAX)

    for i in range(18):
        if (stare_curenta.j_curent == Joc.JMIN):
            #plaseaza jucatorul
            t_inainte = int(round(time.time() * 1000))
            raspuns_valid = False
            while not raspuns_valid:
                try:
                    poz = input("\nPlaseaza piesa pe pozitia: ")

                    if poz == 'exit':
                        print("Scor jucator: " + str(stare_curenta.tabla_joc.numarPiese(Joc.JMIN)))
                        print("Scor calculator: " + str(stare_curenta.tabla_joc.numarPiese(Joc.JMAX)))
                        return

                    poz = int(poz)

                    if (poz in range(0, 24)):
                        if stare_curenta.tabla_joc.config[poz] == Joc.GOL:        #daca pozitia e goala
                            stare_curenta.tabla_joc.config[poz] = Joc.JMIN             #plasam piesa
                            if stare_curenta.tabla_joc.esteMoara(stare_curenta.tabla_joc.config, poz):        #daca este moara
                                piesaStearsa = False
                                while not piesaStearsa:
                                    try:
                                        poz = int(input("\nSterge piesa adversarului: "))

                                        if poz in range(0,24):
                                            if stare_curenta.tabla_joc.config[poz] == Joc.JMAX and not stare_curenta.tabla_joc.esteMoara(stare_curenta.tabla_joc.config, poz) or (
                                                    stare_curenta.tabla_joc.esteMoara(stare_curenta.tabla_joc.config, poz) and stare_curenta.tabla_joc.numarPiese(Joc.JMIN) == 3) or (
                                                    stare_curenta.tabla_joc.toatePieseleInMoara(Joc.JMAX)
                                            ):
                                                stare_curenta.tabla_joc.config[poz] = Joc.GOL
                                                piesaStearsa = True
                                            else:
                                                print("\nPozitie invalida!")
                                        else:
                                            print("\nPozitie invalida! (trebuie sa fie un numar intre 0 si 23).")
                                    except ValueError:
                                        print("\nPozitia trebuie sa fie numer intreg!")

                            raspuns_valid = True
                        else:
                            print("\nExista deja o piesa in pozitia ceruta!")
                    else:
                        print("\nPozitie invalida! (trebuie sa fie un numar intre 0 si 23).")

                except ValueError:
                    print("\nPozitia trebuie sa fie numer intreg!")

            print("\nTabla dupa mutarea jucatorului")
            print(str(stare_curenta))

            nrMiscariJMIN += 1

            t_dupa = int(round(time.time() * 1000))
            print("Jucatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")

            if (afis_daca_final(stare_curenta)):
                break

            stare_curenta.j_curent = stare_curenta.jucator_opus()

        else:
            #plaseaza calculatorul
            t_inainte = int(round(time.time() * 1000))
            if tip_algoritm == '1':
                stare_actualizata = min_max(stare_curenta)
            else:  # tip_algoritm==2
                stare_actualizata = alpha_beta(-500, 500, stare_curenta)
            stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc
            print("Tabla dupa mutarea calculatorului")
            print(str(stare_curenta))

            nrMiscariJMAX += 1

            # preiau timpul in milisecunde de dupa mutare
            t_dupa = int(round(time.time() * 1000))
            print("Calculatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")

            if (afis_daca_final(stare_curenta)):
                break

            # S-a realizat o mutare. Schimb jucatorul cu cel opus
            stare_curenta.j_curent = stare_curenta.jucator_opus()

    etapa = 2

    while True:
        if (stare_curenta.j_curent == Joc.JMIN):
            # plaseaza jucatorul
            nrPieseJMAX = stare_curenta.tabla_joc.numarPiese(Joc.JMAX)
            t_inainte = int(round(time.time() * 1000))
            raspuns_valid = False
            while not raspuns_valid:
                try:
                    poz = input("\nMuta piesa de pe pozitia: ")

                    if poz == 'exit':
                        print("Scor jucator: " + str(stare_curenta.tabla_joc.numarPiese(Joc.JMIN)))
                        print("Scor calculator: " + str(stare_curenta.tabla_joc.numarPiese(Joc.JMAX)))
                        return

                    poz = int(poz)

                    if (poz in range(0, 24)):
                        if stare_curenta.tabla_joc.config[poz] == Joc.JMIN:  # daca pozitia are piesa JMIN
                            if(stare_curenta.tabla_joc.numarPiese(Joc.JMIN) == 3):    #daca jucatorul are doar 3 piese(este in etapa 3)
                                piesaPlasata = False
                                while not piesaPlasata:
                                    pozNoua = int(input("\nPozitie noua: "))

                                    if (pozNoua in range(0, 24)):
                                        if stare_curenta.tabla_joc.config[pozNoua] == Joc.GOL:
                                            stare_curenta.tabla_joc.config[poz] = Joc.GOL
                                            stare_curenta.tabla_joc.config[pozNoua] = Joc.JMIN

                                            if stare_curenta.tabla_joc.esteMoara(stare_curenta.tabla_joc.config,
                                                                                 pozNoua):  # daca este moara
                                                piesaStearsa = False
                                                while not piesaStearsa:
                                                    try:
                                                        pozSt = int(input("\nSterge piesa adversarului: "))

                                                        if pozSt in range(0, 24):
                                                            if stare_curenta.tabla_joc.config[
                                                                pozSt] == Joc.JMAX and not stare_curenta.tabla_joc.esteMoara(
                                                                    stare_curenta.tabla_joc.config, pozSt) or (
                                                                    stare_curenta.tabla_joc.esteMoara(
                                                                            stare_curenta.tabla_joc.config,
                                                                            pozSt) and stare_curenta.tabla_joc.numarPiese(
                                                                    Joc.JMIN) == 3) or (stare_curenta.tabla_joc.toatePieseleInMoara(Joc.JMAX)):
                                                                stare_curenta.tabla_joc.config[pozSt] = Joc.GOL
                                                                piesaStearsa = True
                                                            else:
                                                                print("\nPozitie invalida!")
                                                        else:
                                                            print("\nPozitie invalida! (trebuie sa fie un numar intre 0 si 23).")
                                                    except ValueError:
                                                        print("\nPozitia trebuie sa fie numer intreg!")

                                            piesaPlasata = True
                                            raspuns_valid = True

                                        else:
                                            print("\nExista deja o piesa in pozitia ceruta!")
                                    else:
                                        print("\nPozitie invalida! (trebuie sa fie un numar intre 0 si 23).")

                            else:       #daca jucatorul are mai mult de 3 piese (este in etapa 2)
                                vecini = stare_curenta.tabla_joc.pozitiiVecine(poz)          #aflam pozitiile adiacente cu poz
                                pozVecinaLibera = False
                                for p in vecini:
                                    if stare_curenta.tabla_joc.config[p] == Joc.GOL:           #verificam daca exista o pozitie vecina libera
                                        pozVecinaLibera = True
                                        break

                                if pozVecinaLibera:
                                    piesaPlasata = False
                                    while not piesaPlasata:
                                        pozNoua = int(input("\nPozitie noua: "))

                                        if (pozNoua in vecini):
                                            if stare_curenta.tabla_joc.config[pozNoua] == Joc.GOL:
                                                stare_curenta.tabla_joc.config[poz] = Joc.GOL
                                                stare_curenta.tabla_joc.config[pozNoua] = Joc.JMIN

                                                if stare_curenta.tabla_joc.esteMoara(stare_curenta.tabla_joc.config,
                                                                                     pozNoua):  # daca este moara
                                                    piesaStearsa = False
                                                    while not piesaStearsa:
                                                        try:
                                                            pozSt = int(input("\nSterge piesa adversarului: "))
                                                            if pozSt in range(0, 24):
                                                                if stare_curenta.tabla_joc.config[
                                                                    pozSt] == Joc.JMAX and not stare_curenta.tabla_joc.esteMoara(
                                                                    stare_curenta.tabla_joc.config, pozSt) or (
                                                                        stare_curenta.tabla_joc.esteMoara(
                                                                            stare_curenta.tabla_joc.config,
                                                                            pozSt) and stare_curenta.tabla_joc.numarPiese(
                                                                    Joc.JMIN) == 3) or (stare_curenta.tabla_joc.toatePieseleInMoara(Joc.JMAX)):
                                                                    stare_curenta.tabla_joc.config[pozSt] = Joc.GOL
                                                                    piesaStearsa = True
                                                                else:
                                                                    print("\nPozitie invalida!")
                                                            else:
                                                                print("\nPozitie invalida! (trebuie sa fie un numar intre 0 si 23).")
                                                        except ValueError:
                                                            print("\nPozitia trebuie sa fie numer intreg!")

                                                piesaPlasata = True
                                                raspuns_valid = True

                                            else:
                                                print("\nExista deja o piesa in pozitia ceruta!")
                                        else:
                                            print("\nPozitie invalida!")
                                else:
                                    print("\nPiesa este blocata!")

                except ValueError:
                    print("\nPozitia trebuie sa fie numer intreg!")

            print("\nTabla dupa mutarea jucatorului")
            print(str(stare_curenta))

            nrMiscariJMIN += 1

            t_dupa = int(round(time.time() * 1000))
            print("Jucatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")

            nrPieseJMAXNou = stare_curenta.tabla_joc.numarPiese(Joc.JMAX)
            nrMiscariFaraStergere += 1
            if(nrPieseJMAXNou < nrPieseJMAX):
                nrMiscariFaraStergere = 0


            if (afis_daca_final(stare_curenta)):
                break

            stare_curenta.j_curent = stare_curenta.jucator_opus()
        # --------------------------------
        else:  # jucatorul e JMAX (calculatorul)
            # plaseaza calculatorul
            nrPieseJMIN = stare_curenta.tabla_joc.numarPiese(Joc.JMIN)
            t_inainte = int(round(time.time() * 1000))
            if tip_algoritm == '1':
                stare_actualizata = min_max(stare_curenta)
            else:  # tip_algoritm==2
                stare_actualizata = alpha_beta(-500, 500, stare_curenta)
            stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc
            print("Tabla dupa mutarea calculatorului")
            print(str(stare_curenta))

            nrMiscariJMAX += 1

            # preiau timpul in milisecunde de dupa mutare
            t_dupa = int(round(time.time() * 1000))
            print("Calculatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")

            nrPieseJMINNou = stare_curenta.tabla_joc.numarPiese(Joc.JMIN)
            nrMiscariFaraStergere += 1
            if (nrPieseJMINNou < nrPieseJMIN):
                nrMiscariFaraStergere = 0

            if (afis_daca_final(stare_curenta)):
                break

            # S-a realizat o mutare. Schimb jucatorul cu cel opus
            stare_curenta.j_curent = stare_curenta.jucator_opus()

if __name__ == "__main__":
    t_inainte = int(round(time.time() * 1000))
    main()
    t_dupa = int(round(time.time() * 1000))
    print("Meciul a durat " + str(t_dupa - t_inainte) + " milisecunde.")
    print("Numar miscari jucator: " + str(nrMiscariJMIN))
    print("Numar miscari calculator: " + str(nrMiscariJMAX))
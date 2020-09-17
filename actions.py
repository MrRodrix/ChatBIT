# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

import pandas as pd


#TODO: colocar nomes alternativos para disciplinas obrigatórias
cadeiras={
    "matematicadiscreta":"Matemática Discreta I",
    "matemáticadiscreta":"Matemática Discreta I",
    "discreta":"Matemática Discreta I",
    "matematicadiscreta1":"Matemática Discreta I",
    "matemáticadiscreta1":"Matemática Discreta I",
    "discreta1":"Matemática Discreta I",
    "matematicadiscretai":"Matemática Discreta I",
    "matemáticadiscretai":"Matemática Discreta I",
    "discretai":"Matemática Discreta I",
    "discretas1":"Matemática Discreta I",

    "matematicadiscreta2":"Matemática Discreta I",
    "matemáticadiscreta2":"Matemática Discreta I",
    "discretas2":"Matemática Discreta I",
    "matematicadiscreta2":"Matemática Discreta I",
    "matemáticadiscreta2":"Matemática Discreta I",
    "discreta2":"Matemática Discreta I",
    "matematicadiscretaii":"Matemática Discreta I",
    "matemáticadiscretaii":"Matemática Discreta I",
    "discretaii":"Matemática Discreta I",

    "ip":"Introdução à Programação I",
    "ipi":"Introdução à Programação I",
    "ip1":"Introdução à Programação I",
    "prog1":"Introdução à Programação I",
    "programação1":"Introdução à Programação I",
    "programaçao1":"Introdução à Programação I",
    "programacao1":"Introdução à Programação I",
    "progi":"Introdução à Programação I",
    "programaçãoi":"Introdução à Programação I",
    "programacãoi":"Introdução à Programação I",
    "programacaoi":"Introdução à Programação I",

    "ipii":"Introdução à Programação II",
    "ip2":"Introdução à Programação II",
    "prog2":"Introdução à Programação II",
    "programação2":"Introdução à Programação II",
    "programaçao2":"Introdução à Programação II",
    "programacao2":"Introdução à Programação II",
    "progii":"Introdução à Programação II",
    "programaçãoii":"Introdução à Programação II",
    "programaçaoii":"Introdução à Programação II",
    "programacaoii":"Introdução à Programação II",

    "calc":"Cálculo N I",
    "calculo":"Cálculo N I",
    "cálculo":"Cálculo N I",
    "cálc":"Cálculo N I",
    "calc1":"Cálculo N I",
    "calculo1":"Cálculo N I",
    "cálculo1":"Cálculo N I",
    "cálc1":"Cálculo N I",
    "calci":"Cálculo N I",
    "calcn1":"Cálculo N I",
    "calculon1":"Cálculo N I",
    "cálculoni":"Cálculo N I",
    "cálcni":"Cálculo N I",
    "calcni":"Cálculo N I",
    "calculon1":"Cálculo N I",
    "cálculon1":"Cálculo N I",
    "cálcn1":"Cálculo N I",
    "calcni":"Cálculo N I",

    "calcii":"Cálculo N II",
    "calculo2":"Cálculo N II",
    "cálculoii":"Cálculo N II",
    "cálcii":"Cálculo N II",
    "calc2":"Cálculo N II",
    "calculo2":"Cálculo N II",
    "cálculo2":"Cálculo N II",
    "cálcii":"Cálculo N II",
    "calcnii":"Cálculo N II",
    "calculon2":"Cálculo N II",
    "cálculonii":"Cálculo N II",
    "cálcnii":"Cálculo N II",
    "calcn2":"Cálculo N II",
    "calculon2":"Cálculo N II",
    "cálculon2":"Cálculo N II",
    "cálcnii":"Cálculo N II",

    "algoritmos":"Algoritmos e Estruturas de Dados",
    "algo":"Algoritmos e Estruturas de Dados",
    "algorit":"Algoritmos e Estruturas de Dados",
    "algoritmoseestruturadedados":"Algoritmos e Estruturas de Dados",
    "pericles":"Algoritmos e Estruturas de Dados",
    "algoritmo":"Algoritmos e Estruturas de Dados",
    "algoritmoeestruturadedados":"Algoritmos e Estruturas de Dados",
    "algoritmoseestruturadedado":"Algoritmos e Estruturas de Dados",
    "algoritmoeestruturadedado":"Algoritmos e Estruturas de Dados",
    "algoritmoseestruturasdedados":"Algoritmos e Estruturas de Dados",
    "pericleiton":"Algoritmos e Estruturas de Dados",
    "algoritmoeestruturasdedados":"Algoritmos e Estruturas de Dados",
    "algoritmoseestruturasdedado":"Algoritmos e Estruturas de Dados",
    "algoritmoeestruturasdedado":"Algoritmos e Estruturas de Dados"
    
}
class Prereq(Action):

    def name(self) -> Text:
        return "action_prereq"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        cadeira = None
        cadeira = tracker.get_slot("facilitytype")
        #caso o usuario nao bote cadeira ele só ignora
        if cadeira is None or cadeira == '' or cadeira==' ':
            dispatcher.utter_message(text="Não consegui indentificar qual disciplina você deseja saber os pré requisitos, pode escrever de outra forma?")
           
            return [SlotSet("facilitytype", "")]

        #tira os espaços e pesquias pela cadeira no dicionario
        cadeiraA = cadeira.replace(" ","")
        cadeiraA = cadeiraA.lower()
        pre = cadeiras.get(cadeiraA)
        #se n achar
        if pre is None:
            output = "Não consegui encontrar uma disciplina com o nome: " + cadeira
        #se achar falar as cadeiras prereqs
        else:
            #TODO: colocar ementas optativas
            #carrega csv com ementas
            disciplinas = pd.read_csv("files/ementas.csv")
            #pesquisa os prereq pra aquela disciplina
            requisitos=disciplinas[disciplinas['DISCIPLINA']==pre]['PRÉ-REQUISITOS'].values[0]
            
            #se nao for float (padrão para não existe pre req)
            if type(requisitos)!=float:
                #splito a string de prereqs
                vec=requisitos.split(",")
                output = "Os pré requisitos para " + str(pre) + " são:\n"
                for i in range(0, len(vec)):
                    output+=str(i+1)+". "+vec[i]+"\n"
            else:
                output= "A disciplina " + str(pre) + " não possui pré requisitos"
        #enviar output e zerar a entidade disciplina
        dispatcher.utter_message(text=output)
        
        
        return [SlotSet("facilitytype", "")]
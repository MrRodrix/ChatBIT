from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

import pandas as pd

class Prereq(Action):

    def name(self) -> Text:
        return "action_prereq"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        #pego a cadeira q o cara digitou
        cadeira = None
        cadeira = tracker.get_slot("disciplina")

        #vejo se é estagio, se for mando link do informativo geral
        if(cadeira == 'Estágio Supervisionado Obrigatório I' or cadeira == 'Estágio Supervisionado Obrigatório II'):
                dispatcher.utter_message(text="Para mais informações sobre quais os procedimentos do Estágio Supervisionado Obrigatório acesse: http://ww2.bcc.ufrpe.br/content/est%C3%A1gio-supervisionado-obrigat%C3%B3rio-procedimentos")
        else:    
            #caso o usuario nao bote cadeira ou ele nao identifique uma cadeira
            if cadeira is None or cadeira == '' or cadeira==' ':
                dispatcher.utter_message(text="Não consegui indentificar qual disciplina você deseja saber os pré requisitos, pode escrever de outra forma?")
            else:
                #TODO: colocar ementas optativas
                #carrega csv com ementas
                disciplinas = pd.read_csv("files/ementas_obrigatorias.csv")
                disciplinas = disciplinas.append(pd.read_csv("files/ementas_optativas.csv"), ignore_index = True) 
                disciplinas_nomes = [x.lower() for x in disciplinas['DISCIPLINA'].to_list()]
                #pesquisa os prereq pra aquela disciplina
                requisitos = ''
                if cadeira.lower() in disciplinas_nomes:
                    requisitos=disciplinas.loc[[disciplinas_nomes.index(cadeira.lower())]]['PRÉ-REQUISITOS'].values[0]
                else:
                    dispatcher.utter_message(text="Não encontrei a disciplina \""+cadeira+"\" no meu banco de dados")
                    return [SlotSet("disciplina", "")]

                if requisitos!='' and requisitos!=0 and requisitos!='0' and requisitos!='Nenhum':
                    #splito a string de prereqs
                    #é splitado por ","
                    #prepara o output para a cadeira e os requisitos
                    output = "Os pré requisitos para " + str(cadeira) + " são:\n"
                    output+=requisitos+"\n"
                #caso contrario n tem prereq
                else:
                    output= "A disciplina " + str(cadeira) + " não possui pré requisitos"
                #enviar output e zerar a entidade disciplina
                dispatcher.utter_message(text=output)
                
            
        return [SlotSet("disciplina", "")]
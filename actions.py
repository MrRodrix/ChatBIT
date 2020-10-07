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
        cadeira = tracker.get_slot("facilitytype")

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
                disciplinas = pd.read_csv("files/ementas.csv")
                #pesquisa os prereq pra aquela disciplina
                requisitos=0.0
                try:
                    requisitos=disciplinas[disciplinas['DISCIPLINA']==cadeira]['PRÉ-REQUISITOS'].values[0]
                    pass
                except:
                    dispatcher.utter_message(text="Não encontrei a disciplina \""+cadeira+"\" no meu banco de dados")
                    return [SlotSet("facilitytype", "")]
                #se nao for float (padrão para 'não existe pre req')
                if type(requisitos)!=float:
                    #splito a string de prereqs
                    #é splitado por ","
                    vec=requisitos.split(",")
                    #prepara o output para a cadeira e os requisitos
                    output = "Os pré requisitos para " + str(cadeira) + " são:\n"
                    for i in range(0, len(vec)):
                        output+=str(i+1)+". "+vec[i]+"\n"
                #caso contrario n tem prereq
                else:
                    output= "A disciplina " + str(cadeira) + " não possui pré requisitos"
                #enviar output e zerar a entidade disciplina
                dispatcher.utter_message(text=output)
                
            
        return [SlotSet("facilitytype", "")]
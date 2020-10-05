## saudar 1
* saudar
  - utter_saudar

## saudar 2
* saudar
  - utter_saudar
  * help
    - utter_help

## saudar 3
* start
  - utter_saudar

## saber criador
* saber_criador
  - utter_criador

## saber prereq
* prereqs
  - action_prereq

## agradecer
* agradecer
  - utter_disponha

## help
* help
  - utter_help

## piada path negativo
* piada
  - utter_piada
  - utter_continuar
  * recusar
    - utter_ok

## piada path positivo
* piada
  - utter_piada
  - utter_continuar
  * aceitar
    - utter_piada
    - utter_continuar

## despedir
* despedir
  - utter_despedir

## calendario
* calendario
  - utter_duvida_calendario

## carga complementar path sim
* duvida_carga_horaria_complementar
  - utter_duvida_carga_horaria_complementar
  - utter_contatos_coordenacao
  - utter_deseja_categorias
    * aceitar
      - utter_divisao_att_comp

## carga complementar path nao
* duvida_carga_horaria_complementar
  - utter_duvida_carga_horaria_complementar
  - utter_contatos_coordenacao
  - utter_deseja_categorias
    * recusar
      - utter_ok

## carga complementar 2 positivo
* duvida_carga_horaria_complementar2
  - utter_divisao_att_comp
  - utter_ajudou
    * aceitar
      - utter_ok

## carga complementar 2 negativo
* duvida_carga_horaria_complementar2
  - utter_divisao_att_comp
  - utter_ajudou
    * recusar
      - utter_duvida_carga_horaria_complementar2
      - utter_contatos_coordenacao

## carga complementar 3
* duvida_carga_horaria_complementar3
  - utter_duvida_carga_horaria_complementar3

## carga complementar 4
* duvida_carga_horaria_complementar4
  - utter_duvida_carga_horaria_complementar4

## carga complementar 5
* duvida_carga_horaria_complementar5
  - utter_duvida_carga_horaria_complementar5

## carga complementar 6
* duvida_carga_horaria_complementar6
  - utter_duvida_carga_horaria_complementar6

## contatos coordenacao
* contato
  - utter_contatos_coordenacao

## saber professores
* saber_professores
  - utter_saber_professores

## o que são trilhas
* oq_e_trilha
  - utter_oq_e_trilha

## cursar trilhas
* cursar_trilhas
  - utter_cursar_trilhas

## dispensar estagio
* dispensar_estagio
  - utter_dispensar_estagio

## cumprir estagio
* cumprir_estagio
  - utter_cumprir_estagio

## info estagio
* info_estagio
  - utter_info_estagio

## horas para se formar
* horas_necessarias
  - utter_horas_necessarias

## melhor momento p atividades complementares
* qlqr_momento_complementar
  - utter_qlqr_momento_complementar

## após da entrada nas atividades complementares oq acontece
* oq_acontece_apos_entrada_ch_complementar
  - utter_oq_acontece_apos_entrada_ch_complementar

## trabalho em empresa ch complementar path ajudou
* empresa_ch_complementar
  - utter_empresa_ch_complementar
  - utter_ajudou
    * aceitar
      - utter_ok

## trabalho em empresa ch complementar path nao ajudou
* empresa_ch_complementar
  - utter_empresa_ch_complementar
  - utter_ajudou
    * recusar
      - utter_duvida_carga_horaria_complementar2
      - utter_contatos_coordenacao

## não é um segredo
* segredo
  - utter_segredo

## recusar por nada
* recusar
  - utter_ok

## aceitar por nada
* aceitar
  - utter_ok

## New Story

* saudar
    - utter_saudar
* help
    - utter_help
* empresa_ch_complementar{"trabalho":"trabalhei","empresa":"lugar","horas":"horas","ch_complementar":"atividade complementar"}
    - utter_empresa_ch_complementar
    - utter_ajudou
* aceitar
    - utter_ok

## New Story

* saudar
    - utter_saudar
* saber_criador
    - utter_criador
* agradecer
    - utter_disponha

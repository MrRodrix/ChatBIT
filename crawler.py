# Esse arquivo serve para pegar as informações de disciplinas do arquivo pdf no servidor 
# http://www.bcc.ufrpe.br/sites/ww3.bcc.ufrpe.br/files/ementasObrigatorias.pdf
# http://www.bcc.ufrpe.br/sites/ww3.bcc.ufrpe.br/files/ementasOptativas.pdf

import io
import requests
import pdfplumber

discipline_pdf = 'optativas' # optativas // obrigatorias

def clear_string(string):
    string = string.replace('\n', '')
    try:
        while(string[0]==' '):
            string = string[1:]
    except:
        return 0
    while(string[-1]==' '):
        string = string[:-1]
    string = string.split(' ')
    for i in range(len(string)):
        if (len(str(string[i]))>4):
            string[i] = str(string[i]).capitalize() 
        elif (string[i].lower() == 'de' or string[i].lower() == 'do' or string[i].lower() == 'da' or string[i].lower() == 'dos' or string[i].lower() == 'das' or string[i].lower() == 'e' or string[i].lower() == 'para' or string[i].lower() == 'à' or string[i].lower() == 'a' or string[i].lower() == 'o'):
            string[i] = str(string[i]).lower()
        else:
            string[i] = str(string[i]).upper()

    return  " ".join(str(x) for x in string)


def filter_content(content, str_start, str_end):
    content = content[content.index(str_start):]
    index_start = content.index(str_start) + len(str_start) 
    index_end = content.index(str_end)
    ##casos especificos
    if(str_start=='CARGA HORÁRIA TOTAL'): 
        index_start = index_start + 2
    elif (str_start == 'DEPARTAMENTO'):
        try:
            temp_i = content.index('DEPARTAMENTO/UNIDADE ACADÊMICA')
            temp_j = content.index('DEPARTAMENTO:')
            index_start = temp_j + len('DEPARTAMENTO:')  if temp_j < temp_i else temp_i + len('DEPARTAMENTO/UNIDADE ACADÊMICA')
        except:
            try:
                index_start = content.index('DEPARTAMENTO:') + len('DEPARTAMENTO:')
            except:
                index_start = temp_i + len('DEPARTAMENTO/UNIDADE ACADÊMICA')

    return (content[index_start:], str(clear_string(content[index_start:index_end])))


if discipline_pdf == 'obrigatorias':
    url = 'http://www.bcc.ufrpe.br/sites/ww3.bcc.ufrpe.br/files/ementasObrigatorias.pdf'
elif discipline_pdf == 'optativas':
    url = 'http://www.bcc.ufrpe.br/sites/ww3.bcc.ufrpe.br/files/ementasOptativas.pdf'
else:
    print('Escolha uma opção válida para \'discipline_pdf\' (optativas // obrigatorias).')

r = requests.get(url)
f = io.BytesIO(r.content)
pdf = pdfplumber.open(f)
content = ''
#print(pdf.pages[32].extract_text())

for page in pdf.pages:
    print('Loading page: ' + str(pdf.pages.index(page)) + '/' + str(len(pdf.pages)))
    content += '\n'+page.extract_text()

course_info_list = [['DISCIPLINA', 'CÓDIGO', 'DEPARTAMENTO', 'ÁREA', 'CARGA HORÁRIA TOTAL', 'NÚMERO DE CRÉDITOS', 
                    'CARGA HORÁRIA SEMANAL', 'TEÓRICAS', 'PRÁTICAS', 'PRÉ-REQUISITOS', 'EMENTA']]
existe_disciplina = True
i=0
while existe_disciplina:
    i+=1
    if (content.__contains__('DISCIPLINA:') and content.__contains__('CÓDIGO:')):
        content, course_name = filter_content(content, 'DISCIPLINA:', 'CÓDIGO:')
        if len(course_name)>150:
            print('ERROR, please check this discipline in PDF.'+' // ' + str(i))
            continue
            
        print(course_name +' // ' + str(i))
        content, course_code = filter_content(content, 'CÓDIGO:', 'DEPARTAMENTO')
        content, course_dep = filter_content(content, 'DEPARTAMENTO', 'ÁREA:')
        content, course_area = filter_content(content, 'ÁREA:', 'CARGA HORÁRIA')
        content, course_total_hours = filter_content(content, 'CARGA HORÁRIA TOTAL', 'NÚMERO DE CRÉDITOS:')
        content, course_credits = filter_content(content, 'NÚMERO DE CRÉDITOS:', 'CARGA HORÁRIA SEMANAL:')
        content, course_weekly_hours = filter_content(content, 'CARGA HORÁRIA SEMANAL:', '  ')
        
        content, course_teoric_hours = filter_content(content, 'TEÓRICAS:', '  ')
        content, course_pratical_hours = filter_content(content, 'PRÁTICAS:', '  ')
        content, course_prereq = filter_content(content, 'PRÉ-REQUISITOS:', '\n')
        content, course_syllabus = filter_content(content, 'EMENTA', 'CONTEÚDOS')
        
        course_info_list.append([course_name, course_code, course_dep, course_area, 
                                course_total_hours, course_credits, course_weekly_hours, 
                                course_teoric_hours, course_pratical_hours, course_prereq,
                                course_syllabus])
        
    else:
        #print(content)
        existe_disciplina = False


import pandas as pd
my_df = pd.DataFrame(course_info_list)
print(my_df.head())
my_df.to_csv('files/ementas_'+discipline_pdf+'.csv', index=False, header=False)



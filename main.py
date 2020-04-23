import PySimpleGUI as sg
import pandas as pd
import docx # shorten to docx.Document to remove bloat
import os


def retrieveDirPath():
    layout = [[sg.Text('Job Name')],
              [sg.InputText()],
              [sg.Text('Template Form:')],  
              [sg.Input(), sg.FileBrowse()],  
              [sg.Text('Form Folder')],
              [sg.Input(), sg.FolderBrowse()],
              [sg.OK(), sg.Cancel()]]  
    
    window = sg.Window('Equality & Diversity Reader').Layout(layout)  
    
    # The Event Loop  
    while True:  
        event, values = window.Read()  
        if event is None:  
            break
        if event == 'OK':  
            template_path = values[0]
            folder_path = values[1]
            job_name = values[2]
            break
    
    window.Close()
    
    return template_path, folder_path, job_name

def getFolderDocs(directory):
    folder = os.listdir(directory)
    
    for i in folder:
        if i[-4:] != 'docx':
            folder.pop(i)
    
    return folder

def readTemplate(template):
    template_tables = template.tables
    

    demographic_categories = {}
    
    i = 1

    for table in template_tables:
        data = []
    # Iterates over each cell and adds to list
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    data.append(paragraph.text)
    # Removes empty strings in list
        data = [x for x in data if x]

    # Adds dictionary key as the table number, values being a list of possible answers
        demographic_categories['Question ' + str(i)] = data
        i += 1
        
    # Creates list of all possible answers in the form
    template_answers = list(demographic_categories.values())
    template_answers = [inner for outer in template_answers for inner in outer]

    return demographic_categories, template_answers

def createDF(column_names):  
    # Returns list of tuples of all values (answers) with their associated key (question)
    cat_keys = [(i,x) for i in demographic_categories for x in demographic_categories[i]]

    # Creates multilevel dataframe with top level being the question number and the lower level being the possible answers for that question
    df = pd.DataFrame(columns=pd.MultiIndex.from_tuples(cat_keys, names=('Questions', 'Answers')))

    # Fills df with 0 to specify integer values
    df.loc[0, :] = 0
    return df

def retrieveAnswers(doc, template_answers):
    tables = doc.tables
    data = []

    for table in tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    data.append(paragraph.text)
    
    data = [x for x in data if x]
    
    # Finds indices for filled cells that are not in answer cells
    tick_index = [index for index, value in enumerate(data) if value not in template_answers]

    # Map to change each element (x) of list to x-1
    demographic_index = list(map(lambda x: x-1, tick_index))

    # Returns a list of the answers given in doc
    demographics = [e for i, e in enumerate(data) if i in demographic_index]
    
    return demographics, demographic_index

def insertAnswers(template, df, answers, answers_index):
    question_no = 1
    i = 0

    while i in range(0, len(answers)):
    # Question No. corresponds to df
        question = "Question " + str(question_no)
    # If the first answer is in question 1, updates the df count by +1
        if answers[i] in list(df[question].columns):
            df.loc[:, (question, answers[i])] += 1
            print('Added to {} {}'.format(question, answers[i]))
            i += 1
            question_no += 1
        else:
            question_no += 1
    # Catches error if question_no is more than the number of tables
    # Removes string when two answers in the same string, only takes first answer
            if question_no > len(template.tables):
                answers.pop(i)
                question_no = i + 1
            continue
    
    return df





while True:
    template_path, folder_path, job_name = retrieveDirPath()
    try:
        if template_path[-4:] == 'docx':
            template = docx.Document(template_path)
        else:
            break
    except FileNotFoundError:
        break
    
    demographic_categories, possible_answers = readTemplate(template)
    
    df = createDF(demographic_categories)
    
    try:
        folder = getFolderDocs(folder_path)
    except FileNotFoundError:
        break
        
    for filename in folder:
        try:
            doc = docx.Document(filename)
            print(doc)
            answers, answers_index = retrieveAnswers(doc, possible_answers)
            df = insertAnswers(template, df, answers, answers_index)
            
        except:
            print('Error in file {}'.format(filename))
            pass
    try:
        df.loc[:, (df != 0).any(axis=0)].to_excel('{}.xlsx'.format(job_name))
    except:
        break
    
    break

    # Removes any columns with sums = 0

import PySimpleGUI as sg
import pandas as pd
from functions import get_projects
import datetime as dt

sg.theme('Reddit')
project_dd = sg.Combo(
    values= get_projects(),
    key='project_list'
)
event_type = sg.Combo(
    values = ['Insight','Update','Analytics'],
    key='type_of_event'
)

tab1_layout = [
    [sg.T('Select Project Name'), project_dd],
    [sg.T('Select Type of Completed Task'), event_type],
    [sg.T('Description')],
    [sg.Multiline(key='description',size=(40, 4))],
    [sg.Button('Submit'),sg.Button('Close')]
]

headers = {'Date':[],'Project Name':[],'Type of Insight':[],'Description':[]}
table = pd.read_excel('files/insights.xlsx')
headings = list(headers)
values = table.values.tolist()

tab2_layout = [
    [sg.T('Previous Entries')],
    [sg.Table(values=values, 
              headings=headings, 
              auto_size_columns=False, 
              key='table',
              col_widths=list(map(lambda x:len(x)+1, headings)),
              enable_events=True,
              size=[60,10]
              )],
    [sg.Button('Clear All Insights')]
]

layout = [
    [sg.TabGroup([
        [sg.Tab('Add Provided Insight',tab1_layout),
        sg.Tab('See Previous Entries', tab2_layout)]
    ])]
]

window = sg.Window(
    'Project Insight Tracker',
    layout,
    font = ('Helvetica', 12)
)

while True:
    event, values = window.read(timeout=200)

    match event:

        case 'Submit':
            df = pd.read_excel('files/insights.xlsx')
            print(df.columns)
            values['project_list'] = values['project_list'].strip('\n')
            new_item = [dt.datetime.now(), values['project_list'], values['type_of_event'], values['description']]
            df.loc[len(df)] = new_item
            df.to_excel('files/insights.xlsx', index=False)
            window['table'].update(values=df.values.tolist())
            sg.popup('Insight saved!')
            # print(event, values)

        case 'Clear All Insights':
            df = pd.read_excel('files/insights.xlsx')
            df = df[0:0]
            df.to_excel('files/insights.xlsx', index=False)
            window['table'].update(values=df.values.tolist())


        case sg.WIN_CLOSED:
            break
        case 'Close':
            break

window.close()
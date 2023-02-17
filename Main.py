import PySimpleGUI as psg

# Global color def
Color1 = '#272838'
Color2 = '#F9F8F8'
Color3 = '#FF8811'

# BMR calculated with Harris-Benedict Equation
def BMR(weight: float, height: float, age: int, sex: str):
    if sex == 'male':
        bmr = 66 + 13.7 * weight + 5 * height - 6.8 * age
    elif sex == 'female':
        bmr = 655 + 9.6 * weight + 1.8 * height - 4.7 * age
    else:
        exit('Sex error')
    return bmr

# GUI Columns
weightColumn = psg.Column([[psg.Text("Weight [kg]", key='-WEIGHTLABEL-', background_color=Color1, text_color=Color2)],
                           [psg.InputText(key='-WEIGHT-', size=(8,5), background_color=Color2)]], background_color=Color1)
heightColumn = psg.Column([[psg.Text("Height [cm]", key='-HEIGHTLABEL-', background_color=Color1, text_color=Color2)],
                           [psg.InputText(key='-HEIGHT-', size=(8,5), background_color=Color2)]], background_color=Color1)
ageColumn = psg.Column([[psg.Text("Age", background_color=Color1, text_color=Color2)],
                        [psg.Spin([i for i in range(1, 101)], key='-AGE-', initial_value=18, readonly=True, background_color=Color2)]], background_color=Color1)
sexColumn = psg.Column([[psg.Text("Sex", background_color=Color1, text_color=Color2)],
                        [psg.Combo(['male', 'female'], key='-SEX-', readonly=True, background_color=Color2)]], background_color=Color1)
activityColumn1 = psg.Column([[psg.Radio('Sedentary', "ACTIVITY", key='-ACTIVITY1-', default=True, background_color=Color1)],
                              [psg.Text('Little to no exercise', background_color=Color1, text_color=Color2)]], background_color=Color1)
activityColumn2 = psg.Column([[psg.Radio('Lightly Active', "ACTIVITY", key='-ACTIVITY2-', background_color=Color1)],
                              [psg.Text('Exercise 1-3 times / week', background_color=Color1, text_color=Color2)]], background_color=Color1)
activityColumn3 = psg.Column([[psg.Radio('Moderately Active', "ACTIVITY", key='-ACTIVITY3-', background_color=Color1)],
                              [psg.Text('Exercise 3-5 times / week', background_color=Color1, text_color=Color2)]], background_color=Color1)
activityColumn4 = psg.Column([[psg.Radio('Very Active', "ACTIVITY", key='-ACTIVITY4-', background_color=Color1)],
                              [psg.Text('Exercise 6-7 times / week', background_color=Color1, text_color=Color2)]], background_color=Color1)
activityColumn5 = psg.Column([[psg.Radio('Extremely Active', "ACTIVITY", key='-ACTIVITY5-', background_color=Color1)],
                              [psg.Text('Exercise 14 times / week', background_color=Color1, text_color=Color2)]], background_color=Color1)

# GUI Layout
layout = [[psg.Text("Input your data", font=(25), background_color=Color1, text_color=Color2)],
          [weightColumn, heightColumn, ageColumn, sexColumn],
          [psg.Radio('Metric', "SYSTEM", key='-METRIC-', enable_events=True, default=True, background_color=Color1), psg.Radio('Imperial', "SYSTEM", key='-IMPERIAL-', enable_events=True, background_color=Color1)],
          [psg.Text('_'*120, background_color=Color1, text_color=Color2)],
          [psg.Text("Choose activity level", font=(25), background_color=Color1, text_color=Color2)],
          [activityColumn1, activityColumn2, activityColumn3, activityColumn4, activityColumn5],
          [psg.Text("", background_color=Color1)],
          [psg.Button("Results", font=(25), button_color=Color1 + " on " + Color3)]]
window = psg.Window("TDEE Calculator", layout, background_color=Color1)

while(True):
    event, values = window.read()
    if event == psg.WIN_CLOSED:
        break
    elif event == '-IMPERIAL-' or event == '-METRIC-': # Label update with changing system of units
        if values['-METRIC-']:
            window['-WEIGHTLABEL-'].update("Weight [kg]")
            window['-HEIGHTLABEL-'].update("Height [cm]")
        elif values['-IMPERIAL-']:
            window['-WEIGHTLABEL-'].update("Weight [lbs]")
            window['-HEIGHTLABEL-'].update("Height [in]")
        else:
            exit('Radio error')
    elif event == "Results":
        weight = values['-WEIGHT-']
        height = values['-HEIGHT-']
        age = values['-AGE-']
        sex = values['-SEX-']
        if sex == '': # Checking if sex Combo was not empty
            correct = False
        else:
            correct = True
        try: # Checking if user input is float
            temp = float(weight)
            temp = float(height)
        except:
            correct = False
        if not correct:
            psg.popup_ok('Double check your data')
        else:   # Actiivity multipliers are Kath-McArdle multipliers for TDEE aproximation
            if values['-ACTIVITY1-']:
                activityMultiplier = 1.2
            elif values['-ACTIVITY2-']:
                activityMultiplier = 1.375
            elif values['-ACTIVITY3-']:
                activityMultiplier = 1.55
            elif values['-ACTIVITY4-']:
                activityMultiplier = 1.725
            elif values['-ACTIVITY5-']:
                activityMultiplier = 1.9
            else:
                exit('Radio error')
            if values['-METRIC-']: # BMR function calculates on metric units, so converting imperial values before passing
                psg.popup('Your TDEE is ' + str(round(activityMultiplier * BMR(float(weight), float(height), int(age), sex))), background_color=Color1, text_color=Color2, button_color=(Color1, Color3))
            elif values['-IMPERIAL-']:
                psg.popup('Your TDEE is ' + str(round(activityMultiplier * BMR(float(weight)/2.2, 2.54*float(height), int(age), sex))), background_color=Color1, text_color=Color2, button_color=(Color1, Color3))
            else:
                exit('Radio error')
            
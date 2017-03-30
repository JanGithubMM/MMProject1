from Steps3Functions import *

#oefening_chosen = 0         #voor testen
(init_info) = init_steps()
oefening_chosen = menu_steps(init_info, oefening_selected = 0, welcome = True)

while True:
    oefening_uitleg(init_info, oefening_chosen)
    oefening_result = oefening_steps(init_info, oefening_chosen)
    #excelSave(oefeningResult)
    oefening_selected = oefening_chosen  #selecteerd de vorige gekozen oefening in het menu
    oefening_chosen = menu_steps(init_info, oefening_selected, welcome = False)
    #de volgende oefening is gekozen en de uitleg wordt gestart

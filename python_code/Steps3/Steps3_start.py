from Steps3_functions import *

oefening_chosen = 2         #voor testen
aantal_fotos = 10           #voor testen
sensors, screen, screen_w, screen_h, my_font, datalogger, datalogger_sheet, foto_generator = init_steps()
oefening_chosen, aantal_fotos = menu_steps(sensors, screen, screen_w, screen_h, my_font, oefening_selected = 0, welcome = True)


##for oefening_chosen in range(0,11):
##    print(oefening_chosen, get_oefening_naam(oefening_chosen))
##    oefening_uitleg(screen, screen_w, screen_h, my_font, oefening_chosen)
##    #oefening_result = oefening_steps((sensors, screen, screen_w, screen_h, my_font, foto_generator), oefening_chosen, aantal_fotos)    

while True:
    oefening_uitleg(screen, screen_w, screen_h, my_font, oefening_chosen)
    start_tijd_oefening = excel_start_oefening()
    oefening_result = oefening_steps((sensors, screen, screen_w, screen_h, my_font, foto_generator), oefening_chosen, aantal_fotos)
    excel_save(datalogger, datalogger_sheet, start_tijd_oefening, oefening_result, oefening_chosen)
    oefening_selected = oefening_chosen  #selecteerd de vorige gekozen oefening in het menu
    oefening_chosen, aantal_fotos = menu_steps(sensors, screen, screen_w, screen_h, my_font, oefening_selected, welcome = False)
    #de volgende oefening is gekozen en de uitleg wordt gestart

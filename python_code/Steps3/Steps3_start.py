from Steps3_functions import *

oefening_chosen = 1         #voor testen
sensors, screen, screen_w, screen_h, my_font, datalogger, datalogger_sheet, foto_generator = init_steps()
oefening_chosen = menu_steps(sensors, screen, screen_w, screen_h, my_font, oefening_selected = 0, welcome = True)

while True:
    oefening_uitleg(sensors, screen, screen_w, screen_h, my_font, oefening_chosen)
    start_tijd_oefening = excel_start_oefening()
    oefening_result = oefening_steps((sensors, screen, screen_w, screen_h, my_font, foto_generator), oefening_chosen)
    excel_save(datalogger, datalogger_sheet, start_tijd_oefening, oefening_result, oefening_chosen)
    oefening_selected = oefening_chosen  #selecteerd de vorige gekozen oefening in het menu
    oefening_chosen = menu_steps(sensors, screen, screen_w, screen_h, my_font, oefening_selected, welcome = False)
    #de volgende oefening is gekozen en de uitleg wordt gestart

#typed on the computer

def InitSteps():
    Initsensors()
    InitPygameAndScreen()
    fotosLaden


def Initsensors():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    sL = MCP3008(1)     #druksensor links
    sR = MCP3008(3)     #druksensor rechts

def InitPygameAndScreen():  #pygame en screen init
    pygame.init()
    windowInfo = pygame.display.Info()
    screen_size = (windowInfo.current_w,windowInfo.current_h)
    screen_w = windowInfo.current_w
    screen_h = windowInfo.current_h
    #screen_size = (1920,800)            #voor testen met andere schermresolutie
    #screen_w = 800                     #voor testen met andere schermresolutie
    #screen_h = 600                     #voor testen met andere schermresolutie
    screen_ratio = int((screen_w * (4/5)) / screen_h)
    myfont = pygame.font.SysFont("Arial", int(screen_h/25))    


def fotosladen():           #fotos inladen en schalen
        usbStickHasNoPhotos = True
        for file in os.listdir("/home/pi/usbdrv"):
                if file.endswith(".png")|file.endswith(".PNG")|file.endswith(".jpg")|file.endswith(".JPG")|file.endswith(".jpeg")|file.endswith(".JPEG"):
                        usbStickHasNoPhotos = False
                        image = pygame.image.load("/home/pi/usbdrv/"+file)
                        image_ratio = image.get_width()/image.get_height()
                        if image_ratio > screen_ratio:          #zwarte balk aan de zijkant
                                image = pygame.transform.scale(image, (int(screen_h*image_ratio), screen_h))
                        else:                                   #zwarte balk aan de onder en bovenkant
                                image = pygame.transform.scale(image, (screen_w, int(screen_w*image_ratio)))
                        yield image
        if (usbStickHasNoPhotos):
                for file in os.listdir("/home/pi/Pictures/Voorbeeldfotos"):
                        if file.endswith(".png")|file.endswith(".PNG")|file.endswith(".jpg")|file.endswith(".JPG")|file.endswith(".jpeg")|file.endswith(".JPEG"):
                                image = pygame.image.load("/home/pi/Pictures/Voorbeeldfotos/"+file)
                                image = pygame.transform.scale(image, (screen_size))
                                yield image


def InitScreen

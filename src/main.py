import sys
import os
import requests
import json
import sounddevice as sd
from pygame import mixer, _sdl2 as devicer
from time import sleep as wait
from colorama import Fore as fore
from threading import Thread


# Variables
version = "1.0.0"
latest_version = None
developer_mode = False
program_path = ""
data = {
    "audio_cable_name": None,
    "prefered_ai_voice": None
}
logger = None

# Classes
class Logger:
    def logInfo(message: str):
        global developer_mode
        if developer_mode:
            print(fore.WHITE + f"[INFO] {message}")
    def logErr(message: str):
        global developer_mode
        if developer_mode:
            print(fore.LIGHTRED_EX + f"[ERR] {message}")

def clearConsole():
    os.system('cls')

# Functions
def loadData():
    global program_path
    global data
    global logger
    global version

    # Clear Terminal
    clearConsole()

    # Create Logger
    logger = Logger

    # Init Mixer
    mixer.init()

    # Check Pyinstaller
    def check_pyinstaller():
        if getattr(sys, 'frozen', False):
            path = os.path.dirname(sys.executable)
            return path
        return os.path.dirname(os.path.abspath(__file__))
    
    # Set Variable and Change Dir
    logger.logInfo("Finding program path and then changing directory")
    program_path = check_pyinstaller()
    os.chdir(program_path)

    # Attempt to read data file
    logger.logInfo("Attempting to read data folder")
    try:
        # File does exist, read
        with open(rf"{program_path}/data.json", 'r') as data_file:
            data = json.load(data_file)
            logger.logInfo("Successfully loaded data into program")
    except FileNotFoundError:
        # File doesn't exist, write/create
        logger.logInfo("Data file doesn't exist! Creating new file")
        with open(rf"{program_path}/data.json", 'w') as data_file:
            json.dump(data, data_file, indent=4)
            logger.logInfo("Successfully loaded default data into file")
    except Exception as err:
        # Some unknown error idk
        logger.logErr(f"Unknown Error: {err}")
        print("Unknown Error! Please create an issue with the error below in github (or try to delete data file)")
        print(err)
        input(fore.CYAN + "[ENTER]")
        sys.exit()

    # Next Step
    wait(1)
    clearConsole()
    checkUpdates()

def checkUpdates():
    global version
    global latest_version
    print("Checking for Updates...")
    try:
        latest_version = requests.get(rf"https://github.com/deR0R0/TikTok-TTS-Generator/releases/latest")
        latest_version = latest_version.json()
        latest_version = latest_version["tag_name"]
    except Exception as err:
        clearConsole()
        print(fore.RED + rf"Error while checking for update \/")
        print(fore.RED + "Skipping for now...")
        print(err)
        input(fore.LIGHTGREEN_EX + "[ENTER]")
            
    # Check if it's the user's first time booting up the program :D
    clearConsole()
    checkFirstTime()

def checkFirstTime():
    global program_path
    global data
    # Check if it's "empty"
    if data["audio_cable_name"] == None:
        print(fore.CYAN + "Wait! Before you continue, which cable should I stream audio through? (You are able to change later)")
        changeAudioDevice()

    clearConsole()
    mainMenu()

def changeAudioDevice():
    global data
    print(fore.CYAN + "If you are also using VB Virtual Cable, you should look for CABLE ____ (VB-Audio Virtual Cable)!")
    print(fore.LIGHTBLACK_EX + f"Current Selected Audio Device: {data["audio_cable_name"]}")
    audDev_dict = {}
    # Find all devices and list them
    audio_devices = devicer.audio.get_audio_device_names(True) + devicer.audio.get_audio_device_names(False)
    for x in range(len(audio_devices)):
        print(fore.WHITE + f"[{x+1}] {audio_devices[x]}")
        audDev_dict[str(x+1)] = audio_devices[x]
    print(fore.LIGHTRED_EX + "[EXIT] Exit")
    # Ask for user input until they input something related...
    while True:
        audio_device = input(fore.WHITE + "Audio Device To Use: ")
        if audio_device.lower() == "exit":
            return
        if audio_device in list(audDev_dict):
            clearConsole()
            break
        else:
            print(fore.LIGHTRED_EX + "That is not in the list!")
    # Save their preference
    try:
        with open(rf"{program_path}/data.json", 'w') as data_file:
            data["audio_cable_name"] = audDev_dict[audio_device]
            json.dump(data, data_file, indent=4)
    except Exception as err:
        print(fore.LIGHTRED_EX + "An Error has Occured!")
        print(err)

    audDev_dict = None
    audio_device = None
    device = None


def mainMenu():
    global data
    global version
    global latest_version
    print(fore.WHITE + "████████╗██╗██╗░░██╗████████╗░█████╗░██╗░░██╗  ████████╗████████╗░██████╗")
    print("╚══██╔══╝██║██║░██╔╝╚══██╔══╝██╔══██╗██║░██╔╝  ╚══██╔══╝╚══██╔══╝██╔════╝")
    print("░░░██║░░░██║█████═╝░░░░██║░░░██║░░██║█████═╝░  ░░░██║░░░░░░██║░░░╚█████╗░")
    print("░░░██║░░░██║██╔═██╗░░░░██║░░░██║░░██║██╔═██╗░  ░░░██║░░░░░░██║░░░░╚═══██╗")
    print("░░░██║░░░██║██║░╚██╗░░░██║░░░╚█████╔╝██║░╚██╗  ░░░██║░░░░░░██║░░░██████╔╝")
    print("░░░╚═╝░░░╚═╝╚═╝░░╚═╝░░░╚═╝░░░░╚════╝░╚═╝░░╚═╝  ░░░╚═╝░░░░░░╚═╝░░░╚═════╝░")
    if latest_version == version:
        print(fore.GREEN + f"Version: {version} | Up To Date!")
    else:
        print(fore.LIGHTRED_EX + f"Version: {version} | Update Needed: {version} -> {latest_version}")
    print(fore.LIGHTBLACK_EX + f"Selected Audio Device: {data["audio_cable_name"]}")
    print(f"Currently Selected Voice: {data["prefered_ai_voice"]}")
    print(fore.CYAN + "Type the number next to the option!")
    print(fore.WHITE + "[1] Start TTSing")
    print("[2] Change Audio Cable")
    print("[3] Change TTS Voice")
    print("[4] Exit")
    option = input(fore.LIGHTGREEN_EX + "?: ")

    if option == "1":
        clearConsole()
        TTSMenu()
        clearConsole()
        mainMenu()
    elif option == "2":
        clearConsole()
        changeAudioDevice()
        clearConsole()
        mainMenu()
    elif option == "3":
        clearConsole()
        chooseAiVoice()
        clearConsole()
        mainMenu()
    elif option == "4":
        sys.exit()
    else:
        clearConsole()
        print(fore.LIGHTRED_EX + "That is not an option!")
        input("[ENTER]")
        clearConsole()
        mainMenu()

def chooseAiVoice():
    global ai_voice_id
    global nationality_codes
    global human_variants
    global program_path
    global data

    """
    US ENGLISH: en_us_001, en_us_006, en_us_007, en_us_009, en_us_010
    UK ENGLISH: en_uk_001, en_uk_003
    AU ENGLISH: en_au_001, en_au_002
    FRENCH: fr_001, fr_002
    GERMAN: de_001, de_002
    SPANISH: es_female_f6, es_female_fp1, es_mx_female_supermom, es_mx_002, es_male_m3
    PORT: br_003, br_004, br_005
    INDO: id_001
    JAPANESE: jp_001, jp_003, jp_005, jp_006
    KOREAN: kr_003, kr_002, kr_004
    """

    nationality_codes = {
        "1": "en_us",
        "2": "en_uk",
        "3": "en_au",
        "4": "fr",
        "5": "de",
        "6": "es",
        "7": "br",
        "8": "id",
        "9": "jp",
        "10": "kr"
    }

    human_variants = {
        "en_us": [1, 4],
        "en_uk": [0, 2],
        "en_au": [1, 1],
        "fr": [0, 2],
        "de": [1, 1],
        "es": [3, 2],
        "br": [2, 1],
        "id": [1, 0],
        "jp": [3, 1],
        "kr": [1, 2]
    }

    ai_voice_id = ""

    def human():
        def nationality():
            global ai_voice_id
            global nationality_codes
            global human_variants
            print(fore.WHITE + "[1] ENGLISH (US)")
            print("[2] ENGLISH (UK)")
            print("[3] ENGLISH (AU)")
            print("[4] FRENCH")
            print("[5] GERMAN")
            print("[6] SPANISH")
            print("[7] PORTUGUESE")
            print("[8] INDONESIAN")
            print("[9] JAPANESE")
            print("[10] KOREAN")
            while True:
                x = input(fore.LIGHTGREEN_EX + "?: ")
                if x.isnumeric():
                    if int(x) in [1,2,3,4,5,6,7,8,9,10]:
                        break
                    else:
                        print(fore.LIGHTRED_EX + "That is not a choice!")
                        wait(3)
                else:
                    print(fore.LIGHTRED_EX + "Please enter a number!")
                    wait(3)
            ai_voice_id = ai_voice_id + nationality_codes[x]
            clearConsole()
            variant()
        
        def variant():
            global ai_voice_id
            global nationality_codes
            global human_variants
            # List out all of the variants (also yes, this is not the most eff way but whatever)
            print(fore.CYAN + "Choose the gender/variant you would like. (Classic TikTok TTS Is English US, Female 1!)")
            if ai_voice_id == "en_us":
                print(fore.WHITE + "[1] Female 1")
                print("[2] Male 1")
                print("[3] Male 2")
                print("[4] Male 3")
                print("[5] Male 4")
                while True:
                    x = input(fore.LIGHTGREEN_EX + "?: ")
                    if int(x) in [1,2,3,4,5]:
                        break
                    else:
                        print(fore.LIGHTRED_EX + "That is not a choice!")
                        input(fore.LIGHTGREEN_EX + "[ENTER]")
                if int(x) == 1:
                    ai_voice_id = ai_voice_id + "_001"
                elif int(x) == 2:
                    ai_voice_id = ai_voice_id + "_006"
                elif int(x) == 3:
                    ai_voice_id = ai_voice_id + "_007"
                elif int(x) == 4:
                    ai_voice_id = ai_voice_id + "_009"
                elif int(x) == 5:
                    ai_voice_id = ai_voice_id + "_010"
            elif ai_voice_id == "en_uk":
                print(fore.WHITE + "[1] Male 1")
                print("[2] Male 2")
                while True:
                    x = input(fore.LIGHTGREEN_EX + "?: ")
                    if int(x) in [1,2]:
                        break
                    else:
                        print(fore.LIGHTRED_EX + "That is not a choice!")
                        input(fore.LIGHTGREEN_EX + "[ENTER]")
                if int(x) == 1:
                    ai_voice_id = ai_voice_id + "_001"
                elif int(x) == 2:
                    ai_voice_id = ai_voice_id + "_003"
            elif ai_voice_id == "en_au":
                print(fore.WHITE + "[1] Female 1")
                print("[2] Male 1")
                while True:
                    x = input(fore.LIGHTGREEN_EX + "?: ")
                    if int(x) in [1,2]:
                        break
                    else:
                        print(fore.LIGHTRED_EX + "That is not a choice!")
                        input(fore.LIGHTGREEN_EX + "[ENTER]")
                if int(x) == 1:
                    ai_voice_id = ai_voice_id + "_001"
                elif int(x) == 2:
                    ai_voice_id = ai_voice_id + "_002"
            elif ai_voice_id == "fr":
                print(fore.WHITE + "[1] Male 1")
                print("[2] Male 2")
                while True:
                    x = input(fore.LIGHTGREEN_EX + "?: ")
                    if int(x) in [1,2]:
                        break
                    else:
                        print(fore.LIGHTRED_EX + "That is not a choice!")
                        input(fore.LIGHTGREEN_EX + "[ENTER]")
                if int(x) == 1:
                    ai_voice_id = ai_voice_id + "_001"
                elif int(x) == 2:
                    ai_voice_id = ai_voice_id + "_002"
            elif ai_voice_id == "de":
                print(fore.WHITE + "[1] Female 1")
                print("[2] Male 1")
                while True:
                    x = input(fore.LIGHTGREEN_EX + "?: ")
                    if int(x) in [1,2]:
                        break
                    else:
                        print(fore.LIGHTRED_EX + "That is not a choice!")
                        input(fore.LIGHTGREEN_EX + "[ENTER]")
                if int(x) == 1:
                    ai_voice_id = ai_voice_id + "_001"
                elif int(x) == 2:
                    ai_voice_id = ai_voice_id + "_002"
            elif ai_voice_id == "es":
                print(fore.WHITE + "[1] Female 1")
                print("[2] Female 2")
                print("[3] Female 3")
                print("[4] Male 1")
                print("[5] Male 2")
                while True:
                    x = input(fore.LIGHTGREEN_EX + "?: ")
                    if int(x) in [1,2,3,4,5]:
                        break
                    else:
                        print(fore.LIGHTRED_EX + "That is not a choice!")
                        input(fore.LIGHTGREEN_EX + "[ENTER]")
                if int(x) == 1:
                    ai_voice_id = ai_voice_id + "_female_f6"
                elif int(x) == 2:
                    ai_voice_id = ai_voice_id + "_female_fp1"
                elif int(x) == 3:
                    ai_voice_id = ai_voice_id + "_mx_female_supermom"
                elif int(x) == 4:
                    ai_voice_id = ai_voice_id + "_mx_002"
                elif int(x) == 5:
                    ai_voice_id = ai_voice_id + "_male_m3"

            elif ai_voice_id == "br":
                print(fore.WHITE + "[1] Female 1")
                print("[2] Female 2")
                print("[3] Male 1")
                while True:
                    x = input(fore.LIGHTGREEN_EX + "?: ")
                    if int(x) in [1,2,3]:
                        break
                    else:
                        print(fore.LIGHTRED_EX + "That is not a choice!")
                        input(fore.LIGHTGREEN_EX + "[ENTER]")
                if int(x) == 1:
                    ai_voice_id = ai_voice_id + "_003"
                elif int(x) == 2:
                    ai_voice_id = ai_voice_id + "_004"
                elif int(x) == 3:
                    ai_voice_id = ai_voice_id + "_005"

            elif ai_voice_id == "id":
                print(fore.WHITE + "There's only 1 voice for indo, it will be automatically chosen")
                ai_voice_id = ai_voice_id + "_001"
                input("[ENTER]")
            elif ai_voice_id == "jp":
                print(fore.WHITE + "[1] Female 1")
                print("[2] Female 2")
                print("[3] Female 3")
                print("[4] Male 1")
                while True:
                    x = input(fore.LIGHTGREEN_EX + "?: ")
                    if int(x) in [1,2,3,4]:
                        break
                    else:
                        print(fore.LIGHTRED_EX + "That is not a choice!")
                        input(fore.LIGHTGREEN_EX + "[ENTER]")
                if int(x) == 1:
                    ai_voice_id = ai_voice_id + "_001"
                elif int(x) == 2:
                    ai_voice_id = ai_voice_id + "_003"
                elif int(x) == 3:
                    ai_voice_id = ai_voice_id + "_005"
                elif int(x) == 4:
                    ai_voice_id = ai_voice_id + "_006"
            elif ai_voice_id == "kr":
                print(fore.WHITE + "[1] Female 1")
                print("[2] Male 1")
                print("[3] Male 2")
                while True:
                    x = input(fore.LIGHTGREEN_EX + "?: ")
                    if int(x) in [1,2,3]:
                        break
                    else:
                        print(fore.LIGHTRED_EX + "That is not a choice!")
                        input(fore.LIGHTGREEN_EX + "[ENTER]")
                if int(x) == 1:
                    ai_voice_id = ai_voice_id + "_003"
                elif int(x) == 2:
                    ai_voice_id = ai_voice_id + "_002"
                elif int(x) == 3:
                    ai_voice_id = ai_voice_id + "_004"
            
        nationality()
            
            
            
    def character():
        print("character")

    def singing():
        print('singing')

    print(fore.LIGHTBLACK_EX + f"Current Selected Audio Device: {data["prefered_ai_voice"]}")
    # Ask user for type of tts voice they want
    print(fore.CYAN + "Type the number next to the option you want to select")
    print(fore.WHITE + "[1] Normal Human TTS")
    print("[2] Characters")
    print("[3] Singing")
    print(fore.LIGHTRED_EX + "[EXIT] Exit")
    x = input(fore.LIGHTGREEN_EX + "?: ")

    if x == "1":
        clearConsole()
        human()
        clearConsole()
    elif x.lower() == "exit":
        clearConsole()
        mainMenu()
    else:
        clearConsole()
        print(fore.LIGHTRED_EX + "Sorry! That Doesn't Work Right Now!")
        chooseAiVoice()
    # Save when user is done choosing their prefered ai voice
    data["prefered_ai_voice"] = ai_voice_id
    try:
        with open(rf"{program_path}/data.json", 'w') as data_file:
            json.dump(data, data_file, indent=4)
    except Exception as err:
        logger.logErr("Error while writing file for prefered ai voice!")
        logger.logErr(err)
        print(fore.LIGHTRED_EX + "An Error has Occured!")
        print(fore.LIGHTRED_EX + f"Error: {err}")
        input(fore.LIGHTGREEN_EX + "[ENTER]")
        sys.exit()
    

def TTSMenu():
    global data
    global program_path

    audio_device_name = None
    # Prep Work!

    # Get the audio device id
    logger.logInfo("Attempting to get audio device to stream audio through")
    audio_device_name = data["audio_cable_name"]
    # Check if audio device is none
    logger.logInfo("Attempting to check if device id exists")
    if audio_device_name == None:
        logger.logErr("User doesn't have an audio cable set! Telling them to set now")
        clearConsole()
        print(fore.LIGHTRED_EX + "You do not have an audio cable set! Please set one")
        input(fore.LIGHTGREEN_EX + "[ENTER]")
        clearConsole()
        mainMenu()
    # Check if user has a prefered ai voice! If not, prompt them to put in one, otherwise continue
    logger.logInfo("Checking if user has a tts voice set up!")
    if data["prefered_ai_voice"] == None:
        clearConsole()
        print(fore.LIGHTRED_EX + "You have not set the TTS voice yet!")
        print(fore.CYAN + "You will set it up now :D")
        input(fore.LIGHTGREEN_EX + "[ENTER]")
        clearConsole()
        chooseAiVoice()

    # Now init the audio cable
    mixer.quit()
    mixer.init(devicename=audio_device_name)

    # TTS IS HERE!
    clearConsole()
    print(fore.CYAN + "The TTS is Ready To Go!")
    input(fore.LIGHTGREEN_EX + "[ENTER]")
    # KEEP GENERATING
    try:
        while True:
            clearConsole()
            print(fore.CYAN + "What to say? (CTRL + C to Exit!)")
            x = input(fore.LIGHTGREEN_EX + "?: ")
            if not x == "":
                pass
            else:
                print(fore.LIGHTRED_EX + "Message cannot be empty!")
                input(fore.LIGHTGREEN_EX + "[ENTER]")
                clearConsole()


            # Notify user it's loading
            clearConsole()
            print(fore.CYAN + "Downloading...")

            # Send post requests and download the response
            try:
                message = requests.post(url="https://tiktok-tts.weilbyte.dev/api/generate", json={"text": str(x), "voice": data["prefered_ai_voice"]})
                if message.status_code == 200:
                    pass
                elif message.status_code == 400:
                    clearConsole()
                    print(fore.LIGHTRED_EX + "External Server Error!")
                    input(fore.LIGHTGREEN_EX + "[DANG, THAT SUCKS]")
                    return
                elif message.status_code == 500:
                    clearConsole()
                    print(fore.LIGHTRED_EX + "External Server Error!")
                    input(fore.LIGHTGREEN_EX + "[DANG, THAT SUCKS]")
                    return
                elif message.status_code == 503:
                    clearConsole()
                    print(fore.LIGHTRED_EX + "Server Down!")
                    input(fore.LIGHTGREEN_EX + "[WELP, THAT SUCKS]")
                    return



                with open(rf"{program_path}/message.mp3", 'wb') as mp3_file:
                    mp3_file.write(message.content)
            except Exception as err:
                logger.logErr(err)
                print(fore.LIGHTRED_EX + "An Network/Download Error has Occured!")
                print(err)
                input(fore.LIGHTGREEN_EX + "[RETRY]")
                return


            # Attempt to play
            mixer.music.load(rf"{program_path}/message.mp3")
            mixer.music.play()
            clearConsole()
            print(fore.CYAN + "Playing TTS...")

            while mixer.music.get_busy():
                wait(0.1)
            
            clearConsole()
            print(fore.CYAN + "Reseting...")
            mixer.music.unload()
            os.remove(rf"{program_path}/message.mp3")
            print("Done")
    except KeyboardInterrupt:
        return
    


# Run
if __name__ == "__main__":
    loadData()
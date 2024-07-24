from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.ios.xcuitest.base import XCUITestOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput


# override as 'touch' pointer action

def test_music(num1,num2):
    # Desired capabilities
    desired_capabilities = {
        "platformName": "iOS",
        "appium:udid": "00008110-001974661EF2201E",
        "appium:automationName": "XCUITest",
        "appium:bundleId": "com.spotify.client"
    }

    # Load capabilities into options
    options = XCUITestOptions()
    options.load_capabilities(desired_capabilities)

    # Appium server URL
    appium_server_url = 'http://localhost:4723'

    # Initialize the driver
    driver = webdriver.Remote(appium_server_url, options=options)

    # MetaDAta check
    def is_substring(string1, string2):
        return string1 in string2

    actions = ActionChains(driver)
    def scroll(num):
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(191, 650)
        actions.w3c_actions.pointer_action.pointer_down()
        
        actions.w3c_actions.pointer_action.move_to_location(191, num)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

    # Accessing the Library tab
    library = WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.XPATH, "//XCUIElementTypeButton[@name='tabbar-item-collection']"))
    )
    library.click()
    playlist_no=int(num1)
    # Accessing the Liked Songs playlist
    liked_song_playlist = WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.XPATH, f"//XCUIElementTypeCollectionView[@name='YourLibraryContent.collectionView']/XCUIElementTypeCell[{playlist_no}]/XCUIElementTypeOther[2]"))
    )
    liked_song_playlist.click()
    scroll(570)
    n=int(num2)
    cnt = n*2 - 1
    onSong = ''
    count = 0
    slide=0
    while slide<n-1 :
        scroll(577)
        slide+=1

    while cnt < n*2-1+11:
        it = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, f"(//XCUIElementTypeButton[@name='Track.Row'])[{cnt}]"))
        )
        it.click()
        onSong = it.get_attribute('label')
        print(onSong)
        cnt += 2
        count += 1
        if count == 4 :
            scroll(580)
            


    print(onSong)

    # Accessing the currently playing bar
    current_playing = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//XCUIElementTypeOther[@name='Components.UI.PageInformationUnitNowPlayingBar']"))
    )

    currentlableName = current_playing.get_attribute("label")
    print(currentlableName)

    # Check if string1 is a substring of string2
    string1_cleaned = currentlableName.replace(",", "").replace(" ", "")
    string2_cleaned = onSong.replace(",", "").replace(" ", "")
    result = is_substring(string1_cleaned, string2_cleaned)

    if result:
        print('passed')

    # Quit the driver after the operations
    driver.quit()

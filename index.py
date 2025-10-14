import subprocess
import time
import uiautomation as auto
import utils

utils.open_app(r'"C:\Program Files\Google\Chrome\Application\chrome.exe"')
chrome_window = auto.WindowControl(searchDepth=1, ClassName='Chrome_WidgetWin_1')
chrome_window.SetActive()

print("✅ Chrome window activated:", chrome_window.Name)

# 4️⃣ Example: find the address bar and type a URL
addr_bar = chrome_window.EditControl(searchDepth=10)
if addr_bar.Exists():
    addr_bar.Click()
    addr_bar.SendKeys('https://openai.com{ENTER}')
else:
    print("⚠️ Address bar not found.")
    print(utils.get_content_all(chrome_window))
    print(utils.get_content_by_name(chrome_window, name="Open lead profile"))
    lead_profile = utils.get_content_by_name(chrome_window, name="Open lead profile")
    
    if lead_profile:
        print(f"✅ Found lead profile button: {lead_profile}")
        utils.perform_action(lead_profile, "click")
        
        # Wait for the new Chrome window to open
        time.sleep(2)
        
        # Get the new Chrome window (there might be multiple now)
        new_chrome_window = auto.WindowControl(searchDepth=1, ClassName='Chrome_WidgetWin_1')
        if new_chrome_window.Exists():
            print("\n🔍 New Chrome window content:")
            print(utils.get_content_all(new_chrome_window))
        else:
            print("⚠️ New Chrome window not found")
    else:
        print("⚠️ Lead profile button not found")


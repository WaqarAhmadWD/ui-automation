import uiautomation as auto
import utils
utils.open_app(r'"C:\Program Files\Google\Chrome\Application\chrome.exe"')
chrome_window = auto.WindowControl(searchDepth=1, ClassName='Chrome_WidgetWin_1')
chrome_window.SetActive()




chainOfTasks = [
    {"task": "Open lead profile", "action": "click", "keys": None},
    {"task": "Search Google or type a URL", "action": "send_keys", "keys": "https://waqar.website"},
    {"task": "Portfolio - Google Chrome", "action": "click", "keys": None},
]
current_window = chrome_window
for task in chainOfTasks:
    current_window = utils.do_work(current_window, task["task"], task["action"], task["keys"])
    print(utils.get_content_all(current_window))


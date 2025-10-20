import uiautomation as auto
import utils
utils.open_app(r'"C:\Program Files\Google\Chrome\Application\chrome.exe"')
chrome_window = auto.WindowControl(searchDepth=1, ClassName='Chrome_WidgetWin_1')
chrome_window.SetActive()

def do_work(control, work,action="click",keys=None):
    task = utils.get_content_by_name(control, name=work)
    utils.perform_action(task, action, keys)
    current_window = utils.get_current_window()['control']
    return current_window


chainOfTasks = [
    {"task": "Open lead profile", "action": "click", "keys": None},
    {"task": "Search Google or type a URL", "action": "send_keys", "keys": "https://www.google.com"},
]
current_window = chrome_window
for task in chainOfTasks:
    current_window = do_work(current_window, task["task"], task["action"], task["keys"])
    print(utils.get_content_all(current_window))


import subprocess
import time
import uiautomation as auto
import utils
utils.open_app(r'"C:\Program Files\Google\Chrome\Application\chrome.exe"')
chrome_window = auto.WindowControl(searchDepth=1, ClassName='Chrome_WidgetWin_1')
chrome_window.SetActive()

def do_work(control, work):
    task = utils.get_content_by_name(control, name=work)
    if task:
        # Perform action and get back either new window or original control
        window_changed = utils.perform_action(
            task, 
            "click",
        )
        print(f"✅ Found task '{work}': Window changed = {window_changed}")
        if window_changed:
            return task
        else:
            return control
    else:
        print(f"⚠️ Task '{work}' not found")
        return control

new_task = do_work(chrome_window, "Open lead profile")
print(new_task)

# another_new_task = do_work(new_task, "Open in new tab")

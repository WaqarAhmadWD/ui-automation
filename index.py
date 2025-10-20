import uiautomation as auto
import constant
import utils
chrome_window = utils.open_app(r'"C:\Program Files\Google\Chrome\Application\chrome.exe"')['control']
utils.do_work_chain(chrome_window, constant.chainOfTasks)

import subprocess
import time
import uiautomation as auto

from uiautomation import Keys


def get_content_all(control, depth=0, max_depth=15, all_content=None):
    """Recursively print all UI controls in a tree structure"""
    if all_content is None:
        all_content = []
    
    indent = "  " * depth
    try:
        if control.Name != None and control.Name != "":
            all_content.append(control.Name)
        if depth < max_depth:
            children = control.GetChildren()
            for child in children:
                get_content_all(child, depth + 1, max_depth, all_content)
        return all_content
    except Exception as e:
        print(f"{indent}└─ Error reading control: {e}")
        return None

# Helper function to find control by name recursively
def get_content_by_name(control, name=None, depth=0, max_depth=15):
    """Recursively search for a control by name"""
    indent = "  " * depth
    try:
        if control.Name == name:
            return control
        
        if depth < max_depth:
            children = control.GetChildren()
            for child in children:
                result = get_content_by_name(child, name, depth + 1, max_depth)
                if result:
                    return result
    except Exception as e:
        print(f"{indent}└─ Error reading control: {e}")
        return None
    
    return None

def open_app(app_url):
    subprocess.Popen(app_url)
    time.sleep(3)
    return app_url

def perform_action(control, action, keys=None):
    if action == "click":
        control.Click()
    elif action == "send_keys":
        control.SendKeys(Keys)
    elif action == "enter":
        control.Enter()
    elif action == "tab":
        control.Tab()
    elif action == "shift+tab":
        control.Shift+Tab()
    time.sleep(1)

def get_all_windows():
    """Get all current top-level windows with their handles"""
    windows = []
    try:
        for window in auto.GetRootControl().GetChildren():
            if window.ClassName and window.Name:
                windows.append({
                    'handle': window.NativeWindowHandle,
                    'name': window.Name,
                    'class': window.ClassName,
                    'control': window
                })
    except Exception as e:
        print(f"⚠️ Error getting windows: {e}")
    return windows


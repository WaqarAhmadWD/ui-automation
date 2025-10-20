import json
import subprocess
import time
import uiautomation as auto
import os
import google.generativeai as genai
from dotenv import load_dotenv

from uiautomation import Keys

import constant

# Load environment variables
load_dotenv()


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

def open_app(app_url, wait_time=3):
    """Open an application and return its window control"""
    try:
        # Open the application
        subprocess.Popen(app_url)
        time.sleep(wait_time)
        
        # Get the current foreground window (should be the newly opened app)
        window = auto.GetForegroundControl()
        
        if window:
            # Ensure the window is active and in foreground
            try:
                window.SetFocus()
            except:
                pass  # Some windows don't support SetFocus
            
            return {
                'handle': window.NativeWindowHandle,
                'name': window.Name,
                'class': window.ClassName,
                'control': window
            }
        else:
            print(f"⚠️ Could not get window for app: {app_url}")
            return None
    except Exception as e:
        print(f"⚠️ Error opening app: {e}")
        return None

def perform_action(control, action, keys=None):
    if action == "click":
        control.Click()
    elif action == "send_keys":
        control.SendKeys(keys)
        control.SendKeys("{ENTER}")
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

def get_current_window():
    """Get the currently active/focused window"""
    try:
        window = auto.GetForegroundControl()
        if window:
            return {
                'handle': window.NativeWindowHandle,
                'name': window.Name,
                'class': window.ClassName,
                'control': window
            }
    except Exception as e:
        print(f"⚠️ Error getting current window: {e}")
    return None

def do_work(control, work,action="click",keys=None):
    task = get_content_by_name(control, name=work)
    perform_action(task, action, keys)
    current_window = get_current_window()['control']
    return current_window

def do_work_chain(current_window, chainOfTasks):
    for task in chainOfTasks:
        current_window = do_work(current_window, task["task"], task["action"], task["keys"])
    return current_window

def useAi(prompt, data=None, model="models/gemini-2.0-flash"):
 
    # Get API key from environment
    api_key = os.getenv('API_KEY')
 
    # Configure Gemini
    genai.configure(api_key=api_key)
    
 
    ai_model = genai.GenerativeModel(model)
    
    # Combine prompt and data
    full_prompt = constant.get_instruction(prompt, data)
    
    # Generate response
    response = ai_model.generate_content(full_prompt)
    
    # Get text from response object
    response_text = response.text
    
    # Remove markdown code block markers if present
    response_text = response_text.strip()
    if response_text.startswith("```json"):
        response_text = response_text[7:]  # Remove ```json
    elif response_text.startswith("```"):
        response_text = response_text[3:]  # Remove ```
    
    if response_text.endswith("```"):
        response_text = response_text[:-3]  # Remove trailing ```
    
    response_text = response_text.strip()
    
    # Parse JSON to Python dictionary
    try:
        return json.loads(response_text)
    except json.JSONDecodeError as e:
        print(f"⚠️ Error parsing JSON: {e}")
        print(f"Response: {response_text}")
        return None 



def useAiChain(prompt, data=None,current_window=None):
    response = useAi(prompt, data=data)
    chainOfTasks = response["chainOfTasks"]
    latestTask = chainOfTasks[-1]
    print(response["message"])
    if response["completed"]:
        return response["message"]
    else:
        if latestTask["type"] == "open app":
            current_window = open_app(latestTask["task"])['control']
            latestTask["status"] = "success"
        elif latestTask["type"] == "perform action":
            current_window = do_work(current_window, latestTask["task"], latestTask["action"], latestTask["keys"])
            latestTask["status"] = "success"
        return useAiChain(response,get_content_all(current_window),current_window)
   
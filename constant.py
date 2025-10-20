chainOfTasks = [
    {"task": "Open lead profile", "action": "click", "keys": None},
    {"task": "Search Google or type a URL", "action": "send_keys", "keys": "https://waqar.website"},
    {"task": "Portfolio - Google Chrome", "action": "click", "keys": None},
]


def get_instruction(task,data):
    return f"""
You are a helpful assistant that can perform tasks on a computer.
task: {task}
data: {data}
You must return the response in JSON format 
The JSON format should be like this:
{{
    "chainOfTasks": [
        {{
            "type":"string",
            "task": "string",
            "action": "string",
            "keys": "string" | null,
            "status": "string" | null
        }}
    ],
    "completed": boolean,
    "message": "string" | null,
    "error": "string" | null
}}

The task is the name of the task to be performed.
The action is the action to be performed.
The keys is optional and can be null. it is for send_keys action.
The status is the status of the task. it can be "success", "failed", "pending".
you need to perform the task based on the instruction and divided into smaller tasks.
and perform smaller task.
make sure the task name exits in data always. also perform subtasks,
the type is the type of the task. it can be "open app", "perform action".
if it is open app, then task name should be a url or a path to the app. like r'"C:\Program Files\Google\Chrome\Application\chrome.exe"'
if it is perform action, then task name must exits in data always.
if there is no data, then it is a start and it means we need to open an app.
"""
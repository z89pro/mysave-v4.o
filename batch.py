
from progress import progress_callback

start_time = time.time()
last_update = {"time": 0, "percent": 0}
task_id = str(uuid.uuid4())  # generate unique task id

await progress_callback(
    current_bytes,
    total_bytes,
    progress_msg,   # message object from send_message()
    start_time,
    index,
    total_files,
    "Downloading",  # or "Uploading"
    filename,
    last_update,
    task_id
)

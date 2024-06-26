import keyboard
import threading
import time


def background_task(stop_event):
    print("Task started")
    while not stop_event.is_set():
        # Perform long-running task here
        print("ayo")
        time.sleep(1)

    # TODO: Cleanup
    print("Task stopped")


def background_task2(stop_event):
    print("Task 2 started")
    while not stop_event.is_set():
        # Perform long-running task here
        print("a2o")
        time.sleep(1)

    # TODO: Cleanup
    print("Task2 stopped")


def stop_background_task(stop_event):
    if keyboard.is_pressed("esc"):
        stop_event.set()


stop_event = threading.Event()

task_thread = threading.Thread(target=background_task, args=(stop_event,))
task_thread.start()

task_thread2 = threading.Thread(target=background_task2, args=(stop_event,))
task_thread2.start()

keyboard.add_hotkey("esc", stop_background_task, args=[stop_event])

# Keep the main program running, otherwise python exits
keyboard.wait("esc")

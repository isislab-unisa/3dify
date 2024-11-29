import subprocess
import time

def run_process():
    while True:
        try:
            # process = subprocess.Popen(["python", "makehuman/makehuman/makehuman.py"])
            process = subprocess.Popen(["sh", "-c", "Xvfb :99 -screen 0 1024x768x24 & sleep 2 && python makehuman/makehuman/makehuman.py"])
            process.wait()
            
            if process.returncode == 0:
                print("Makehuman exited normally")
                break
            else:
                print(f"Process exited with code {process.returncode}. Restarting...")
        
        except Exception as e:
            print(f"An error occured: {e}. Restarting...")
            
        time.sleep(1)
        
run_process()
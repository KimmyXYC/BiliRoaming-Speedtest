import schedule
import time
import subprocess

def run_script():
    subprocess.call(['python', 'main.py'])

def main():
    schedule.every(10).minutes.do(run_script)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()

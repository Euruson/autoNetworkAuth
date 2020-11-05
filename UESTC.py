import logging, logging.handlers
import os
import platform
import subprocess
import time
import argparse

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.handlers.TimedRotatingFileHandler(
            os.path.abspath(
                os.path.join(os.path.dirname(__file__), "autoNetworkAuth.log")
            ),
            when="midnight",
            backupCount=3,
        )
    ],
)
ping_logger = logging.getLogger("ping")
reconnect_logger = logging.getLogger("reconnect")


def ping():
    if platform.system() == "Windows":
        ping_cmd = ["ping", "www.baidu.com", "-n", "3"]
    else:
        ping_cmd = ["ping", "www.baidu.com", "-c", "3"]
    result = subprocess.run(
        ping_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
    )
    if result.returncode == 0:
        ping_logger.info("Connected to the Internet")
    else:
        ping_logger.warning("Disconnected to the Internet")
    return result.returncode


def reconnect(username, password):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    if platform.system() == "Windows":
        path = r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
    else:
        path = "/usr/local/bin/chromedriver"
    browser = webdriver.Chrome(executable_path=path, options=chrome_options)
    url = "http://aaa.uestc.edu.cn"
    try:
        reconnect_logger.info("Trying to reconnect...")
        browser.get(url)
        form_username = browser.find_element_by_xpath("//input[@id='username']")
        form_username.send_keys(username)
        form_password = browser.find_element_by_xpath("//input[@id='password']")
        form_password.send_keys(password)
        form_btn = browser.find_element_by_xpath("//button[@id='school-login']")
        form_btn.click()
        time.sleep(3)
        browser.quit()
        reconnect_logger.info("Reconnected to the Internet")
    except Exception:
        reconnect_logger.error("Failed to reconnect to the Internet")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Automate network authentication for UESTC"
    )
    parser.add_argument(
        "-u", "--username", type=str, required=True, help="Username to log in"
    )
    parser.add_argument(
        "-p", "--password", type=str, required=True, help="Password corresponding"
    )
    args = parser.parse_args()
    while True:
        if ping() == 0:
            time.sleep(10)
        else:
            reconnect(args.username, args.password)

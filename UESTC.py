import argparse
import json
import logging
import logging.handlers
import os
import platform
import subprocess
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

dir_path = os.path.abspath(os.path.dirname(__file__))


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
        reconnect_logger.error("Failed to reconnect to the Internet", exc_info=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Automated network authentication for UESTC"
    )
    subparsers = parser.add_subparsers(
        help="Get username and password from command line or config file", dest="method"
    )

    parser_a = subparsers.add_parser(
        "cli", help="Get username and password from command line"
    )
    parser_a.add_argument(
        "-u", "--username", type=str, required=True, help="Username to log in"
    )
    parser_a.add_argument(
        "-p", "--password", type=str, required=True, help="Password corresponding"
    )

    parser_b = subparsers.add_parser(
        "config", help="Get username and password from config file"
    )
    parser_b.add_argument(
        "-p",
        "--path",
        type=str,
        default=os.path.join(dir_path, "config.json"),
        help="The path of config file",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.handlers.TimedRotatingFileHandler(
                os.path.join(dir_path, "autoNetworkAuth.log"),
                when="midnight",
                backupCount=3,
            )
        ],
    )
    ping_logger = logging.getLogger("ping")
    reconnect_logger = logging.getLogger("reconnect")

    if args.method == "cli":
        username = args.username
        password = args.password
    else:
        with open(args.path, "r") as f:
            configs = json.load(f)
            username = configs["username"]
            password = configs["password"]
    while True:
        if ping() == 0:
            time.sleep(10)
        else:
            reconnect(username, password)

import inquirer
from platform import platform
from os import system
from rich import print
from shutil import get_terminal_size
from urllib.parse import unquote
import re


# Source: https://github.com/TorhamDev/Better-Movie-finder
def print_banner():
    columns = get_terminal_size().columns
    banner = """
    [green]
    ⢀⡴⠑⡄⠀⠀⠀⠀⠀⠀⠀⣀⣀⣤⣤⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ 
    ⠸⡇⠀⠿⡀⠀⠀⠀⣀⡴⢿⣿⣿⣿⣿⣿⣿⣿⣷⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀ 
    ⠀⠀⠀⠀⠑⢄⣠⠾⠁⣀⣄⡈⠙⣿⣿⣿⣿⣿⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀ 
    ⠀⠀⠀⠀⢀⡀⠁⠀⠀⠈⠙⠛⠂⠈⣿⣿⣿⣿⣿⠿⡿⢿⣆⠀⠀⠀⠀⠀⠀⠀ 
    ⠀⠀⠀⢀⡾⣁⣀⠀⠴⠂⠙⣗⡀⠀⢻⣿⣿⠭⢤⣴⣦⣤⣹⠀⠀⠀⢀⢴⣶⣆ 
    ⠀⠀⢀⣾⣿⣿⣿⣷⣮⣽⣾⣿⣥⣴⣿⣿⡿⢂⠔⢚⡿⢿⣿⣦⣴⣾⠁⠸⣼⡿ 
    ⠀⢀⡞⠁⠙⠻⠿⠟⠉⠀⠛⢹⣿⣿⣿⣿⣿⣌⢤⣼⣿⣾⣿⡟⠉⠀⠀⠀⠀⠀ 
    ⠀⣾⣷⣶⠇⠀⠀⣤⣄⣀⡀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀ 
    ⠀⠉⠈⠉⠀⠀⢦⡈⢻⣿⣿⣿⣶⣶⣶⣶⣤⣽⡹⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀ 
    ⠀⠀⠀⠀⠀⠀⠀⠉⠲⣽⡻⢿⣿⣿⣿⣿⣿⣿⣷⣜⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀ 
    ⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣷⣶⣮⣭⣽⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀ 
    ⠀⠀⠀⠀⠀⠀⣀⣀⣈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀ 
    ⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀ 
    ⠀⠀⠀⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀ 
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠻⠿⠿⠿⠿⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ 
    [/green]                                                
    """
    banner = banner.split("\n")
    banner = "\n".join(line.center(columns) for line in banner)
    print(banner)


def clear_terminal() -> None:
    running = platform()

    if "Windows" in running:
        system("cls")

    elif "Linux" in running:
        system("clear")

    elif "macOS" in running:
        system("clear")


def ask_for_web_page_url() -> str:
    ip_middle_octet = u"(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5]))"
    ip_last_octet = u"(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))"

    regex = re.compile(
        u"^"
        # protocol identifier
        u"(?:(?:https?|ftp)://)"
        # user:pass authentication
        u"(?:\S+(?::\S*)?@)?"
        u"(?:"
        u"(?P<private_ip>"
        # IP address exclusion
        # private & local networks
        u"(?:(?:10|127)" + ip_middle_octet + u"{2}" + ip_last_octet + u")|"
        u"(?:(?:169\.254|192\.168)" + ip_middle_octet + ip_last_octet + u")|"
        u"(?:172\.(?:1[6-9]|2\d|3[0-1])" + \
        ip_middle_octet + ip_last_octet + u"))"
        u"|"
        # IP address dotted notation octets
        # excludes loopback network 0.0.0.0
        # excludes reserved space >= 224.0.0.0
        # excludes network & broadcast addresses
        # (first & last IP address of each class)
        u"(?P<public_ip>"
        u"(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])"
        u"" + ip_middle_octet + u"{2}"
        u"" + ip_last_octet + u")"
        u"|"
        # host name
        u"(?:(?:[a-z\u00a1-\uffff0-9]-?)*[a-z\u00a1-\uffff0-9]+)"
        # domain name
        u"(?:\.(?:[a-z\u00a1-\uffff0-9]-?)*[a-z\u00a1-\uffff0-9]+)*"
        # TLD identifier
        u"(?:\.(?:[a-z\u00a1-\uffff]{2,}))"
        u")"
        # port number
        u"(?::\d{2,5})?"
        # resource path
        u"(?:/\S*)?"
        # query string
        u"(?:\?\S*)?"
        u"$",
        re.UNICODE | re.IGNORECASE
    )

    while True:
        url = input('Please enter the URL: ')
        if re.match(regex, url):
            break
        print('[red]Entered URL is invalid.[/red]')

    return url


def ask_to_select_urls(urls: list[str]) -> str:
    names = [unquote(url.split("/")[-1]) for url in urls]
    choices = [("All", "all")] + [(name, url)
                                  for name, url in zip(names, urls)]

    questions = [
        inquirer.Checkbox(
            "urls",
            message="Select urls to download",
            choices=choices,
        )
    ]
    answers = inquirer.prompt(questions)

    if "all" in answers["urls"]:
        return urls

    return answers["urls"]


def ask_confirmation(message: str) -> bool:
    questions = [
        inquirer.Confirm(
            "save",
            message=message,
            default=True,
        )
    ]
    answers = inquirer.prompt(questions)

    return answers["save"]

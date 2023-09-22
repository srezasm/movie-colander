from cli import *
from platform import platform
from extractor import extract_movie_urls
from rich import print
import webbrowser
from os import system

def main():
    clear_terminal()
    print_banner()
    
    url = ask_for_web_page_url()

    movie_urls = extract_movie_urls(url)
    if len(movie_urls) == 0:
        print('')
    
    dl_urls = ask_to_select_urls(movie_urls)
    for dl in dl_urls:
        if "Linux" in platform() or "macOS" in platform():
            system(f"wget -c {dl}")
        else:
            webbrowser.open(dl)

if __name__ == "__main__":
    main()
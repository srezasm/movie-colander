from cli import *
from platform import platform
from extractor import extract_movie_urls

def main():
    clear_terminal()
    print_banner()
    
    # url = ask_for_web_page_url()
    url = input("Enter URL: ")

    movie_urls = extract_movie_urls(url)
    
    print_movies(movie_urls)

    save = ask_confirmation("Do you want to save the results in a file?")
    if save:
        with open("movies.txt", "w") as f:
            for movie in movie_urls:
                f.write(f"{movie}\n")

    if "Linux" in platform():
        download = ask_confirmation("Download?")


if __name__ == "__main__":
    main()
import sys

import questionary

import save
import web_scrape


def main():
    start = questionary.select(
        "Select Option",
        choices=["Start", "Exit"]
    ).ask()

    if start is None or start == "Exit":
        sys.exit(0)

    if start == "Start":
        extract = questionary.select(
            "Select Scraping Option",
            choices=["Content Only", "Exit"]
        ).ask()

        if extract == "Content Only":
            answer = questionary.text("Enter the Fandom URL:").ask()

            if not answer:
                print("Cannot be empty.")
                return

            print("Scraping data... Please wait.")
            unsave_content = web_scrape.scrape(answer)

            if not unsave_content:
                print("ERROR")
                return

            testing = questionary.select(
                "Select Output Format",
                choices=["CSV", "JSON"]
            ).ask()

            match testing:
                case "CSV":
                    save.save_as_csv(unsave_content)
                case "JSON":
                    save.save_as_json(unsave_content)

        elif extract == "Exit" or extract is None:
            sys.exit(0)

if __name__ == "__main__":

    main()

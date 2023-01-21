import pytube
import ffmpeg
import re
import os
from datetime import date

# Create the regex needed to grab only letters and numbers from title
PATTERN = re.compile(r"[0-9A-Za-z]*")

FILE_PATH_TO_SAVE_TO = r"/home/jaxon/Desktop/flipthis/samples-to-post/"


def create_sanitized_title(original_title: str) -> str:
    # Get date to append to end of file name
    current_date = date.today()
    # Split the title on pattern to only match letters and numbers
    split_title = re.findall(pattern=PATTERN, string=original_title)
    # Filter out any empty strings and whitespace strings, lowercase all elements
    split_title = list(filter(lambda part: part and not part.isspace(), split_title))
    split_title = list(map(lambda part: part.lower(), split_title))
    # Return final title. Each word in title joined by an _ and date appended to end
    return ("_").join(split_title) + f"(DOWNLOADED_{current_date}).mp4"


def main():
    # Check that they have specified a file path
    if not FILE_PATH_TO_SAVE_TO:
        print(
            "You need to specify a file path in the .py file.\nFind the TODO comment at the top."
        )
        return

    # Create the YouTube video object based on user link
    link = input("\nEnter the YouTube link for the sample:\n")
    print("---")
    print("\nFetching and downloading from YouTube (this may take a few seconds)...")

    try:
        yt = YouTube(link)
    except Exception as e:
        print("Something went wrong. Ensure this is a valid YouTube link.")
        return
    
    # Get the raw title of the video and create sanitized file title from it
    raw_title = yt.title
    file_safe_title = create_sanitized_title(raw_title)




if __name__ == "__main__":
    main()

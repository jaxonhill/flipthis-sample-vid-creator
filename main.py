from pytube import YouTube
import ffmpeg
import re
import os
from datetime import date
import pyinputplus as pyip

# Create the regex needed to grab only letters and numbers from title
PATTERN = re.compile(r"[0-9A-Za-z]*")
TIME_PATTERN = re.compile(r"(\d{2}):(\d{2}):(\d{2})")

FILE_PATH_TO_SAVE_ORIGINAL_VIDEO_TO = (
    r"/home/jaxon/Desktop/flipthis/samples-to-post/FILE_TO_MAKE_AND_REMOVE_VIDEOS/"
)

FILE_PATH_FOR_FINISHED_VIDEO = (
    r"/home/jaxon/Desktop/flipthis/samples-to-post/finished-videos/"
)


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


def check_time_input_validity(inputted_time: str) -> bool:
    match = TIME_PATTERN.match(inputted_time)
    # If the time matches the regex, further verify it based on standard time conventions
    if match:
        hours, minutes, seconds = match.groups()
        if int(hours) >= 24:
            return False
        if int(minutes) >= 60 or int(seconds) >= 60:
            return False

        return True

    # If here, there was no match for regex, so just return False
    return False


def convert_inputted_time_to_seconds(inputted_time: str) -> int:
    match = TIME_PATTERN.match(inputted_time)
    hours, minutes, seconds = match.groups()
    return (int(hours) * 3600) + (int(minutes) * 60) + (int(seconds))


def main():
    # Check that they have specified a file path
    if not FILE_PATH_TO_SAVE_ORIGINAL_VIDEO_TO:
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

    # Get the mp4 stream
    highest_resolution_video_stream = yt.streams.get_highest_resolution()

    # Download the video to path set above with sanitized file name
    try:
        path_video_saved_to = highest_resolution_video_stream.download(
            output_path=FILE_PATH_TO_SAVE_ORIGINAL_VIDEO_TO, filename=file_safe_title
        )
    except Exception as e:
        print("Something went wrong when downloading.")
        return

    start_time_seconds = ""
    end_time_seconds = ""

    # Get input for the start_time_seconds of the sample they want to trim from
    while not start_time_seconds and not end_time_seconds:
        # Create a temp variable called inputted_start that will get validated by a regex
        inputted_start = input(
            "\n\nEnter the time you want to START the trim at IN THIS FORMAT (HH:MM:SS):\n"
        )
        # Strip whitespace
        inputted_start = inputted_start.strip()

        # Validate that the time is valid
        isValidTime = check_time_input_validity(inputted_start)
        if not isValidTime:  # If not valid, then continue so the loop runs again
            continue

        # Take the time they entered and make it into int seconds from a string
        start_time_seconds = convert_inputted_time_to_seconds(inputted_start)

        # Create a temp variable called inputted_end that will get validated by a regex
        inputted_end = input(
            "\n\nEnter the time you want to END the trim at IN THIS FORMAT (HH:MM:SS):\n"
        )
        # Strip whitespace
        inputted_end = inputted_end.strip()

        # Validate that the time is valid
        isValidTime = check_time_input_validity(inputted_end)
        if not isValidTime:  # If not valid, then continue so the loop runs again
            continue

        # Take the time they entered and make it into int seconds from a string
        end_time_seconds = convert_inputted_time_to_seconds(inputted_end)

    print(f"\n\nSTART TIME IN SECONDS: {start_time_seconds}")
    print(f"END TIME IN SECONDS: {end_time_seconds}")

    # Start ffmpeg process of trimming
    final_file_name_and_path = f"{FILE_PATH_FOR_FINISHED_VIDEO + file_safe_title}"

    isDownloaded = False

    try:
        # ss = start time, t = trim by how many seconds? So we take end time - start time
        input_stream = ffmpeg.input(
            path_video_saved_to,
            ss=start_time_seconds,
            t=(end_time_seconds - start_time_seconds),
        )
        output = ffmpeg.output(input_stream, final_file_name_and_path, format="mp4")
        output.run()
        isDownloaded = True
    except Exception as e:
        print("Something went wrong with ffmpeg.")

    os.remove(path_video_saved_to)

    if isDownloaded:
        print(f'\n\nSUCCESS! Saved your file to:\n"{final_file_name_and_path}"\n')
    else:
        print("Please retry.")


if __name__ == "__main__":
    main()

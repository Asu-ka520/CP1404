"""
CP1404/CP5632 Assignment 1 - Albums Archive
Name:Hu Zedong
Date started:2026/6/23
Link:https://github.com/Asu-ka520/CP1404/tree/master/cp1404-2026-2-a1-Asu-ka520-main
"""

import csv
import operator
import random

FILENAME = "albums.csv"
STATUS_REQUIRED = 'r'
STATUS_COMPLETED = 'c'


def main():
    print("Albums Archive 1.0 by Your Name")
    albums = load_albums(FILENAME)

    while True:
        display_menu()
        choice = input(">>> ").upper().strip()

        if choice == 'D':
            display_albums(albums)
        elif choice == 'R':
            recommend_album(albums)
        elif choice == 'A':
            add_album(albums)
        elif choice == 'M':
            mark_album_completed(albums)
        elif choice == 'Q':
            save_albums(FILENAME, albums)
            print(f"{len(albums)} albums saved to {FILENAME}\nHave a nice day :)")
            break
        else:
            print("Invalid menu choice")


def display_menu():
    print("\nMenu:")
    print("D - Display all albums")
    print("R - Recommend a random album")
    print("A - Add a new album")
    print("M - Mark an album as completed")
    print("Q - Quit")


def load_albums(filename):
    albums = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if row:
                    title = row[0].strip()
                    artist = row[1].strip()
                    year = int(row[2].strip())
                    status = row[3].strip().lower()
                    albums.append([title, artist, year, status])
        print(f"{len(albums)} albums loaded from {filename}")
    except FileNotFoundError:
        print(f"Error, {filename} not found!")
        print(f"0 albums loaded from {filename}")

    albums.sort(key=operator.itemgetter(3, 2))
    return albums


def save_albums(filename, albums):
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(albums)
    except IOError:
        print(f"Error writing to file {filename}")


def display_albums(albums):
    if not albums:
        print("No albums!")
        return

    max_title_len = max(len(album[0]) for album in albums)
    max_artist_len = max(len(album[1]) for album in albums)

    required_count = 0
    for i, album in enumerate(albums, 1):
        title, artist, year, status = album
        prefix = "*" if status == STATUS_REQUIRED else " "

        if status == STATUS_REQUIRED:
            required_count += 1

        print(f"{prefix}{i}. {title:<{max_title_len}} by {artist:<{max_artist_len}} {year}")

    print(f"{len(albums)} albums in archive. You still want to listen to {required_count} albums.")


def recommend_album(albums):
    required_albums = [album for album in albums if album[3] == STATUS_REQUIRED]

    if not required_albums:
        print("No albums left to listen to!")
        return

    recommended = random.choice(required_albums)
    print("Not sure what to listen to next?")
    print(f"How about... {recommended[0]} by {recommended[1]}?")


def add_album(albums):
    title = get_valid_string("Title: ")
    artist = get_valid_string("Artist: ")
    year = get_valid_number("Year: ", low=0)

    new_album = [title, artist, year, STATUS_REQUIRED]
    albums.append(new_album)

    albums.sort(key=operator.itemgetter(3, 2))
    print(f"{title} by {artist} ({year}) added to Albums Archive.")


def mark_album_completed(albums):
    required_count = sum(1 for album in albums if album[3] == STATUS_REQUIRED)
    if required_count == 0:
        print("No required albums.")
        return

    display_albums(albums)
    print("Enter the number of an album to mark as completed")

    album_index = get_valid_number(">>> ", low=1, high=len(albums)) - 1

    if albums[album_index][3] == STATUS_COMPLETED:
        print(f"You have already completed {albums[album_index][0]}")
    else:
        albums[album_index][3] = STATUS_COMPLETED
        albums.sort(key=operator.itemgetter(3, 2))
        print(f"{albums[album_index][0]} by {albums[album_index][1]} completed!")


def get_valid_string(prompt):
    while True:
        user_input = input(prompt).strip()
        if user_input:
            return user_input
        print("Input cannot be blank")


def get_valid_number(prompt, low, high=None):
    while True:
        try:
            value = int(input(prompt))
            if value <= low - 1:
                print(f"Number must be > {low - 1}")
            elif high is not None and value > high:
                print("Invalid album number")
            else:
                return value
        except ValueError:
            print("Invalid input; enter a valid number")


if __name__ == '__main__':
    main()
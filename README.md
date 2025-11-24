# Django Blind Test Game 🎵🎤

## Introduction

Blind Test Game is a fun and interactive application that lets users enjoy a music guessing game. With a database of songs categorized by difficulty, genre, and other attributes, the application randomly selects songs and displays the corresponding YouTube video. Players can play the video and let others guess the song's name, artist, or other details, making it a perfect choice for parties, team-building events, or casual entertainment.

The application is powered by Daphne to handle WebSocket connections, enabling real-time interactions between the server and players.

Features
* 🎶 Dynamic Song Selection: Randomly selects songs based on difficulty and genre preferences.
* 🎥 YouTube Integration: Displays YouTube videos related to the selected songs.
* 📂 Comprehensive Database: Stores songs with detailed metadata like artist, genre, year, and difficulty.
* ⚡ Real-Time Gameplay: Utilizes WebSocket connections for smooth, responsive gameplay.
* 🏆 Customizable Gameplay: Players can adjust settings such as difficulty and genre.


## Models Overview
### Artist
* Stores artist information, including their name, Spotify ID, genre, and avatar.
* Example Fields:
    * name, spotify_id, genre, spotify_avatar, created_on.

### Song
* Represents individual songs with metadata such as artist, genre, YouTube video ID, and difficulty level.
* Features properties like enriched, youtube_watch_link, and period for enhanced functionality.
* Supports subcategories through proxy models (PopSong, RapSong, RnBSong).

### SongConsumer
* A WebSocket consumer for managing game interactions in real-time.
* Core Features:
    * Dynamic song fetching based on difficulty and genre.
    * Randomized song selection while avoiding duplicates.
    * Sends game events like starting the game and fetching songs.

This project combines Django’s robust database management with Daphne’s real-time capabilities, creating an engaging and seamless music experience. 🎉



https://vuejsexamples.com/one-time-passcode-input-for-vue/
https://vuejsexamples.com/page-speed-dev-simplifying-web-performance-sharing/
https://vuejsexamples.com/a-javascript-consent-script-that-interacts-directly-with-google-tag-manager-consent-overview/

## Connection process

The admin of the database connects to the blindtest admin `frontend` and establishes a WebSocket connection which creates a new Firebase ID. 
This connection allows real-time communication between the admin interface and the game instances, enabling features like live updates and player interactions.

The Firebase ID is used to uniquely identify each game session and its associated players, ensuring that all interactions are properly routed and managed.

https://example.com/blind-test -> UNIQUE_ID_123 -> https://example.com/tv/ -> Enters unique ID 


## Mode Ultimate

- Every wrong answer costs points (which depend on the difficulty of the song)
- Every right answer gives points based on the difficulty of the song
- The player who gives the right answer gains points and every other player loses a certain amount of points based on their ranking
- A player can multiply their points based on how fast they answer (first: x3, second: x2, third: x1.5, others: x1)
- A player can multiply theirt points if he answers in a row without making mistakes (2 in a row: x1.5, 3 in a row: x2, 4 in a row: x3, 5+ in a row: x4)
- A player can multiply their points based on the difficulty of the song (easy: x1, medium: x1.5, hard: x2)
- A player can multiply their points if he answers a song which genre matches his favorite genre (x1.5)
- A player must obtain 5 points or more in each category to win the game

## Jokers

- Player steals the points of another player if he answers right and inversely the other player loses points if he answers wrong
- Player steals 1 point from every other player if he answers right but makes every other player gain 1 point if he answers wrong
- Player can double his points if he answers right but loses double points if he answers wrong

### Special Jokers

Obtained after answers a certain number of songs correctly in a row:

- Perfect Combo: If a player answers 10 songs correctly in a row, they earn the "Perfect Combo" joker. This joker allows them to double their points for the next 5 songs they answer, regardless of whether they answer correctly or incorrectly.

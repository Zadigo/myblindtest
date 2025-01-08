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

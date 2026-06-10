# Go Jokers

This mico-service is designed to host the different jokers used for the blindtest game. It is responsible for managing the jokers, their effects and the points system. This is decoupled from the main game logic to allow for more flexibility and scalability. The jokers can be easily added, modified or removed without affecting the core game mechanics.

## Jokers

- Player steals the points of another player if he answers right and inversely the other player loses points if he answers wrong
- Player steals 1 point from every other player if he answers right but makes every other player gain 1 point if he answers wrong
- Player can double his points if he answers right but loses double points if he answers wrong

## Special Jokers

Obtained after answers a certain number of songs correctly in a row:

- Perfect Combo: If a player answers 10 songs correctly in a row, they earn the "Perfect Combo" joker. This joker allows them to double their points for the next 5 songs they answer, regardless of whether they answer correctly or incorrectly.

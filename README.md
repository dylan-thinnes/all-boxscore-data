Running the following commands (first command will take an hour, second command
will take 3 days, last command will take half a minute).

```sh
# Downloading 119 leagues, 10s/league (rate limiting) gives 19m, 50s to run this command
./download-all-leagues
# Downloading 17950 games, 10s/game (rate limiting) gives 2d, 1h, 51m, 40s to run this command
./download-all-games
# Extract the scoring data from the HTML for each game
# Faster version ./extract-scoring.py full-download/*.htm
parallel -n 10 ./extract-scoring.py -- full-download/*.htm > output.json
# Extract actual plays and a summary via jq, along with validation info
./extract-plays-and-summary.jq output.json > full.json
```

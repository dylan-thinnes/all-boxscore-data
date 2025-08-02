Running the following commands (first command will take an hour, second command
will take 3 days, last command will take half a minute).

```bash
./download-all-leagues
./download-all-games
# ./extract-scoring.py *.htm
parallel -n 10 ./extract-scoring.py -- *.htm
```

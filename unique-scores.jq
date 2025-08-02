#!/usr/bin/env -S jq -s -r -f
def order_by_winner:
  if .scores[0] > .scores[1]
  then .scores |= reverse | .rows[].score_diff |= reverse
  else .
  end
  ;

def scoring_histogram:
    .rows
  | map(.score_diff | join(" "))
  | reduce .[] as $item ({}; .[$item] += 1)
  | to_entries | sort | from_entries
  ;

  map(select(.valid))
| map(order_by_winner)
| map(.scoring_histogram = scoring_histogram)
| group_by(.scores)
| map(group_by(.scoring_histogram))
| map(
    { "scores": .[0][0].scores | join(" - ")
    , "unique_ways_count": length
    , "ways_count": map(length) | add
    , "ways":
      map(
        { "count": length
        , "scoring_histogram": .[0].scoring_histogram
        })
    })
| sort_by(.unique_ways_count)
| reverse

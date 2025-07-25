#!/usr/bin/env -S jq -r -f
def score_names:
  { "7": "touchdown + 1 pt conversion"
  , "6": "touchdown"
  , "8": "touchdown + 2 pt conversion"
  , "2": "safety"
  , "3": "field goal"
  }
  ;

  map([.vis_team_score, .home_team_score])    # extract both running scores after event
| [[0,0]] + .                                 # pad with the starting 0,0 score
| [.[0:-1], .[1:]] | transpose                # pair off consecutive scores
| map(transpose) | map(map(.[1] - .[0]))      # subtract consecutive scores from each other to get delta of each event
| map(map(score_names[tostring]))             # map each delta to a score name, null if no score exists
| map
  ( "visiting team scores " + (.[0] | values) # prepend "visiting team scores" to non-null score events on left side of scoreboard
  , "home team scores " + (.[1] | values)     # prepend "home team scores" to non-null score events on left side of scoreboard
  )
| .[]                                         # pull all summaries out of array

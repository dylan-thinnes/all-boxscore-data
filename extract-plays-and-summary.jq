#!/usr/bin/env -S jq -r -f
def score_names:
  { "7": "touchdown + 1 pt conversion"
  , "6": "touchdown"
  , "8": "touchdown + 2 pt conversion"
  , "2": "safety"
  , "3": "field goal"
  }
  ;

def score_diffs:
    .rows
  | map([.vis_team_score, .home_team_score])
  | [[0,0]] + .
  | [.[0:-1], .[1:]]
  | transpose
  | map(transpose | map(.[1] - .[0]))
  ;

def spread_quarters:
    reduce .[] as $item
      ( {"rows": [], "quarter": null}
      ; (($item.quarter | numbers) // .quarter) as $new_quarter
      | .quarter |= $new_quarter
      | .rows |= . + [$item | .quarter = $new_quarter]
      )
  | .rows
  ;

def annotated_rows:
    [.rows, score_diffs]
  | transpose
  | map(.[0].score_diff = .[1] | .[0])
  | spread_quarters
  ;

def row_summary:
    .score_diff
  | map(score_names[tostring])
  | ( "Visiting team scores " + (.[0] | values)
    , "Home team scores " + (.[1] | values)
    )
  ;

def padded:
    tostring
  | " " + ([range(2 - length)] | map(" ") | join("")) + . + " "
  ;

def rows_summary:
    .rows
  | map("\(.vis_team_score | padded) - \(.home_team_score | padded) | " + row_summary)
  | ["AWAY | HOME | SUMMARY", .[]]
  ;

  .rows = annotated_rows
#| .summary = rows_summary

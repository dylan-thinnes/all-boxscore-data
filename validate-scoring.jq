#!/usr/bin/env -S jq -r -f
def final_rows_score:
    [{vis_team_score: 0, home_team_score: 0}] + .rows
  | .[-1]
  | [.vis_team_score, .home_team_score]
  ;

def pad2: tostring | ([range(2 - length) | " "] | join("")) + .;
def pad2_list: map(pad2) | join(" ");

  select(final_rows_score != .scores)
| "\(.url) \(.scores | pad2_list) \(final_rows_score | pad2_list) \(.rows | length | pad2)"

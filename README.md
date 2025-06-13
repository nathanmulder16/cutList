~~~ cutList ~~~

This program is for outputting a cut list of dimensional lumber for woodworking projects.

Provide .csv with columns:
    Description | Quantity | Length | W x H
    example1    | 3        | 60     | 2 x 4
    example2    | 2        | 15     | 2 x 4
    example3    | 4        | 20     | 4 x 4

MVP is
1.) Takes csv as input
2.) Produces a horizontal stacked bar graph of the pieces

Use uv, ruff, pytest, pandas, matplotlib, sql

Future features:
- post to streamlit or dashly
- have a more user friendly way of adding cut lengths
- ripping boards option
- factor for blade kerf
- factor for additional length of pieces to be removed during final assembly
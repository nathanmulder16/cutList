# Cutlist
This program is for outputting a cut list of dimensional lumber for woodworking projects.

### Usage
1. Enter in data via .csv file, adding rows via UI, or both.
2. Produces horizontal stacked bar graphs of the boards

### .csv file format
| Description | Quantity | Length | W x H |
| ----------- | -------- | ------ | ----- |
| example1    | 3        | 60     | 2 x 4 |
| example2    | 2        | 15     | 2 x 4 |
| example3    | 4        | 20     | 4 x 4 |

#### Built with:
- streamlit
- plotly
- pandas
- uv
- ruff 
- pytest
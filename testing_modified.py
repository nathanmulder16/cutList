import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random


def create_stacked_chart(x_data, y_data, z_data, project_title):

    data = {"x": [i for i in range(len(x_data))], "duration": y_data, "type": x_data}
    df = pd.DataFrame(data)


    df["cut_id"] = z_data
    print(df["cut_id"].unique())
    # [ ]: go through unique list and assign a color from color list
    # [ ]: if out of colors, reset the list
    # [ ]: create a df["color"] that correlates with cut_id
    
    df.drop(["x"], axis=1, inplace=True)
    print(df)
    # set for remembering types
    remember = set()
    fig = go.Figure()
    for duration, text, cut in zip(df.duration, df.type, df.cut_id):
        fig.add_bar(
            x=[duration],
            y=[text],
            # marker_color=color,
            # marker_color=df["cut_id"],
            orientation="h",
            # hovertext=cut,
            showlegend=cut not in remember,  # decide if trace is shown in legend
            name=cut,
            text=cut,
            textposition="auto",
        )
        remember.add(cut)  # add current type to set

    fig.update_layout(
        xaxis={"categoryorder": "array", "categoryarray": []},
        title={
            "text": f"<b>{project_title}</b>",
            "y": 0.97,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
        },
        xaxis_title="Length (in)",
        yaxis_title="Board #",
        legend=dict(
            title="Cut Length",
            orientation="h",
            yanchor="top",
            y=1.5,
            xanchor="left",
            x=0,
        ),
        showlegend=True,
        width=1200,
        height=250,
        colorway=[
            "#2E91E5",
            "#E15F99",
            "#1CA71C",
            "#FB0D0D",
            "#DA16FF",
            "#222A2A",
            "#B68100",
            "#750D86",
            "#EB663B",
            "#511CFB",
            "#00A08B",
            "#FB00D1",
            "#FC0080",
            "#B2828D",
            "#6C7C32",
            "#778AAE",
            "#862A16",
            "#A777F1",
            "#620042",
            "#1616A7",
            "#DA60CA",
            "#6C4516",
            "#0D2A63",
            "#AF0038",
        ],
    )

    fig.update_traces(marker=dict(line=dict(width=0.25, color="black")))

    # switch to stacked bar
    fig.update_layout(barmode="stack")
    fig.show()


print(px.colors.qualitative.Dark24)

# using the event type from this dict
color_map = {
    "create": "#3288bd",
    "update": "#fee08b",
    "delete": "#4d4d4d",
    "paste": "#fc8d59",
    "copy": "#fc8d59",
    "copy_paste": "#fc8d59",
    "run_success": "#99d594",
    "run_fail": "#d53e4f",
    "enter_focus": "#e0e0e0",
    "exit_focus": "#e0e0e0",
}

# x_data = [random.choice([*color_map.keys()]) for _ in range(40)]
y_data = [60.0, 15.0, 15.0, 60.0, 60.0, 45.0, 45.0]
# y_data = [random.random() for _ in range(40)]
x_data = [1, 1, 1, 2, 3, 4, 4]
z_data = ["60.0", "15.0", "15.0", "60.0", "60.0", "45.0", "45.0"]
fig = create_stacked_chart(x_data, y_data, z_data, "Cut List")

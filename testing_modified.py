import pandas as pd
import plotly.graph_objects as go


def create_stacked_chart(x_data, y_data, z_data, project_title):

    data = {"length": y_data, "board_id": x_data, "cut_id": z_data, "color": ""}
    df = pd.DataFrame(data)

    kerf_color = "#FB0D0D"

    color_options = [
        "#2E91E5",
        "#E15F99",
        "#1CA71C",
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
    ]

    unique_cuts = df["cut_id"].unique()
    unique_color_counter = 0
    for unique_cut in unique_cuts:
        if unique_cut == "kerf":
            df.loc[df["cut_id"] == unique_cut, "color"] = kerf_color
        else:
            unique_color = color_options[unique_color_counter]
            df.loc[df["cut_id"] == unique_cut, "color"] = unique_color
            unique_color_counter = (unique_color_counter + 1) % len(color_options)

    # set for remembering types
    remember = set()
    fig = go.Figure()
    for length, text, cut, color in zip(df.length, df.board_id, df.cut_id, df.color):
        fig.add_bar(
            x=[length],
            y=[text],
            marker_color=color,
            orientation="h",
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
            orientation="v",
            yanchor="top",
            y=1.5,
            xanchor="left",
            x=0,
        ),
        showlegend=True,
        # width=1200,
        # height=250,
    )
    fig.update_traces(marker=dict(line=dict(width=1, color="black")))

    # switch to stacked bar
    fig.update_layout(barmode="stack")
    fig.show()


# x_data = [random.choice([*color_map.keys()]) for _ in range(40)]
y_data = [60.0, 15.0, 0.125, 15.0, 60.0, 60.0, 45.0, 45.0]
# y_data = [random.random() for _ in range(40)]
x_data = [1, 1, 1, 1, 2, 3, 4, 4]
z_data = ["60.0", "15.0", "kerf", "15.0", "60.0", "60.0", "45.0", "45.0"]
fig = create_stacked_chart(x_data, y_data, z_data, "2x4")

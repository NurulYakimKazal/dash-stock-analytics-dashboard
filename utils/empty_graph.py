import plotly.graph_objects as go


def empty_chart(message):

    fig = go.Figure()

    fig.add_annotation(
        text=message,
        x=0.5,
        y=0.5,
        xref="paper",
        yref="paper",
        showarrow=False,
        font=dict(size=16),
    )

    fig.update_layout(
        height=150,
        xaxis_visible=False,
        yaxis_visible=False,
        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20,
        )
    )

    return fig
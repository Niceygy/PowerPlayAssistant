import plotly.graph_objs as go
from server.database.database import StarSystem, PowerData
import numpy as np

def frequency_map(session):
    systems = session.query(PowerData, StarSystem).join(
        StarSystem,
        PowerData.system_name == StarSystem.system_name,
    ).filter(StarSystem.frequency > 500).all()

    lats = [s.StarSystem.latitude for s in systems]
    lons = [s.StarSystem.longitude for s in systems]
    heights = [s.StarSystem.height for s in systems]
    texts = [f"{s.PowerData.system_name}: {s.StarSystem.frequency} Visits" for s in systems]
    colors = [np.exp(s.StarSystem.frequency) for s in systems]  # Replace the original
    
    scatter = go.Scatter3d(
        x=lons,
        y=lats,
        z=heights,
        mode='markers',
        marker=dict(
            color=colors,
            colorscale='Viridis',
            showscale=True
        ),
        text=texts
    )

    fig = go.Figure(data=[scatter])
    
    return fig.to_html()
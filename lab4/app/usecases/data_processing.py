from app.entities.agent_data import AgentData
from app.entities.processed_agent_data import ProcessedAgentData

def process_agent_data(agent_data: AgentData) -> ProcessedAgentData:
    """
    Process agent data and classify the state of the road surface.

    Parameters:
    agent_data (AgentData): Agent data that contains accelerometer, GPS, and timestamp.

    Returns:
    processed_data (ProcessedAgentData): Processed data containing the classified state of the road.
    """

    z = agent_data.accelerometer.z

    # Класифікація стану дороги на основі координати z акселерометра
    if -0.2 <= z <= 0.2:
        road_state = "smooth"
    elif 0.2 < abs(z) <= 0.8:
        road_state = "slightly_rough"
    else:
        road_state = "very_rough"

    return ProcessedAgentData(
        road_state=road_state,
        agent_data=agent_data
    )
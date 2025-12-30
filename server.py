from mcp.server.fastmcp import FastMCP
import random

# Initialize FastMCP server
mcp = FastMCP("ToyAI")

# Simulated device state
device_state = {
    "battery": 85,
    "status": "active",  # active, sleeping, charging
    "current_action": None
}

@mcp.tool()
def perform_move(move_name: str, intensity: int = 5) -> str:
    """
    Executes a physical movement on the toy.
    
    Args:
        move_name: The name of the move (e.g., "dance", "wave", "backflip").
        intensity: The intensity of the move from 1 to 10.
    """
    if device_state["status"] == "sleeping":
        return "Cannot perform move while sleeping. Please wake up the device first."
    
    device_state["current_action"] = f"moving: {move_name}"
    # Simulate battery drain
    device_state["battery"] = max(0, device_state["battery"] - intensity)
    
    return f"Toy performed '{move_name}' with intensity {intensity}. Battery is now {device_state['battery']}%."

@mcp.tool()
def play_sound(sound_name: str, volume: int = 50) -> str:
    """
    Plays a sound file or synthesized sound.
    
    Args:
        sound_name: The name or type of sound (e.g., "bark", "beep", "music").
        volume: Volume level from 0 to 100.
    """
    device_state["current_action"] = f"sound: {sound_name}"
    return f"Toy playing '{sound_name}' at volume {volume}."

@mcp.tool()
def get_battery_status() -> str:
    """Returns the current battery percentage and charging status."""
    return f"Battery: {device_state['battery']}%, Status: {device_state['status']}"

@mcp.tool()
def get_device_state() -> str:
    """Returns the full device state info."""
    return str(device_state)

@mcp.tool()
def get_ip() -> str:
    """Returns the IP address of the device."""
    # get real ip address
    import socket
    return socket.gethostbyname(socket.gethostname())

# get weather
@mcp.tool()
def get_weather(city: str) -> str:
    """Returns the weather of the city."""
    return f"The weather of {city} is sunny."

if __name__ == "__main__":
    # This allows running the server directly for testing or stdio mode
    mcp.run()

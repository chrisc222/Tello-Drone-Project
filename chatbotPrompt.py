from djitellopy import Tello
import ollama


# Initialize Tello drone
tello = Tello()
tello.connect()
print(f"Battery: {tello.get_battery()}%")
tello.enable_mission_pads()  # Optional: for mission pad detection


# Function to parse NLP input into Tello commands
def parse_command(text):
    response = ollama.chat(
        model='llama3.1:8b',
        messages=[
            {
                'role': 'system',
                'content': '''You are a drone control assistant. Convert natural language commands into specific DJI Tello drone commands.
                Examples:
                - "Take off" -> "takeoff"
                - "Fly forward" -> "forward 50"
                - "Land now" -> "land"
                - "Turn left" -> "ccw 90"
                - "Flip forward" -> "flip f"
                Respond with only the command string or "unknown" if the command is unclear.'''
            },
            {'role': 'user', 'content': text}
        ]
    )
    return response['message']['content'].strip()


# Main loop for user input
def main():
    tello.streamoff()  # Disable stream if not needed
    while True:
        user_input = input("Enter a command (or 'exit' to quit): ")
        if user_input.lower() == 'exit':
            tello.land()
            break
        command = parse_command(user_input)
        print(f"Parsed command: {command}")
        try:
            if command == "takeoff":
                tello.takeoff()
            elif command == "land":
                tello.land()
            elif command.startswith("forward"):
                distance = int(command.split()[-1])
                tello.move_forward(distance)
            elif command.startswith("ccw"):
                angle = int(command.split()[-1])
                tello.rotate_counter_clockwise(angle)
            elif command.startswith("flip"):
                direction = command.split()[-1]
                tello.flip(direction)
            else:
                print("Command not recognized by script.")
        except Exception as e:
            print(f"Error executing command: {e}")


if __name__ == "__main__":
    main()
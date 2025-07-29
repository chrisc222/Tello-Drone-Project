from djitellopy import Tello
import cv2
import numpy as np
import time


# Connect to Tello
tello = Tello()
tello.connect()
print(f"Battery: {tello.get_battery()}%")


# Start camera stream
tello.streamon()
frame_reader = tello.get_frame_read()


print("Press 'q' to quit.")


while True:
    frame = frame_reader.frame
    frame = cv2.resize(frame, (640, 480))


    # OPTIONAL: Convert BGR to RGB if colors look flipped
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


    # Convert to HSV for color detection
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


    # Define red color range
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])


    # Create masks and combine
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = mask1 + mask2


    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 1000:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(frame, "Red Object", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)


    # Draw center point for debugging
    center_x, center_y = 320, 240
    b, g, r = frame[center_y, center_x]
    cv2.circle(frame, (center_x, center_y), 5, (0, 255, 255), -1)
    cv2.putText(frame, f"BGR: ({b},{g},{r})", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)


    # Show the frame
    cv2.imshow("Tello Camera - Red Detection", frame)


    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


tello.streamoff()
cv2.destroyAllWindows()
tello.end()

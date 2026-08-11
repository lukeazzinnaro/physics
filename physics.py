import cv2
import time
import numpy as np

cap = cv2.VideoCapture(0)

previous_center = None
previous_time = None

while True:
    _, frame = cap.read()

    grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurFrame = cv2.GaussianBlur(grayFrame, (17, 17), 0)

    circles = cv2.HoughCircles(
        blurFrame,
        cv2.HOUGH_GRADIENT,
        1.2,
        100,
        param1=100,
        param2=30,
        minRadius=75,
        maxRadius=400
    )

    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")

        # Use the first detected circle
        x, y, radius = circles[0]

        # Draw circle
        cv2.circle(frame, (x, y), radius, (0, 255, 0), 2)

        # Draw center
        cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)

        current_center = (x, y)
        current_time = time.time()

        if previous_center is not None:
            # How far the circle moved
            dx = x - previous_center[0]
            dy = y - previous_center[1]

            distance = np.sqrt(dx**2 + dy**2)

            # How much time passed
            time_difference = current_time - previous_time

            # Speed in pixels per second
            speed = distance / time_difference

            cv2.putText(
                frame,
                f"Speed: {speed:.1f} pixels/sec",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

        previous_center = current_center
        previous_time = current_time

    cv2.imshow("Camera", frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

import tkinter as tk
import cv2
import numpy as np

root = tk.Tk()
root.title("promptpay")
root.geometry('800x1600')
photo = tk.PhotoImage(file="IMG_1501.png")

label = tk.Label(root, image=photo, width=1600, height=1600, bg="black", fg="yellow")
label.pack()

color_ranges = {
    'red': ((0, 100, 100), (10, 255, 255), 30),
    'green': ((35, 100, 100), (85, 255, 255), 45),
    'blue': ((105, 105, 105), (140, 255, 255), 60),

}


def detect_color(frame):
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    detected_colors = {color: 0 for color in color_ranges}

    for color, (lower_bound, upper_bound, _) in color_ranges.items():
        mask = cv2.inRange(hsv_frame, np.array(lower_bound), np.array(upper_bound))
        masked_frame = cv2.bitwise_and(frame, frame, mask=mask)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 500:
                detected_colors[color] += 1

    return detected_colors


def main():
    cap = cv2.VideoCapture(0)

    ret, frame = cap.read()
    if not ret:
        print("Failed to grab a frame")
        cap.release()
        return

    detected_colors = detect_color(frame)

    total_price = sum(count * color_ranges[color][2] for color, count in detected_colors.items())

    result_frame = frame.copy()
    y0, dy = 50, 30
    for idx, (color, count) in enumerate(detected_colors.items()):
        price = count * color_ranges[color][2]
        text = f"{color.capitalize()}: {count} dishes (${price})"
        cv2.putText(result_frame, text, (10, y0 + idx * dy), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)

    cv2.putText(result_frame, f"Total price: ${total_price}", (10, y0 + len(detected_colors) * dy + 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    cv2.imshow('Detected Colors', result_frame)

    cv2.waitKey(0)
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
root.mainloop()

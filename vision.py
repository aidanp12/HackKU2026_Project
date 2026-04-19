from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort
import cv2
import serial
import time

model = YOLO("yolov8n.pt")
tracker = DeepSort(max_age=30)

cap = cv2.VideoCapture(1)
# open raspberry pi port to send data over

pico = serial.Serial("COM4", 115200)
last_transmission = time.time()
buffer = 0.05

def range_conversion(x, y):
    global last_transmission
    current_time = time.time()
    if current_time - last_transmission > buffer:
        new_x = 60 + (x - 0)/(800 - 0) * (125 - 60)
        new_y = 70 + (y - 230)/(800 - 230) * (120 - 70)
        line_x = f"1 = {int(float(new_x))}\n"
        line_y = f"2 = {int(float(new_y))}\n"
        print(line_x)
        print(line_y)
        pico.write(line_x.encode())
        pico.write(line_y.encode())
        last_transmission = current_time


while True:
    # capture video frame
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)[0]

    detections = []

    for box in results.boxes:
        cls = int(box.cls[0])
        if cls == 0:  # person
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])
            detections.append(([x1, y1, x2, y2], conf, "person"))

    tracks = tracker.update_tracks(detections, frame=frame)

    confirmed = [t for t in tracks if t.is_confirmed()]
    target = min(confirmed, key=lambda t: t.track_id) if confirmed else None

    # draw rectangle on the frame
    for t in confirmed:
        track_id = t.track_id
        l, t_, r, b = map(int, t.to_ltrb())
        color = (0, 255, 0) if t is target else (100, 100, 100)
        cv2.rectangle(frame, (l, t_), (r, b), color, 2)
        cv2.putText(frame, f"ID {track_id}", (l, t_-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # prioritize the earliest confirmed target
    if target is not None:
        track_id = target.track_id
        l, t_, r, b = map(int, target.to_ltrb())
        cx = (l + r) // 2
        cy = (t_ + b) // 2
        print(f"ID {track_id} center: ({cx}, {cy})")
        range_conversion(abs(800-cx), abs(800-cy)) # send the data to the pico

    cv2.imshow("DeepSORT Tracking", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
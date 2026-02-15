import cv2
from detector import detect_vehicles
from tracker import CentroidTracker
from anomaly import detect_anomalies
from utils import log_anomaly

video_path = "dataset/anomaly/video1.mp4"

cap = cv2.VideoCapture(video_path)
fps = cap.get(cv2.CAP_PROP_FPS)

tracker = CentroidTracker()

fourcc = cv2.VideoWriter_fourcc(*"XVID")
out = cv2.VideoWriter("output.avi", fourcc, fps,
                      (int(cap.get(3)), int(cap.get(4))))

while True:
    ret, frame = cap.read()
    if not ret:
        break

    detections = detect_vehicles(frame)
    objects = tracker.update(detections)

    anomalies, speeds = detect_anomalies(objects, detections, fps)

    # Convert anomaly list into dictionary
    anomaly_dict = {}
    for obj_id, label in anomalies:
        anomaly_dict[obj_id] = label

    # Draw bounding boxes
    for obj_id, centroid in objects.items():
        cx, cy = centroid

        # Find matching bounding box
        matched_box = None
        for box in detections:
            x1, y1, x2, y2 = box
            box_cx = int((x1 + x2) / 2)
            box_cy = int((y1 + y2) / 2)

            if abs(box_cx - cx) < 20 and abs(box_cy - cy) < 20:
                matched_box = box
                break

        if matched_box:
            x1, y1, x2, y2 = matched_box

            # Default color → Green
            box_color = (0, 255, 0)
            label_text = f"ID {obj_id}"

            # If anomaly → Red
            if obj_id in anomaly_dict:
                box_color = (0, 0, 255)
                label_text += f" | {anomaly_dict[obj_id]}"
                log_anomaly(obj_id, anomaly_dict[obj_id],
                            speeds.get(obj_id, 0))

            # Draw box
            cv2.rectangle(frame, (x1, y1), (x2, y2),
                          box_color, 2)

            # Show speed
            if obj_id in speeds:
                label_text += f" | {int(speeds[obj_id])} km/h"

            cv2.putText(frame, label_text,
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, box_color, 2)

    # Traffic Count
    vehicle_count = len(objects)
    cv2.putText(frame,
                f"Traffic Count: {vehicle_count}",
                (20, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8, (255, 255, 0), 2)

    cv2.imshow("Advanced Traffic Anomaly System", frame)
    out.write(frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
out.release()
cv2.destroyAllWindows()
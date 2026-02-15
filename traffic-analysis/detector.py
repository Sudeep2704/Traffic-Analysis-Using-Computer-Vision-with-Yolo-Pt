from ultralytics import YOLO

model = YOLO("yolov8n.pt")

def detect_vehicles(frame):
    results = model(frame)
    detections = []

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])

            # COCO vehicle classes
            if cls in [2, 3, 5, 7] and conf > 0.4:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                detections.append((x1, y1, x2, y2))

    return detections
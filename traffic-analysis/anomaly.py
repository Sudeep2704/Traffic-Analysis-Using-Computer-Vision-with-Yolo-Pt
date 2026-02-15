import math

previous_positions = {}
previous_speeds = {}

SPEED_LIMIT_KMH = 60
PIXEL_TO_METER = 0.05  # adjust using calibration

def calculate_speed(prev, current, fps):
    distance_pixels = math.sqrt((current[0]-prev[0])**2 +
                                (current[1]-prev[1])**2)

    pixel_speed = distance_pixels * fps
    meter_speed = pixel_speed * PIXEL_TO_METER
    kmh = meter_speed * 3.6
    return kmh

def check_overlap(box1, box2):
    x1, y1, x2, y2 = box1
    x3, y3, x4, y4 = box2

    if (x1 < x4 and x2 > x3 and
        y1 < y4 and y2 > y3):
        return True
    return False

def detect_anomalies(objects, detections, fps):
    anomalies = []
    speeds = {}

    for obj_id, centroid in objects.items():

        if obj_id in previous_positions:
            prev = previous_positions[obj_id]
            speed_kmh = calculate_speed(prev, centroid, fps)
            speeds[obj_id] = speed_kmh

            # Overspeed
            if speed_kmh > SPEED_LIMIT_KMH:
                anomalies.append((obj_id, "Overspeed"))

            # Wrong Way (Assume downward flow)
            if centroid[1] < prev[1]:
                anomalies.append((obj_id, "Wrong Way"))

            # Sudden Stop → Accident suspicion
            if obj_id in previous_speeds:
                if previous_speeds[obj_id] > 40 and speed_kmh < 5:
                    anomalies.append((obj_id, "Sudden Stop"))

            previous_speeds[obj_id] = speed_kmh

        previous_positions[obj_id] = centroid

    # Check collision overlap
    for i in range(len(detections)):
        for j in range(i+1, len(detections)):
            if check_overlap(detections[i], detections[j]):
                anomalies.append(("Multiple", "Possible Collision"))

    return anomalies, speeds
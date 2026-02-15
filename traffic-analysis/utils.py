import csv

def log_anomaly(object_id, anomaly_type, speed):

    with open("anomaly_log.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([object_id, anomaly_type, speed])
import cv2
import subprocess
from ultralytics import YOLO

#DISCLAIMER: Not my code, but rather based on https://github.com/MrShivam-Pal/Content-Aware-Video-Cropping

def load_yolov8_model(model_path):
    """Load the YOLOv8 model."""
    model = YOLO(model_path)
    return model

def detect_objects_yolov8(frame, model, confidence_threshold=0.5):
    """Detect objects with confidence threshold."""
    results = model(frame, stream=False)
    detections = []

    for box in results[0].boxes:
        if box.conf[0] < confidence_threshold:
            continue
            
        x_min, y_min, x_max, y_max = map(int, box.xyxy[0].tolist())
        confidence = float(box.conf[0])
        class_id = int(box.cls[0])
        detections.append({
            'x_min': x_min, 'y_min': y_min,
            'x_max': x_max, 'y_max': y_max,
            'confidence': confidence, 'class_id': class_id
        })

    return detections

def prioritize_objects(detections, frame_width, frame_height, prev_object=None):
    """Prioritize objects with tracking awareness."""
    if not detections:
        return None
        
    frame_center = (frame_width / 2, frame_height / 2)

    def calculate_score(roi, prev_obj):
        x_center = (roi['x_min'] + roi['x_max']) / 2
        y_center = (roi['y_min'] + roi['y_max']) / 2
        width = roi['x_max'] - roi['x_min']
        height = roi['y_max'] - roi['y_min']
        area = width * height
        
        score = roi['confidence'] + 0.5 * area - 0.2 * ((x_center - frame_center[0])**2 + (y_center - frame_center[1])**2)**0.5
        
        if prev_obj:
            prev_x = (prev_obj['x_min'] + prev_obj['x_max']) / 2
            prev_y = (prev_obj['y_min'] + prev_obj['y_max']) / 2
            distance = ((x_center - prev_x)**2 + (y_center - prev_y)**2)**0.5
            score += 0.5 * (1 - min(distance / max(frame_width, frame_height), 1))
            
        return score

    scored_detections = [(d, calculate_score(d, prev_object)) for d in detections]
    best_detection = max(scored_detections, key=lambda x: x[1], default=None)
    
    return best_detection[0] if best_detection else None

def adjust_to_aspect_ratio(x_center, y_center, target_aspect_ratio, frame_width, frame_height):
    """Adjusts cropping region to match aspect ratio."""
    if frame_height * target_aspect_ratio <= frame_width:
        crop_height = frame_height
        crop_width = int(crop_height * target_aspect_ratio)
    else:
        crop_width = frame_width
        crop_height = int(crop_width / target_aspect_ratio)

    x1 = max(0, int(x_center - crop_width / 2))
    x2 = min(frame_width, int(x_center + crop_width / 2))
    y1 = max(0, int(y_center - crop_height / 2))
    y2 = min(frame_height, int(y_center + crop_height / 2))

    return x1, y1, x2, y2

def process_video(input_path, output_path, model, target_aspect_ratio=9/16, 
                 smoothing_factor=0.95, min_confidence=0.6):
    """Main video processing function with stabilization."""
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        raise ValueError("Unable to open video file")

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output_width = int(frame_height * target_aspect_ratio)
    output_height = frame_height

    out = cv2.VideoWriter(output_path, fourcc, fps, (output_width, output_height))

    prev_crop = None
    prev_object = None
    no_detection_frames = 0
    MAX_NO_DETECTION_FRAMES = 10

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        detections = detect_objects_yolov8(frame, model, min_confidence)
        main_object = prioritize_objects(detections, frame_width, frame_height, prev_object)

        if main_object:
            prev_object = main_object
            no_detection_frames = 0
            x_center = (main_object['x_min'] + main_object['x_max']) / 2
            y_center = (main_object['y_min'] + main_object['y_max']) / 2
        elif no_detection_frames < MAX_NO_DETECTION_FRAMES and prev_object:
            no_detection_frames += 1
            x_center = (prev_object['x_min'] + prev_object['x_max']) / 2
            y_center = (prev_object['y_min'] + prev_object['y_max']) / 2
        else:
            x_center, y_center = frame_width // 2, frame_height // 2

        x1, y1, x2, y2 = adjust_to_aspect_ratio(x_center, y_center, 
                                               target_aspect_ratio, 
                                               frame_width, frame_height)

        if prev_crop is not None:
            prev_x1, prev_y1, prev_x2, prev_y2 = prev_crop
            smooth_x1 = int(smoothing_factor * prev_x1 + (1 - smoothing_factor) * x1)
            smooth_y1 = int(smoothing_factor * prev_y1 + (1 - smoothing_factor) * y1)
            smooth_x2 = int(smoothing_factor * prev_x2 + (1 - smoothing_factor) * x2)
            smooth_y2 = int(smoothing_factor * prev_y2 + (1 - smoothing_factor) * y2)
            
            x1 = max(0, min(smooth_x1, frame_width - (x2 - x1)))
            y1 = max(0, min(smooth_y1, frame_height - (y2 - y1)))
            x2 = x1 + (prev_x2 - prev_x1)
            y2 = y1 + (prev_y2 - prev_y1)

        prev_crop = (x1, y1, x2, y2)

        cropped_frame = frame[y1:y2, x1:x2]
        cropped_frame = cv2.resize(cropped_frame, (output_width, output_height))
        out.write(cropped_frame)

    cap.release()
    out.release()
    cv2.destroyAllWindows()

def add_audio_to_video(input_video_path, processed_video_path, output_with_audio_path):
    """Add audio from original video to processed video."""
    command = [
        "ffmpeg", "-i", processed_video_path, "-i", input_video_path, "-c:v", "copy",
        "-map", "0:v:0", "-map", "1:a:0", "-y", output_with_audio_path
    ]
    subprocess.run(command, check=True)
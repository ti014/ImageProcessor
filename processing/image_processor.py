import os
import cv2
import mediapipe as mp
import uuid  # Importing UUID module for generating random file names
import numpy as np  # Importing numpy for adding noise

class ImageProcessor:
    def __init__(self):
        self.mp_face_detection = mp.solutions.face_detection
        self.face_detection = self.mp_face_detection.FaceDetection(min_detection_confidence=0.5)

    def detect_face(self, image):
        results = self.face_detection.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        if results.detections:
            for detection in results.detections:
                bboxC = detection.location_data.relative_bounding_box
                ih, iw = image.shape[:2]
                x = int(bboxC.xmin * iw)
                y = int(bboxC.ymin * ih)
                w = int(bboxC.width * iw)
                h = int(bboxC.height * ih)
                return x + w // 2, y + h // 2
        return None

    def crop_image(self, image, center_x, center_y, target_width, target_height):
        # Calculate the coordinates for cropping
        start_x = max(0, center_x - target_width // 2)
        end_x = min(image.shape[1], center_x + target_width // 2)
        start_y = max(0, center_y - target_height // 2)
        end_y = min(image.shape[0], center_y + target_height // 2)

        # Debugging information
        # print(f"Image dimensions: {image.shape}")
        # print(f"Cropping coordinates - start_x: {start_x}, end_x: {end_x}, start_y: {start_y}, end_y: {end_y}")

        # Crop the image
        cropped_image = image[start_y:end_y, start_x:end_x]
        return cropped_image

    def process_image(self, image_path, output_folder, target_width, target_height, action, rename_files, detect_face, flip_image, flip_axis, rotate_image, rotate_angle, add_noise, noise_level):
        image = cv2.imread(image_path)
        if image is None:
            return f"Cannot read image from path: {image_path}"

        if flip_image:
            image = cv2.flip(image, flip_axis)  # Flip based on user input

        if rotate_image:
            (h, w) = image.shape[:2]
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, rotate_angle, 1.0)
            image = cv2.warpAffine(image, M, (w, h))

        if add_noise:
            noise = np.random.normal(0, noise_level, image.shape).astype(np.uint8)
            image = cv2.add(image, noise)

        if action == "crop":
            if detect_face:
                # Step 1: Detect face and crop around it
                center = self.detect_face(image)
                if not center:
                    center = (image.shape[1] // 2, image.shape[0] // 2)  # Default to image center if no face is detected
            else:
                center = (image.shape[1] // 2, image.shape[0] // 2)  # Default to image center

            center_x, center_y = center
            cropped_image = self.crop_image(image, center_x, center_y, target_width, target_height)

            if cropped_image is None or cropped_image.size == 0:
                return f"Could not crop image: {os.path.basename(image_path)}."

            final_image = cropped_image
        else:  # Resize action
            final_image = cv2.resize(image, (target_width, target_height), interpolation=cv2.INTER_CUBIC)

        # Step 2: Save with random UUID filename
        if rename_files:
            output_file_name = f"{uuid.uuid4()}.jpg"
        else:
            output_file_name = os.path.basename(image_path)

        output_file_path = os.path.join(output_folder, output_file_name)
        os.makedirs(output_folder, exist_ok=True)
        cv2.imwrite(output_file_path, final_image)
        return f"Processed: {output_file_name}"
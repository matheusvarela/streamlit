import cv2
import mediapipe as mp

# Inicializar Mediapipe
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5)

# Captura de vídeo
cap = cv2.VideoCapture(0)  # 0 para webcam

while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    # Converter a imagem para RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_detection.process(image_rgb)

    # Desenhar as caixas delimitadoras ao redor das faces detectadas
    if results.detections:
        for detection in results.detections:
            bboxC = detection.location_data.relative_bounding_box
            h, w, _ = image.shape
            cv2.rectangle(image, 
                          (int(bboxC.xmin * w), int(bboxC.ymin * h)), 
                          (int((bboxC.xmin + bboxC.width) * w), int((bboxC.ymin + bboxC.height) * h)), 
                          (255, 0, 0), 2)

    cv2.imshow('Detecção de Faces', image)
    if cv2.waitKey(5) & 0xFF == 27:  # Pressione 'Esc' para sair
        break

cap.release()
cv2.destroyAllWindows()

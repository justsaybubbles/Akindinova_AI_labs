import random
import cv2
import numpy as np
import pytesseract

#pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'

def correct_perspective(image):
    """
    Исправление перспективы изображения (выпрямление изогнутых краев).
    """
    # Перевод в градации серого
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Повышение контрастности
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)

    # Удаление шумов и границы
    blurred = cv2.GaussianBlur(enhanced, (5, 5), 0)
    edged = cv2.Canny(blurred, 50, 200)  # Нахождение границ с Canny

    # Найти контуры страницы
    contours, _ = cv2.findContours(edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]  # Топ-5 контуров

    screen_cnt = None
    for contour in contours:
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * peri, True)

        if len(approx) == 4:  # Проверяем, что контур четырёхугольный
            screen_cnt = approx
            break

    # Если контуры страницы не найдены, используем весь кадр
    if screen_cnt is None:
        height, width = image.shape[:2]
        screen_cnt = np.array([[0, 0], [width, 0], [width, height], [0, height]])

    # Упорядочивание точек и трансформация перспективы
    rect = order_points(screen_cnt.reshape(4, 2))
    (tl, tr, br, bl) = rect

    width_a = np.linalg.norm(br - bl)
    width_b = np.linalg.norm(tr - tl)
    max_width = max(int(width_a), int(width_b))

    height_a = np.linalg.norm(tr - br)
    height_b = np.linalg.norm(tl - bl)
    max_height = max(int(height_a), int(height_b))

    dst = np.array([
        [0, 0],
        [max_width - 1, 0],
        [max_width - 1, max_height - 1],
        [0, max_height - 1]
    ], dtype="float32")

    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (max_width, max_height))

    #cv2.imwrite("perspective_corrected.png", warped)
    return warped

def order_points(pts):
    """
    Упорядочивает точки в порядке: верх-лево, верх-право, низ-право, низ-лево.
    """
    rect = np.zeros((4, 2), dtype="float32")

    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]  # Верх-лево
    rect[2] = pts[np.argmax(s)]  # Низ-право

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]  # Верх-право
    rect[3] = pts[np.argmax(diff)]  # Низ-лево

    return rect

def enhance_image(image):
    """
    Улучшение изображения (контрастность и бинаризация).
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    return cv2.adaptiveThreshold(enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                 cv2.THRESH_BINARY, 15, 10)

def extract_text(image):
    """
    Извлекает текст из изображения.
    """
    # Шаг 1: Исправляем перспективу
    corrected_image = correct_perspective(image)

    # Шаг 2: Улучшаем изображение
    processed_image = enhance_image(corrected_image)
    #cv2.imwrite("good2.png", corrected_image)

    # Шаг 3: Используем Tesseract для распознавания текста
    result_text = pytesseract.image_to_string(processed_image, lang='eng')
    print(result_text)
    return result_text
    

async def generate_summary_and_score(text: str) -> str:
    summary = f"Summary: {text[:50]}..."  # Упрощённое содержание
    score = random.randint(7, 10)
    encouragement = "Great work! Keep improving your writing skills!"
    return f"{summary}\nScore: {score}/10\n{encouragement}"

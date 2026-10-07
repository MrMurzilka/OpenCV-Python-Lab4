"""
Скрипт для захвата и обработки видеопотока (Вариант 2).
"""

import cv2
import time
from datetime import datetime

def capture_video_with_timecode(duration: int = 10, output_file: str = 'output.avi') -> None:
    """Захватывает видео с камеры, переводит в ЧБ, накладывает таймкод и сохраняет."""
    # Инициализация захвата с основной камеры (индекс 0)
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Ошибка: Не удалось открыть камеру. Проверьте подключение.")
        return

    # Настройка параметров записи
    fourcc = cv2.VideoWriter.fourcc(*'XVID')
    fps = 20.0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Флаг isColor=False необходим для корректной записи одноканального (черно-белого) видео
    out = cv2.VideoWriter(output_file, fourcc, fps, (width, height), isColor=False)

    print(f"Начало записи на {duration} секунд. Нажмите 'q' для досрочной остановки.")
    start_time = time.time()

    # Чтение кадров в цикле
    while (time.time() - start_time) < duration:
        ret, frame = cap.read()
        if not ret:
            print("Ошибка: Не удалось считать кадр потока.")
            break

        # Преобразование BGR → Grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Формирование и наложение таймкода
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        cv2.putText(
            gray_frame, 
            current_time, 
            (10, 30), 
            cv2.FONT_HERSHEY_SIMPLEX, 
            0.7, 
            (255, 255, 255), 
            2, 
            cv2.LINE_AA
        )

        # Отображение и запись обработанного кадра
        cv2.imshow('Camera (Grayscale + Timecode)', gray_frame)
        out.write(gray_frame)

        # Выход по нажатию клавиши 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Выход по запросу пользователя.")
            break

    # Освобождение ресурсов
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print(f"Запись успешно завершена. Файл сохранен как: {output_file}")

if __name__ == '__main__':
    # Фиксация изменений: git commit -am "Реализован захват видео с камеры в ЧБ с таймкодом"
    capture_video_with_timecode(duration=15)
#include <opencv2/opencv.hpp>
#include <iostream>
#include <filesystem>

namespace fs = std::__fs::filesystem;


// моменты изображения
cv::Point2f findCentroidUsingMoments(const cv::Mat& binaryImage) {
    cv::Moments m = cv::moments(binaryImage, true);
    if (m.m00 != 0) {
        return cv::Point2f(m.m10 / m.m00, m.m01 / m.m00);
    }
    return cv::Point2f(-1, -1); // если объект не найден
}

void drawCentroid(cv::Mat& image, const cv::Point2f& center) {
    // Проверка, что центр масс найден (например, проверка на отрицательные координаты)
    if (center.x >= 0 && center.y >= 0) {
        // Нарисовать круг в центре масс
        cv::circle(image, center, 5, cv::Scalar(0, 0, 255), -1); // Красный круг
        // Добавить текст с координатами
        std::string text = "(" + std::to_string(static_cast<int>(center.x)) + ", " + std::to_string(static_cast<int>(center.y)) + ")";
        cv::putText(image, text, cv::Point(center.x + 10, center.y), cv::FONT_HERSHEY_SIMPLEX, 0.5, cv::Scalar(255, 0, 0), 1);
    }
}

int main() {
    // Папка с входными изображениями
    std::string inputFolder = "./input";
    // Папка для выходных изображений
    std::string outputFolder = "./results";

    // Проверить и создать папку results, если она не существует
    if (!fs::exists(outputFolder)) {
        fs::create_directory(outputFolder);
        std::cout << "Создана папка: " << outputFolder << std::endl;
    }

    // Перебор всех изображений в папке input
    for (const auto& entry : fs::directory_iterator(inputFolder)) {
        std::string inputFilePath = entry.path().string();
        std::string outputFilePath = outputFolder + "/" + entry.path().filename().string();

        // Загрузка изображения
        cv::Mat image = cv::imread(inputFilePath, cv::IMREAD_GRAYSCALE);
        if (image.empty()) {
            std::cout << "Ошибка: не удалось загрузить изображение " << inputFilePath << std::endl;
            continue;
        }

        // Преобразование в бинарное изображение
        cv::threshold(image, image, 128, 255, cv::THRESH_BINARY);

        cv::Point2f center = findCentroidUsingMoments(image);
        //std::cout << "Центр масс (метод моментов): " << center << std::endl;

        drawCentroid(image, center);
        cv::imwrite(outputFilePath, image);

    }

    return 0;
}

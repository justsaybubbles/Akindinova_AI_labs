#include <opencv2/opencv.hpp>
#include <iostream>
#include <filesystem>

namespace fs = std::__fs::filesystem;


// весовое усреднение 
cv::Point2f findCentroidByWeightedAverage(const cv::Mat& binaryImage) {
    double sumX = 0, sumY = 0, totalWeight = 0;

    for (int y = 0; y < binaryImage.rows; y++) {
        for (int x = 0; x < binaryImage.cols; x++) {
            if (binaryImage.at<uchar>(y, x) > 0) { // если пиксель белый (предполагаем бинарное изображение)
                sumX += x;
                sumY += y;
                totalWeight += 1;
            }
        }
    }

    if (totalWeight != 0) {
        return cv::Point2f(sumX / totalWeight, sumY / totalWeight);
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

        cv::Mat image = cv::imread(inputFilePath, cv::IMREAD_GRAYSCALE);
        if (image.empty()) {
            std::cout << "Ошибка: не удалось загрузить изображение!" << std::endl;
            return -1;
        }

        // Преобразование в бинарное изображение
        cv::threshold(image, image, 128, 255, cv::THRESH_BINARY);

        cv::Point2f center = findCentroidByWeightedAverage(image);
        //std::cout << "Центр масс (метод усреднения): " << center << std::endl;

        drawCentroid(image, center);
        cv::imwrite(outputFilePath, image);
        //std::cout << "Обработано и сохранено: " << outputFilePath << std::endl;
    }

    return 0;
}

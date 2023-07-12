#include <opencv2/opencv.hpp>
#include <iostream>

int main() {
    // Carica l'immagine
    cv::Mat img = cv::imread("C:\\Users\\Administrator\\Pictures\\lab_ia\\progetto_lampioni\\data\\immagine_lab_ia (1).jpg");
    if (img.empty()) {
        std::cout << "Immagine non caricata" << std::endl;
        return -1;
    }

    // Ottieni le dimensioni dell'immagine
    int imgWidth = img.cols;
    int imgHeight = img.rows;

    // Imposta le dimensioni desiderate per la visualizzazione
    int displayWidth = 800;
    int displayHeight = 600;

    // Calcola i fattori di ridimensionamento per adattare l'immagine alla finestra di visualizzazione
    double widthRatio = static_cast<double>(displayWidth) / imgWidth;
    double heightRatio = static_cast<double>(displayHeight) / imgHeight;
    double scaleFactor = std::min(widthRatio, heightRatio);

    // Ridimensiona l'immagine mantenendo l'aspetto ratio
    cv::resize(img, img, cv::Size(), scaleFactor, scaleFactor);

    // Converti l'immagine in scala di grigi
    cv::Mat imgGray;
    cv::cvtColor(img, imgGray, cv::COLOR_BGR2GRAY);

    // Crea un'istanza dell'oggetto SIFT
    cv::Ptr<cv::SIFT> sift = cv::SIFT::create();

    // Trova i punti chiave e i descrittori dell'immagine
    std::vector<cv::KeyPoint> keypoints;
    cv::Mat descriptors;
    sift->detectAndCompute(imgGray, cv::noArray(), keypoints, descriptors);

    // Disegna i punti chiave sull'immagine originale
    cv::Mat imgKeypoints;
    cv::drawKeypoints(img, keypoints, imgKeypoints);

    // Visualizza l'immagine con i punti chiave evidenziati
    cv::imshow("Individuazione Luci", imgKeypoints);
    cv::waitKey(0);

    // trova i lampioni
    std::vector<cv::KeyPoint> lampioni;
    for (int i = 0; i < keypoints.size(); i++) {
        cv::KeyPoint kp = keypoints[i];
        if (kp.size > 10) {
            lampioni.push_back(kp);
        }
    }

    // // trova i lampioni
    // std::vector<cv::KeyPoint> lampioni;
    // float sogliaDimensione = 10.0f; // soglia per la dimensione dei punti chiave
    // for (const cv::KeyPoint& kp : keypoints) {
    //     if (kp.size > sogliaDimensione) {
    //         lampioni.push_back(kp);
    //     }
    // }

    // Disegna i lampioni sull'immagine originale
    cv::Mat imgLampioni;
    cv::drawKeypoints(img, lampioni, imgLampioni);

    // Visualizza l'immagine con i lampioni evidenziati
    cv::imshow("Individuazione Lampioni", imgLampioni);
    cv::waitKey(0);


}

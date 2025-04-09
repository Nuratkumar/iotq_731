#include <iostream>
#include <vector>
#include <numeric>
#include <curl/curl.h>

double read_sensor() {
    return 25.0 + (rand() % 1000) / 100.0; // Simulated temp between 25 and 35°C
}

double calculate_average(const std::vector<double>& data) {
    return std::accumulate(data.begin(), data.end(), 0.0) / data.size();
}

bool send_data_secure(double value) {
    CURL* curl = curl_easy_init();
    if (!curl) return false;

    std::string postFields = "sensor=temperature&value=" + std::to_string(value);

    curl_easy_setopt(curl, CURLOPT_URL, "https://your-secure-server.com/api/data");
    curl_easy_setopt(curl, CURLOPT_POSTFIELDS, postFields.c_str());
    curl_easy_setopt(curl, CURLOPT_SSL_VERIFYPEER, 1L); // Validate SSL cert
    curl_easy_setopt(curl, CURLOPT_CAINFO, "/path/to/ca-bundle.crt"); // Your CA cert file

    CURLcode res = curl_easy_perform(curl);
    curl_easy_cleanup(curl);

    return res == CURLE_OK;
}

int main() {
    std::vector<double> buffer;
    const int sampleSize = 10;

    while (true) {
        double value = read_sensor();
        buffer.push_back(value);

        if (buffer.size() >= sampleSize) {
            double avg = calculate_average(buffer);
            std::cout << "Sending avg temperature: " << avg << "°C" << std::endl;

            if (!send_data_secure(avg)) {
                std::cerr << "Failed to send data!" << std::endl;
            }

            buffer.clear(); // reset for next window
        }

        std::this_thread::sleep_for(std::chrono::seconds(1));
    }

    return 0;
}
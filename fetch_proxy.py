import requests
import time

# Konfigurasi
SOURCE_URL = "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt"
OUTPUT_FILE = "local_proxies.txt"
TEST_URL = "https://httpbin.org/ip"
TARGET_COUNT = 200

def fetch_proxy_list():
    """Mengambil daftar proxy dari URL sumber."""
    try:
        response = requests.get(SOURCE_URL, timeout=10)
        response.raise_for_status()
        return response.text.splitlines()
    except requests.RequestException as e:
        print(f"Error fetching proxy list: {e}")
        return []

def test_proxy(proxy):
    """Menguji apakah proxy berfungsi."""
    formatted_proxy = f"http://{proxy}"
    proxies = {"http": formatted_proxy, "https": formatted_proxy}
    try:
        response = requests.get(TEST_URL, proxies=proxies, timeout=5)
        if response.status_code == 200:
            print(f"Proxy OK: {formatted_proxy}")
            return formatted_proxy
        else:
            print(f"Proxy Failed (HTTP Error): {formatted_proxy}")
            return None
    except Exception as e:
        print(f"Proxy Failed: {formatted_proxy} | Error: {e}")
        return None

def save_to_file(proxies, filename):
    """Menyimpan daftar proxy ke file."""
    with open(filename, "w") as file:
        file.write("\n".join(proxies))
    print(f"Saved {len(proxies)} proxies to {filename}")

def main():
    valid_proxies = []
    while len(valid_proxies) < TARGET_COUNT:
        print(f"Fetching proxy list... (Current valid: {len(valid_proxies)}/{TARGET_COUNT})")
        proxy_list = fetch_proxy_list()
        if not proxy_list:
            print("Failed to fetch proxy list. Retrying in 10 seconds...")
            time.sleep(10)
            continue

        for proxy in proxy_list:
            if len(valid_proxies) >= TARGET_COUNT:
                break
            result = test_proxy(proxy)
            if result:
                valid_proxies.append(result)

        # Jika belum cukup, tunggu sebelum mencoba lagi
        if len(valid_proxies) < TARGET_COUNT:
            print("Not enough valid proxies. Retrying in 10 seconds...")
            time.sleep(10)

    save_to_file(valid_proxies, OUTPUT_FILE)
    print("Proxy fetching and validation completed!")

if __name__ == "__main__":
    main()

import speedtest

def measure_speed():
    st = speedtest.Speedtest()

    # Get the best server automatically
    st.get_best_server()
    
    # Get the server details
    server_url = st.results.server['url']
    print(f"Testing against server: {server_url}")

    # Measure download speed
    download_speed = st.download() / 1024 / 1024  # Convert to megabits per second
    print(f"Download Speed: {download_speed:.2f} Mbps")

    # Measure upload speed
    upload_speed = st.upload() / 1024 / 1024  # Convert to megabits per second
    print(f"Upload Speed: {upload_speed:.2f} Mbps")

if __name__ == "__main__":
    measure_speed()


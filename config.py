def near_position(your_lat, your_lng, iss_lat, iss_lng):
    if your_lat - 5 < iss_lat < your_lat + 5 and your_lng - 5 < iss_lng < your_lng + 5:
        return True

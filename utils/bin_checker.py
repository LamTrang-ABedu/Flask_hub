import requests

def check_bin_list(file_path="utils/sample_bins.txt"):
    results = []
    with open(file_path) as f:
        for line in f:
            bin = line.strip()
            if not bin or not bin.isdigit(): continue
            r = requests.get(f"https://lookup.binlist.net/{bin}")
            if not r.ok: continue
            data = r.json()
            results.append({
                "bin": bin,
                "brand": data.get("scheme", "").upper(),
                "bank": data.get("bank", {}).get("name", ""),
                "type": data.get("type", "").upper(),
                "country": data.get("country", {}).get("alpha2", "")
            })
    return results

import urllib.request
import urllib.parse
import json

base_url = 'http://127.0.0.1:8000'

benchmarks = [
    ("satellite_telemetry_qpsk_leo.iq", "qpsk", 10),
    ("deep_space_downlink_bpsk.iq", "bpsk", 10),
    ("tactical_uav_16qam.iq", "16qam", 8),
]

print("=" * 60)
print("  VALIDATING PHYSICAL RF BENCHMARK INGESTION & PIPELINE")
print("=" * 60)

for filename, mod, sps in benchmarks:
    print(f"\n>>> INGESTING: {filename}")
    
    # 1. Load Sample
    data = urllib.parse.urlencode({'filename': filename}).encode('utf-8')
    req = urllib.request.Request(f'{base_url}/api/load-sample', data=data, method='POST')
    with urllib.request.urlopen(req) as resp:
        load_res = json.loads(resp.read().decode())
        print(f"  [OK] Ingested: {load_res['filename']} ({load_res['num_samples']} samples, Fs={load_res['sample_rate']} Hz)")

    # 2. Automated Spectral & Parameter Analysis
    with urllib.request.urlopen(f'{base_url}/api/analyze') as resp:
        ana = json.loads(resp.read().decode())
        print(f"  [OK] /api/analyze: Modulation={ana['estimation']['modulation']['modulation']}, "
              f"Baud={ana['estimation']['baud_rate']['symbol_rate']:.1f} Hz, "
              f"SNR={ana['estimation']['snr']['snr_db']:.2f} dB")

    # 3. Demodulation
    d_demod = urllib.parse.urlencode({'modulation': mod, 'samples_per_symbol': sps}).encode('utf-8')
    with urllib.request.urlopen(urllib.request.Request(f'{base_url}/api/demodulate', data=d_demod, method='POST')) as resp:
        demod = json.loads(resp.read().decode())
        print(f"  [OK] /api/demodulate: {demod['num_symbols']} symbols, {demod['num_bits']} bits, EVM={demod['evm_percent']:.2f}%")

print("\n" + "=" * 60)
print("  ALL PHYSICAL SAMPLES INGESTED & ANALYZED WITH 0 ERRORS!")
print("=" * 60)

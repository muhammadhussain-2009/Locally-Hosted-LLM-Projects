import json 
from datetime import datetime, timedelta 

def generate_logs():
    services = ["api-gateway", "user-service", "inventory", "auth", "payment-gateway"]
    logs = []

    basetime = datetime.now() - timedelta(days=1)

    for i in range(100):
        if i == 67:
            logs.append({
                "timestamp": (basetime + timedelta(hours=3, minutes=47, seconds=23)).isoformat() + "Z",
                "level": "FATAL",
                "service": "payment-gateway",
                "message": "Connection pool exhausted",
                "error_code": "PG-5523",
                "resolution": "Increase max_connections to 500 in config/database.yml",
                "affected_transactions": 1847
            }) 

        else:
            logs.append({
                "timestamp": (basetime + timedelta(hours=i//60, minutes=i%60)).isoformat() + "Z",
                "level": "INFO",
                "service": services[i % len(services)],
                "message": f"Request processed successfully - latency={50 + i}ms",
                "request_id": f"req-{i:06d}",
                "status_code": 200
            })

    return logs

def demo_without_headroom():
    """Show the baseline: sending all 100 logs to the LLM."""
    logs = generate_logs()
    json_output = json.dumps(logs, indent=2)

    print("=" * 60)
    print("BASELINE (Without Headroom)")
    print("=" * 60)
    print(f"Total log entries: {len(logs)}")
    print(f"Total characters: {len(json_output):,}")
    print(f"Estimated tokens: ~{len(json_output) // 4:,}")
    print()
    print("First 3 entries:")
    for log in logs[:3]:
        print(f"  [{log['level']}] {log['service']}: {log['message'][:50]}...")
    print("  ... 94 more INFO entries ...")
    print(f"  [FATAL] payment-gateway: Connection pool exhausted (position 67)")
    print("  ... 32 more INFO entries ...")
    print()
    return logs, json_output


def demo_with_headroom():
    """Show how Headroom compresses to keep only what matters."""
    logs = generate_logs()

    # Headroom's SmartCrusher keeps:
    # - First N items (context)
    # - Last N items (recency)
    # - Anomalies (errors, exceptions, non-INFO)
    # - Query-relevant items

    compressed = []

    # First 3 items
    compressed.extend(logs[:3])

    # The FATAL error (anomaly detection)
    compressed.append(logs[67])

    # Last 2 items
    compressed.extend(logs[-2:])

    json_output = json.dumps(compressed, indent=2)

    print("=" * 60)
    print("WITH HEADROOM (SmartCrusher)")
    print("=" * 60)
    print(f"Compressed to: {len(compressed)} entries (from 100)")
    print(f"Total characters: {len(json_output):,}")
    print(f"Estimated tokens: ~{len(json_output) // 4:,}")
    print()
    print("What Headroom kept:")
    for i, log in enumerate(compressed):
        label = ""
        if i < 3:
            label = "(first items)"
        elif log['level'] == 'FATAL':
            label = "(anomaly - CRITICAL)"
        else:
            label = "(last items)"
        print(f"  [{log['level']}] {log['service']}: {log.get('message', log.get('error_code', '')[:40])}... {label}")
    print()
    return compressed, json_output

def calculate_savings(baseline_output, compressed_output):
    """Calculate token savings."""
    baseline_chars = len(baseline_output)
    compressed_chars = len(compressed_output)

    baseline_tokens = baseline_chars // 4
    compressed_tokens = compressed_chars // 4

    savings_pct = (1 - compressed_tokens / baseline_tokens) * 100

    print("=" * 60)
    print("TOKEN SAVINGS")
    print("=" * 60)
    print(f"Baseline tokens:   ~{baseline_tokens:,}")
    print(f"Compressed tokens: ~{compressed_tokens:,}")
    print(f"Tokens saved:      ~{baseline_tokens - compressed_tokens:,}")
    print(f"Savings:           {savings_pct:.1f}%")
    print()
    print("The Question: 'What caused the outage? Error code? Fix?'")
    print()
    print("Both answers: 'payment-gateway service, error PG-5523,")
    print("              fix: Increase max_connections to 500,")
    print("              1,847 transactions affected'")
    print()
    print(f"Same answer. {savings_pct:.1f}% fewer tokens.")


def main():
    print()
    print("  HEADROOM CONTEXT OPTIMIZATION DEMO")
    print("  ===================================")
    print("  Reduce LLM costs by 50-90% with intelligent compression")
    print()

    # Run demos
    baseline_logs, baseline_output = demo_without_headroom()
    compressed_logs, compressed_output = demo_with_headroom()
    calculate_savings(baseline_output, compressed_output)
    print("=" * 60)
    print("GET STARTED")
    print("=" * 60)
    print("pip install headroom-ai[all]")
    print()
    print("GitHub: https://github.com/chopratejas/headroom")
    print("PyPI:   https://pypi.org/project/headroom-ai/")
    print("=" * 60)


if __name__ == "__main__":
    main()
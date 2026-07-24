import os

OUTPUT_DIR = "test_samples"
os.makedirs(OUTPUT_DIR, exist_ok=True)

samples = [
    {
        "filename": "meeting_sample_1.txt",
        "content": """Hannah: Hey guys, quick sync on the Q3 marketing launch. Did everyone review the draft?
Amanda: Yes! The copy looks solid, but we need to update the landing page hero image.
Hannah: Good call. Rob, can you swap that out with the new product renders by tomorrow?
Rob: On it. I'll have the updated assets pushed to S3 by 3 PM.
Amanda: Also, are we still running the LinkedIn ads starting Monday?
Hannah: Yes, budget is approved. Let's make sure tracking pixels are verified before launch."""
    },
    {
        "filename": "meeting_sample_2.txt",
        "content": """David: Thanks for joining, team. We need to address the latency spikes on the payment gateway API.
Elena: I checked the logs from yesterday's outage. The Redis cache reached max memory capacity around 2 PM.
Marcus: Should we upgrade the Redis instance node size or adjust TTL settings?
Elena: Increasing the node size to cache.m6g.large will give us headroom. I can apply the terraform changes during tonight's maintenance window.
David: Approved. Marcus, please double check that fallback error alerts trigger in Slack if connection pool drops.
Marcus: Will do. I'll test the webhooks in staging this afternoon."""
    },
    {
        "filename": "meeting_sample_3.txt",
        "content": """Sarah: Brief update on the mobile app release. QA completed all regression runs on iOS and Android.
Tom: Any blocking bugs remaining?
Sarah: Zero critical issues. Just a minor font alignment bug on the settings screen, which we postponed to the next patch.
Tom: Perfect. Let's proceed with the production release at 9:00 AM tomorrow.
Sarah: Sounds great. I'll notify the customer success team so they're ready for user inquiries."""
    }
]

print("Generating test meeting samples locally...")

for sample in samples:
    file_path = os.path.join(OUTPUT_DIR, sample["filename"])
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(sample["content"].strip())
    print(f" Saved: {file_path}")

print(f"\nDone! 3 test .txt files are now ready in the '{OUTPUT_DIR}' folder.")
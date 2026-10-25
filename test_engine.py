import forensic_engine

print("================ IMAGES ================")
for name in ['camera_captured_sample.jpg', 'ai_generated_sample.jpg', 'IMG-20260918-WA0034.jpg']:
    with open('samples/' + name, 'rb') as f:
        res = forensic_engine.analyze_image(f.read(), name)
        print(f"File: {name}")
        print(f" -> Verdict:  {res['verdict_text']}")
        print(f" -> Category: {res['category_label']}")
        print(f" -> Reasons:  {res['reasons']}")
        print()

print("================ VIDEOS ================")
for name in ['camera_captured_video.mp4', 'sora_ai_generated_video.mp4', 'VID-20260918-WA0012.mp4']:
    res = forensic_engine.analyze_video('samples/' + name, name)
    print(f"File: {name}")
    print(f" -> Verdict:  {res['verdict_text']}")
    print(f" -> Category: {res['category_label']}")
    print(f" -> Reasons:  {res['reasons']}")
    print()

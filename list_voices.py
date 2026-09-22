import asyncio, edge_tts

async def main():
    voices = await edge_tts.VoicesManager.create()
    male_voices = [v for v in voices.voices if v['Gender'] == 'Male' and ('en-US' in v['Locale'] or 'en-IN' in v['Locale'] or 'en-GB' in v['Locale'])]
    for v in male_voices[:10]:
        print(f"{v['ShortName']} | {v['FriendlyName']}")

asyncio.run(main())

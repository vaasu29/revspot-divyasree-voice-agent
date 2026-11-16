import os
import json
import asyncio
import edge_tts

# Destination directories
OUTPUT_DIR_RECORDINGS = "audio_recordings"
OUTPUT_DIR_STATIC = os.path.join("app", "static", "audio")

os.makedirs(OUTPUT_DIR_RECORDINGS, exist_ok=True)
os.makedirs(OUTPUT_DIR_STATIC, exist_ok=True)

TEMP_DIR = "temp_audio_chunks"
os.makedirs(TEMP_DIR, exist_ok=True)

async def synthesize_turn(text, voice, out_path):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(out_path)

async def generate_flow_audio(flow):
    flow_id = flow["id"]
    flow_title = flow["title"]
    print(f"\nProcessing {flow_title}...")
    
    turn_files = []
    for idx, turn in enumerate(flow["dialogue"]):
        speaker = turn["speaker"]
        voice = turn["voice"]
        text = turn["text"]
        
        turn_file = os.path.join(TEMP_DIR, f"{flow_id}_turn_{idx}_{speaker}.mp3")
        print(f"  [{idx+1}/{len(flow['dialogue'])}] Synthesizing {speaker} ({voice})...")
        await synthesize_turn(text, voice, turn_file)
        turn_files.append(turn_file)

    # Filename based on flow id
    filename_map = {
        "flow_1": "Flow_1_HNI_Investor_Happy_Path.mp3",
        "flow_2": "Flow_2_Luxury_Weekend_Home_Buyer.mp3",
        "flow_3": "Flow_3_Budget_Constraint_Handling.mp3",
        "flow_4": "Flow_4_Location_Objection_Handling.mp3",
        "flow_5": "Flow_5_Irritated_User_Multilingual_Hinglish.mp3"
    }
    target_filename = filename_map.get(flow_id, f"{flow_id}.mp3")
    
    target_rec_path = os.path.join(OUTPUT_DIR_RECORDINGS, target_filename)
    target_stat_path = os.path.join(OUTPUT_DIR_STATIC, target_filename)

    # Binary concatenation of mp3 frames
    with open(target_rec_path, "wb") as outfile:
        for t_file in turn_files:
            with open(t_file, "rb") as infile:
                outfile.write(infile.read())

    # Copy to static dir
    with open(target_stat_path, "wb") as outfile:
        with open(target_rec_path, "rb") as infile:
            outfile.write(infile.read())

    file_size_kb = os.path.getsize(target_rec_path) / 1024
    print(f"  -> Generated: {target_filename} ({file_size_kb:.1f} KB)")

    # Cleanup temp turns
    for t_file in turn_files:
        try:
            os.remove(t_file)
        except Exception:
            pass

async def main():
    with open("data/conversation_flows.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    for flow in data["flows"]:
        await generate_flow_audio(flow)

    try:
        os.rmdir(TEMP_DIR)
    except Exception:
        pass
        
    print("\nAll 5 conversation audio flows generated successfully!")

if __name__ == "__main__":
    asyncio.run(main())

import os
import zipfile

def package_submission():
    zip_filename = "Revspot_AI_Submission_Packet.zip"
    print(f"Creating {zip_filename}...")
    
    files_to_include = [
        "Divyasree_WOW_Voice_Agent_System_Prompt.pdf",
        "Divyasree_WOW_Voice_Agent_System_Prompt.md",
        "README.md",
        "SUBMISSION_GUIDE.md",
        "requirements.txt",
        "render.yaml",
        "Dockerfile",
        "run_app.py",
        "build_pdf.py"
    ]
    
    folders_to_include = [
        "audio_recordings",
        "platform_configs",
        "data",
        "app"
    ]

    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
        for f in files_to_include:
            if os.path.exists(f):
                zipf.write(f, arcname=f)
                print(f"  Added file: {f}")
                
        for folder in folders_to_include:
            if os.path.exists(folder):
                for root, dirs, files in os.walk(folder):
                    # Skip __pycache__
                    if "__pycache__" in root:
                        continue
                    for file in files:
                        full_path = os.path.join(root, file)
                        rel_path = os.path.relpath(full_path, ".")
                        zipf.write(full_path, arcname=rel_path)
                print(f"  Added folder: {folder}")

    size_mb = os.path.getsize(zip_filename) / (1024 * 1024)
    print(f"\n[SUCCESS] {zip_filename} created ({size_mb:.2f} MB)")

if __name__ == "__main__":
    package_submission()

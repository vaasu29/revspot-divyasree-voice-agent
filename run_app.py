import os
import sys
import webbrowser
import uvicorn

def main():
    print("=" * 70)
    print("  DIVYASREE 'WHISPERS OF THE WIND' AI VOICE AGENT SUITE")
    print("  Revspot AI Voice Agent Design Assessment")
    print("=" * 70)
    print("\nStarting local server on http://localhost:8000 ...")
    print("Press CTRL+C to stop.")
    
    # Auto-open browser after a short delay
    def open_browser():
        import time
        time.sleep(1.5)
        webbrowser.open("http://localhost:8000")

    import threading
    threading.Thread(target=open_browser, daemon=True).start()

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=False)

if __name__ == "__main__":
    main()

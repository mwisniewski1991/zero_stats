#!/usr/bin/env python3
"""
Skrypt do uruchamiania aplikacji web YouTube Statistics
"""

import os
import sys
from app import create_app

def main():
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Create Flask app
    app = create_app()
    
    # Get configuration
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    print(f"🚀 Uruchamianie aplikacji YouTube Statistics...")
    print(f"📍 Host: {host}")
    print(f"🔌 Port: {port}")
    print(f"🐛 Debug: {debug}")
    print(f"🌐 URL: http://{host}:{port}")
    print(f"📊 Dashboard: http://{host}:{port}/")
    print(f"📈 Playlisty: http://{host}:{port}/playlists/")
    print(f"🏆 Top Playlisty: http://{host}:{port}/top-playlists/")
    print("\nNaciśnij Ctrl+C aby zatrzymać serwer")
    
    try:
        app.run(host=host, port=port, debug=debug)
    except KeyboardInterrupt:
        print("\n👋 Zatrzymano serwer")
    except Exception as e:
        print(f"❌ Błąd: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 
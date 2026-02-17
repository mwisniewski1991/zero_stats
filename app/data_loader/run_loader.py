#!/usr/bin/env python3
"""
Skrypt do uruchamiania YouTube Data Loader
"""

import argparse
import sys
import logging
from .data_loader import DataLoader

def main():
    parser = argparse.ArgumentParser(description='YouTube Data Loader')
    parser.add_argument('--initial', action='store_true', 
                       help='Załaduj początkowe dane (wszystkie playlisty i filmy)')
    parser.add_argument('--check', action='store_true',
                       help='Jednorazowe sprawdzenie nowych filmów')
    
    args = parser.parse_args()
    
    if not any([args.initial, args.check]):
        parser.print_help()
        sys.exit(1)
    
    # Inicjalizacja data loadera
    loader = DataLoader()
    
    try:
        # Połącz z bazą danych
        loader.initialize_database()
        
        if args.initial:
            print("Ładowanie początkowych danych...")
            loader.load_initial_data()
            print("Zakończono ładowanie początkowych danych")
            
        if args.check:
            print("Sprawdzanie nowych filmów...")
            loader.check_for_new_videos()
            print("Zakończono sprawdzanie")
            
            
    except KeyboardInterrupt:
        print("\nZatrzymano przez użytkownika")
    except Exception as e:
        logging.error(f"Błąd: {e}")
        sys.exit(1)
    finally:
        loader.cleanup()

if __name__ == "__main__":
    main() 
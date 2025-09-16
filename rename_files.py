#!/usr/bin/env python3
"""
File Renaming Script for MarioIbago/math-aa-notes

This script renames all files and directories in a repository according to these rules:
1. Replace all spaces with underscores (_)
2. Convert to Title Case (each word starts with capital letter)
3. Preserve original file extensions
4. Apply to all files and directories including those in subdirectories

Example conversions:
- "area bajo la curva.pdf" -> "Area_Bajo_La_Curva.pdf"
- "resumen final.pdf" -> "Resumen_Final.pdf"
- "sub folder" -> "Sub_Folder"

Usage:
    python rename_files.py [directory_path]
    
If no directory is provided, it will use the current directory.
"""

import os
import sys
import unicodedata
from pathlib import Path


def normalize_filename(filename):
    """
    Normalize a filename according to the specified rules:
    1. Replace spaces with underscores
    2. Convert to Title Case
    3. Preserve file extension
    
    Args:
        filename (str): Original filename
        
    Returns:
        str: Normalized filename
    """
    # Split filename and extension
    name_part, extension = os.path.splitext(filename)
    
    # Strip leading and trailing spaces
    name_part = name_part.strip()
    
    # Replace multiple consecutive spaces with single spaces first
    import re
    name_part = re.sub(r'\s+', ' ', name_part)
    
    # Replace spaces with underscores
    name_part = name_part.replace(' ', '_')
    
    # Convert each word to title case
    # Split by underscores, capitalize each part, then rejoin
    words = name_part.split('_')
    title_cased_words = []
    
    for word in words:
        if word:  # Skip empty strings
            # Handle accented characters properly for title case
            title_word = word.capitalize()
            title_cased_words.append(title_word)
    
    # Rejoin with underscores
    normalized_name = '_'.join(title_cased_words)
    
    # Add back the extension (preserve original case)
    return normalized_name + extension


def should_skip_file(filepath):
    """
    Determine if a file should be skipped during renaming.
    
    Args:
        filepath (Path): Path to the file
        
    Returns:
        bool: True if file should be skipped
    """
    # Skip hidden files and directories
    if filepath.name.startswith('.'):
        return True
    
    # Skip common system/version control directories
    skip_dirs = {'.git', '.github', '.vscode', '__pycache__', 'node_modules', '.streamlit'}
    if any(part in skip_dirs for part in filepath.parts):
        return True
    
    # Skip files that don't need renaming (no spaces)
    if ' ' not in filepath.name:
        return True
        
    return False


def rename_files_in_directory(directory_path):
    """
    Rename all files and directories in the given directory and its subdirectories.
    
    Args:
        directory_path (str): Path to the directory to process
    """
    directory = Path(directory_path)
    
    if not directory.exists():
        print(f"Error: Directory '{directory_path}' does not exist.")
        return
    
    if not directory.is_dir():
        print(f"Error: '{directory_path}' is not a directory.")
        return
    
    print(f"Processing directory: {directory.absolute()}")
    print("=" * 60)
    
    # Track statistics
    files_renamed = 0
    dirs_renamed = 0
    skipped_count = 0
    error_count = 0
    
    # First pass: collect all directories that need renaming (bottom-up)
    # We need to rename directories from deepest to shallowest to avoid path issues
    dirs_to_rename = []
    for dirpath in directory.rglob('*'):
        if dirpath.is_dir() and not should_skip_file(dirpath) and ' ' in dirpath.name:
            dirs_to_rename.append(dirpath)
    
    # Sort directories by depth (deepest first)
    dirs_to_rename.sort(key=lambda p: len(p.parts), reverse=True)
    
    # Rename directories first
    for dirpath in dirs_to_rename:
        try:
            old_name = dirpath.name
            new_name = normalize_filename(old_name)
            
            if old_name != new_name:
                new_dirpath = dirpath.parent / new_name
                
                if new_dirpath.exists():
                    print(f"⚠️  Warning: Target directory already exists, skipping: {old_name} -> {new_name}")
                    skipped_count += 1
                    continue
                
                dirpath.rename(new_dirpath)
                print(f"📁 Renamed directory: {old_name} -> {new_name}")
                dirs_renamed += 1
        except Exception as e:
            print(f"❌ Error renaming directory {dirpath.name}: {str(e)}")
            error_count += 1
    
    # Second pass: rename files (need to re-scan as directory structure may have changed)
    for filepath in directory.rglob('*'):
        if filepath.is_file():
            try:
                # Check if file should be skipped
                if should_skip_file(filepath):
                    skipped_count += 1
                    continue
                
                # Get the new filename
                old_name = filepath.name
                new_name = normalize_filename(old_name)
                
                # If no change needed, skip
                if old_name == new_name:
                    skipped_count += 1
                    continue
                
                # Create new file path
                new_filepath = filepath.parent / new_name
                
                # Check if target file already exists
                if new_filepath.exists():
                    print(f"⚠️  Warning: Target file already exists, skipping: {old_name} -> {new_name}")
                    skipped_count += 1
                    continue
                
                # Perform the rename
                filepath.rename(new_filepath)
                print(f"📄 Renamed file: {old_name} -> {new_name}")
                files_renamed += 1
                
            except Exception as e:
                print(f"❌ Error renaming file {filepath.name}: {str(e)}")
                error_count += 1
    
    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY:")
    print(f"Files renamed: {files_renamed}")
    print(f"Directories renamed: {dirs_renamed}")
    print(f"Items skipped: {skipped_count}")
    print(f"Errors: {error_count}")
    print(f"Total items processed: {files_renamed + dirs_renamed + skipped_count + error_count}")


def main():
    """Main function to handle command line arguments and execute renaming."""
    
    # Get directory path from command line argument or use current directory
    if len(sys.argv) > 1:
        directory_path = sys.argv[1]
    else:
        directory_path = "."
    
    print("File Renaming Script for MarioIbago/math-aa-notes")
    print("=" * 60)
    print("Rules:")
    print("1. Replace spaces with underscores (_)")
    print("2. Convert to Title Case")
    print("3. Preserve file extensions")
    print("4. Process all files and directories in subdirectories")
    print()
    
    # Ask for confirmation before proceeding
    response = input(f"Do you want to rename files in '{directory_path}'? (y/N): ")
    if response.lower() not in ['y', 'yes']:
        print("Operation cancelled.")
        return
    
    print()
    rename_files_in_directory(directory_path)


if __name__ == "__main__":
    main()
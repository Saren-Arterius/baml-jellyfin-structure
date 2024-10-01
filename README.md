# TV Show Organizer

This Python project helps organize TV shows for Jellyfin by processing a folder of TV shows using LLM and creating symlinks to fit Jellyfin format.

## Setup (Run Once)

1. Clone this repository to your local machine.

2. Copy the environment template file:
   ```
   cp .env.template .env
   ```

3. Open the `.env` file and fill in your OpenRouter API key.

4. Create a virtual environment:
   ```
   python -m venv venv
   ```

5. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage (Run Every Time)

1. Activate the virtual environment:
   ```
   source venv/bin/activate
   ```

2. Load the environment variables:
   ```
   source .env
   ```

3. Process the TV shows folder:
   ```
   python3 process.py /path/to/tv-shows-folder data.json
   ```

4. Review and manually edit the `data.json` file if necessary.

5. Create symlinks for Jellyfin:
   ```
   python3 symlink.py /path/to/tv-shows-folder/jellyfin data.json
   ```

6. Preview the results and press 'y' to confirm the changes.

Note that `/path/to/tv-shows-folder/jellyfin` will be `rm -rf`ed for building symlinks so **TRIPLE CHECK** your path.

## Notes

- Make sure to replace `/path/to/tv-shows-folder` with the actual path to your TV shows folder.
- The `data.json` file will be created or updated in the current directory.
- Always review the `data.json` file before creating symlinks to ensure accuracy.

## Requirements
See `requirements.txt` for a list of required Python packages.
1. `mediainfo`
2. GNU parallel
2. POSIX environment
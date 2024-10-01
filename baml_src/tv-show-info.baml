// Defining a data model.
class TVShowInfo {
  idx int
  series_name string @description(#"Use full name if possible. DO NOT use underscores in series name. DO NOT translate. DO NOT include season info."#)
  season_number int? @description(#"Season number may not present. Is usually indicated by S1/S01 S2/S02"#)
  special_name string? @description(#"In some cases, there are special episodes usually denoted with OAD/OVA/SP/Bonus/MV/OP/ED/MMR/Sample or non integer episode number like 65.5 etc. Output them here. null if otherwise. DO NOT output special characters. DO NOT output numbers. If you encounter non video files, write its extension.
  "#)
  episode_number int? @description(#"Extremely likely to contain episode number. Find episode numbers with best effort. Episode numbers can be in brackets (v2/v3 indicates a re-release. remove v2/v3). If you encounter a range in filename, it indicates the range of episodes in the season, not the episode number. If you encounter special episodes, extract and output episode number (e.g. output 1 for OAD01 or OVA01, output 2 for SP02, output 3 for VOL.3, output 4 for EP4 and so on)
  "#)
}

class TVShowFile {
  folder string
  filename string
}

// Creating a function to extract the resume from a string.
function ExtractShowInfo(files: TVShowFile[]) -> TVShowInfo[] {
  client "OpenRouter" // Set OPENAI_API_KEY to use this client.
  prompt #"
Below are TV shows files. Extract info from filepaths below.
Each file is ONE EPISODE. 
Filepaths MAY contain additional/unrelated info that is not useful and confusing.
Filepaths are unstructured, so think logically and guess the episodes with best effort.
    {% for fp in files %}
      {{ loop.index }}. Folder: {{ fp.folder }} | Filename: {{ fp.filename }}
    {% endfor %}

    {{ ctx.output_format }}
  "#
}

// Testing the function with a sample resume.
test animes {
  functions [ExtractShowInfo]
  args {
    files [{
      folder "./To Love (1080p)/To Love Ru Darkness/11/"
      filename "[Airota][To Love-Ru Darkness][11][BDrip_1080P][x264-Hi10P_FLAC].mkv"
    }, {
      folder "./Hoozuki no Reitetsu (720p)/[BeanSub&FZSD][Hoozuki_no_Reitetsu_S2][01-26][BIG5][720P][MP4]/"
      filename "[BeanSub&FZSD][Hoozuki_no_Reitetsu_S2][12][BIG5][720P][x264_AAC].mp4"
    }]
  }
}

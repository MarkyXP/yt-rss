# YouTube Adapter (yt-dlp Implementation)

This directory contains the concrete implementation of the `YouTubePort` interface using the `yt-dlp` library.

## Overview

The `YouTubeDlpAdapter` class implements all three methods from the `YouTubePort` abstract base class:

1. **`get_videos_from_link(link: str)`** - Retrieves videos from channels, playlists, or user profiles
2. **`get_video_details(video_link: str)`** - Gets detailed video information including transcripts
3. **`search_channel(query: str)`** - Searches for YouTube channels

## Features

- **Channel/Playlist Support**: Fetch videos from any YouTube channel or playlist URL
- **Video Details**: Retrieve comprehensive video information including:
  - Title, publication date, thumbnails
  - View count, like count, duration
  - Description, channel information
  - Transcripts and caption tracks
- **Channel Search**: Search for channels by name or keyword
- **Error Handling**: Proper validation and error handling for YouTube links

## Dependencies

The adapter requires the `yt-dlp` library:

```bash
pip install yt-dlp
```

## Usage

```python
import asyncio
from app.adapters.yt.adapter import YouTubeDlpAdapter

async def main():
    adapter = YouTubeDlpAdapter()
    
    # Get videos from a channel
    videos = await adapter.get_videos_from_link(
        "https://www.youtube.com/@LinuxFoundation"
    )
    
    # Get detailed video information
    details = await adapter.get_video_details(
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    )
    
    # Search for a channel
    channels = await adapter.search_channel("Linux Foundation")

asyncio.run(main())
```

## Implementation Notes

### Transcript Handling

The adapter is designed to extract transcripts from videos. Note that:
- Transcripts are only available for videos that have captions
- The actual transcript extraction would require downloading caption files
- In the current implementation, the transcript field is set to `None` as a placeholder

### Channel Search Limitations

Due to limitations in `yt-dlp`, the channel search functionality:
- First attempts to access channels using the `@username` format
- Falls back to searching YouTube results if the direct approach fails
- May not return all possible results

### Error Handling

The adapter raises the following exceptions:
- `InvalidYouTubeLinkError`: When an invalid YouTube URL is provided
- `YouTubeError`: For general YouTube-related errors
- `YouTubeAPIError`: For API-specific errors

## Testing

Run the example in the adapter module to test basic functionality:

```bash
python -m app.adapters.yt.adapter
```

## Future Enhancements

Potential improvements:
- Add caching to reduce API calls
- Implement retry logic for failed requests
- Add support for pagination in channel/playlist results
- Enhance transcript extraction to actually download and parse captions
- Add support for more YouTube URL formats

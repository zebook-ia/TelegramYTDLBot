import re
from y2mate_api import Handler

def extract_youtube_links(text: str) -> list[str]:
    """
    Extracts YouTube links from a given text.
    """
    link_filter = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    all_links = re.findall(link_filter, text)
    yt_links = [link for link in all_links if 'youtube.com' in link or 'youtu.be' in link]
    return yt_links

def get_video_qualities(video_url: str) -> list[dict]:
    """
    Fetches available video qualities for a given YouTube URL.
    Returns a list of dictionaries, each containing 'q' (quality), 'size', and 'dlink'.
    Returns an empty list if no qualities are found or an error occurs.
    """
    try:
        yt_api = Handler(video_url)
        q_list = ['4k', '1080p', '720p', '480p', '360p', '240p']
        
        available_qualities = []

        for quality_preference in q_list:
            for video_metadata in yt_api.run(quality=quality_preference):
                q = video_metadata.get("q")
                dlink = video_metadata.get("dlink")
                size = video_metadata.get("size")
                
                if dlink:
                    # Check if this quality (q) is already added to avoid duplicates from Handler behavior
                    if not any(item['q'] == q for item in available_qualities):
                        available_qualities.append({"q": q, "size": size, "dlink": dlink})

        # Sort qualities for consistent presentation if needed, e.g., by a predefined order or size
        # For now, returning as found, but y2mate_api might return them in a specific order.
        return available_qualities
    except Exception as e:
        print(f"Error fetching video qualities for {video_url}: {e}")
        return []

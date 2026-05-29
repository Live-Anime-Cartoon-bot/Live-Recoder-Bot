"""
Streams Database - All available streams for recording
"""

STREAMS = {
    # 🎬 Kids Channels
    "Disney Channel HD": "http://66.102.126.10:8000/play/a013/index.m3u8",
    "Disney International HD": "http://66.102.126.10:8000/play/a078/index.m3u8",
    "Disney Junior": "http://66.102.126.10:8000/play/a004/index.m3u8",
    "Nick": "http://66.102.126.10:8000/play/a00w/index.m3u8",
    "Nick Jr.": "http://66.102.126.10:8000/play/a00m/index.m3u8",
    "Pogo": "http://66.102.126.10:8000/play/a00d/index.m3u8",
    "Sonic": "http://66.102.126.10:8000/play/a00p/index.m3u8",
    "Cartoon Network": "http://66.102.126.10:8000/play/a011/index.m3u8",
    "Discovery Kids": "http://66.102.126.10:8000/play/a00l/index.m3u8",
    "Hungama": "http://66.102.126.10:8000/play/a00b/index.m3u8",
}

# Aliases for easier searching
STREAM_ALIASES = {
    "disney": "Disney Channel HD",
    "nick": "Nick",
    "pogo": "Pogo",
    "cartoon": "Cartoon Network",
    "sonic": "Sonic",
    "hungama": "Hungama",
    "discovery": "Discovery Kids",
    "jr": "Nick Jr.",
}


def get_stream_url(stream_name: str) -> str:
    """
    Get stream URL by name or alias
    Returns: URL string or None if not found
    """
    # Direct match
    if stream_name in STREAMS:
        return STREAMS[stream_name]
    
    # Case-insensitive match
    for key in STREAMS:
        if key.lower() == stream_name.lower():
            return STREAMS[key]
    
    # Alias match
    lower_name = stream_name.lower()
    if lower_name in STREAM_ALIASES:
        actual_name = STREAM_ALIASES[lower_name]
        return STREAMS.get(actual_name)
    
    return None


def get_all_streams() -> dict:
    """Get all available streams"""
    return STREAMS


def list_streams_by_category(category: str = None) -> list:
    """List all streams (optionally by category)"""
    if category is None:
        return list(STREAMS.keys())
    return [name for name in STREAMS.keys() if category.lower() in name.lower()]


def search_stream(query: str) -> list:
    """Search streams by partial name"""
    query_lower = query.lower()
    results = []
    
    # Search in main streams
    for name in STREAMS.keys():
        if query_lower in name.lower():
            results.append(name)
    
    # Search in aliases
    for alias, actual_name in STREAM_ALIASES.items():
        if query_lower in alias.lower() and actual_name not in results:
            results.append(actual_name)
    
    return results

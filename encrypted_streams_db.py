"""
Encrypted Streams Database - Links are encrypted
"""

from encrypt import encrypt_url, decrypt_url

# ⚠️ DO NOT EXPOSE THESE ENCRYPTED STRINGS
# They are encrypted versions of actual streaming URLs
ENCRYPTED_STREAMS = {
    "Disney Channel HD": "gAAAAABmM2q7...",  # Will be auto-filled
    "Disney International HD": "gAAAAABmM2q8...",
    "Disney Junior": "gAAAAABmM2q9...",
    "Nick": "gAAAAABmM2qa...",
    "Nick Jr.": "gAAAAABmM2qb...",
    "Pogo": "gAAAAABmM2qc...",
    "Sonic": "gAAAAABmM2qd...",
    "Cartoon Network": "gAAAAABmM2qe...",
    "Discovery Kids": "gAAAAABmM2qf...",
    "Hungama": "gAAAAABmM2qg...",
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
    Get decrypted stream URL by name
    Returns: Actual URL (decrypted at runtime)
    """
    # Direct match
    if stream_name in ENCRYPTED_STREAMS:
        encrypted_url = ENCRYPTED_STREAMS[stream_name]
        return decrypt_url(encrypted_url)
    
    # Case-insensitive match
    for key in ENCRYPTED_STREAMS:
        if key.lower() == stream_name.lower():
            encrypted_url = ENCRYPTED_STREAMS[key]
            return decrypt_url(encrypted_url)
    
    # Alias match
    lower_name = stream_name.lower()
    if lower_name in STREAM_ALIASES:
        actual_name = STREAM_ALIASES[lower_name]
        encrypted_url = ENCRYPTED_STREAMS.get(actual_name)
        if encrypted_url:
            return decrypt_url(encrypted_url)
    
    return None


def get_all_streams() -> list:
    """Get all stream names (NOT URLs)"""
    return list(ENCRYPTED_STREAMS.keys())


def list_streams_by_category(category: str = None) -> list:
    """List all stream names"""
    if category is None:
        return list(ENCRYPTED_STREAMS.keys())
    return [name for name in ENCRYPTED_STREAMS.keys() if category.lower() in name.lower()]


def search_stream(query: str) -> list:
    """Search streams by partial name"""
    query_lower = query.lower()
    results = []
    
    # Search in main streams
    for name in ENCRYPTED_STREAMS.keys():
        if query_lower in name.lower():
            results.append(name)
    
    # Search in aliases
    for alias, actual_name in STREAM_ALIASES.items():
        if query_lower in alias.lower() and actual_name not in results:
            results.append(actual_name)
    
    return results

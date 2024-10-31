from youtubesearchpython import VideosSearch
from typing import List, Dict, Optional, Tuple
import logging
import re
import time
from datetime import datetime, timedelta

def search_youtube(primary_query: str, secondary_query: str = "", limit: int = 10, 
                  upload_date: str = "any", duration: str = "any") -> Tuple[int, List[Dict]]:
    """
    Search YouTube for videos matching the given criteria.
    
    :param primary_query: Main search term
    :param secondary_query: Additional search terms
    :param limit: Maximum number of videos to return
    :param upload_date: Filter by upload date ('any', 'today', 'this_week', 'this_month', 'this_year')
    :param duration: Filter by duration ('any', 'short', 'medium', 'long')
    :return: Tuple of (total_results, filtered_videos)
    """
    search_query = f"{primary_query} {secondary_query}".strip()
    videos_search = VideosSearch(search_query, limit=limit)
    
    try:
        search_results = videos_search.result()
        videos = search_results.get('result', [])
        total_results = len(videos)
        
        filtered_videos = []
        for video in videos:
            # Skip if video doesn't match duration filter
            if duration != "any":
                video_duration = video.get('duration', '0:00')
                if not video_duration:  # Skip if duration is None or empty
                    continue
                    
                # Convert duration to seconds
                try:
                    parts = video_duration.split(':')
                    if len(parts) == 2:  # MM:SS format
                        duration_seconds = int(parts[0]) * 60 + int(parts[1])
                    elif len(parts) == 3:  # HH:MM:SS format
                        duration_seconds = int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
                    else:
                        continue
                    
                    if duration == "short" and duration_seconds > 240:  # > 4 minutes
                        continue
                    elif duration == "medium" and (duration_seconds <= 240 or duration_seconds > 1200):  # 4-20 minutes
                        continue
                    elif duration == "long" and duration_seconds <= 1200:  # < 20 minutes
                        continue
                except (ValueError, IndexError):
                    continue
            
            # Skip if video doesn't match upload date filter
            if upload_date != "any":
                publish_time = video.get('publishedTime', '')
                if not _check_upload_date(publish_time, upload_date):
                    continue
            
            # Extract view count safely
            view_count = video.get('viewCount', {})
            if isinstance(view_count, dict):
                views = view_count.get('text', '0 views').replace(' views', '')
            else:
                views = '0'
            
            filtered_videos.append({
                'title': video.get('title', ''),
                'link': video.get('link', ''),
                'duration': video.get('duration', ''),
                'views': views,
                'publish_time': video.get('publishedTime', ''),
                'channel': video.get('channel', {}).get('name', ''),
                'description': video.get('description', ''),
                'score': _calculate_video_score(video, primary_query, secondary_query)
            })
        
        return total_results, sorted(filtered_videos, key=lambda x: x['score'], reverse=True)
    
    except Exception as e:
        logging.error(f"Error searching YouTube: {str(e)}")
        return 0, []

def _check_upload_date(publish_time: str, upload_date: str) -> bool:
    """Check if the video's upload date matches the filter."""
    if upload_date == "any" or not publish_time:
        return True
        
    try:
        # Convert relative time to datetime
        now = datetime.now()
        if "year" in publish_time:
            return upload_date == "this_year"
        elif "month" in publish_time:
            months = int(publish_time.split()[0])
            return upload_date in ["this_year", "this_month"] and months <= 1
        elif "week" in publish_time:
            weeks = int(publish_time.split()[0])
            return upload_date in ["this_year", "this_month", "this_week"] and weeks <= 1
        elif "day" in publish_time:
            days = int(publish_time.split()[0])
            return upload_date in ["this_year", "this_month", "this_week"] or (upload_date == "today" and days < 1)
        elif "hour" in publish_time:
            return True  # Today's content
        return False
    except:
        return True

def _calculate_video_score(video: Dict, primary_query: str, secondary_query: str) -> float:
    """Calculate a relevance score for the video."""
    score = 0.0
    
    # Title and channel matching
    title = video.get('title', '').lower()
    channel = video.get('channel', {}).get('name', '').lower()
    primary_query_lower = primary_query.lower()
    
    # Channel name exact match (highest priority)
    channel_keywords = set(primary_query_lower.split())
    if any(keyword in channel for keyword in channel_keywords):
        score += 10.0  # Significant boost for channel match
    
    # Exact phrase matching in title
    if primary_query_lower in title:
        score += 5.0
    
    # Individual keyword matching (secondary priority)
    primary_keywords = primary_query_lower.split()
    secondary_keywords = secondary_query.lower().split() if secondary_query else []
    
    # Count how many words match in sequence
    words_in_sequence = 0
    for i in range(len(primary_keywords)):
        if i < len(primary_keywords) - 1:
            two_words = f"{primary_keywords[i]} {primary_keywords[i+1]}"
            if two_words in title:
                words_in_sequence += 1
    score += words_in_sequence * 2.0
    
    # Individual word matching
    matching_primary_words = sum(1 for word in primary_keywords if word in title)
    score += matching_primary_words * 1.0
    
    # View count bonus (more significant for channel relevance)
    try:
        views = video.get('viewCount', {}).get('text', '0').replace(' views', '').replace(',', '')
        view_count = int(views)
        if view_count > 1000000:
            score += 2.0  # Increased weight for popular videos
        elif view_count > 100000:
            score += 1.0
    except:
        pass
    
    # Recent upload bonus
    publish_time = video.get('publishedTime', '')
    if 'hour' in publish_time:
        score += 0.4
    elif 'day' in publish_time:
        score += 0.3
    elif 'week' in publish_time:
        score += 0.2
    elif 'month' in publish_time:
        score += 0.1
    
    return score

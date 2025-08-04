import pytest
from modules.checker import extract_youtube_links, get_video_qualities


# Tests for extract_youtube_links
def test_extract_youtube_links_with_standard_link():
    text = "Check out this video: https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    assert extract_youtube_links(text) == ["https://www.youtube.com/watch?v=dQw4w9WgXcQ"]

def test_extract_youtube_links_with_shortened_link():
    text = "Here's a short link: https://youtu.be/dQw4w9WgXcQ"
    assert extract_youtube_links(text) == ["https://youtu.be/dQw4w9WgXcQ"]

def test_extract_youtube_links_with_multiple_links():
    text = "First link: https://youtube.com/watch?v=123, second link: https://youtu.be/456"
    assert extract_youtube_links(text) == ["https://youtube.com/watch?v=123", "https://youtu.be/456"]

def test_extract_youtube_links_with_no_youtube_links():
    text = "This is a string with a link to another site: https://www.google.com"
    assert extract_youtube_links(text) == []

def test_extract_youtube_links_with_no_links_at_all():
    text = "This is a plain text message without any links."
    assert extract_youtube_links(text) == []

def test_extract_youtube_links_with_link_and_query_params():
    text = "A video with timestamp: https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=60s"
    assert extract_youtube_links(text) == ["https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=60s"]


# Tests for get_video_qualities
def test_get_video_qualities_success(mocker):
    """Test get_video_qualities when the API returns valid data."""
    # Mock the Handler class from y2mate_api
    mock_handler_class = mocker.patch('modules.checker.Handler')

    # Define a side effect for the run method to simulate API responses
    def side_effect(quality):
        if quality == '720p':
            return [{"q": "720p", "size": "50 MB", "dlink": "http://example.com/720p"}]
        if quality == '360p':
            return [{"q": "360p", "size": "20 MB", "dlink": "http://example.com/360p"}]
        return []

    mock_handler_class.return_value.run.side_effect = side_effect

    video_url = "https://www.youtube.com/watch?v=some_video"
    qualities = get_video_qualities(video_url)

    # Assert that the handler was initialized
    mock_handler_class.assert_called_once_with(video_url)

    # Assert the structure of the returned data
    assert len(qualities) == 2
    assert qualities[0]['q'] == '720p'
    assert qualities[1]['q'] == '360p'
    assert qualities[0]['dlink'] == 'http://example.com/720p'

def test_get_video_qualities_api_error(mocker):
    """Test get_video_qualities when the API raises an exception."""
    # Mock the Handler to raise an exception upon instantiation
    mocker.patch('modules.checker.Handler', side_effect=Exception("API is down"))

    video_url = "https://www.youtube.com/watch?v=error_video"
    qualities = get_video_qualities(video_url)

    # Expect an empty list as the function should handle the exception gracefully
    assert qualities == []

def test_get_video_qualities_no_streams_found(mocker):
    """Test get_video_qualities when the API returns no downloadable streams."""
    mock_handler_instance = mocker.MagicMock()
    mock_handler_instance.run.return_value = []  # Simulate no streams found
    mocker.patch('modules.checker.Handler', return_value=mock_handler_instance)

    video_url = "https://www.youtube.com/watch?v=no_streams"
    qualities = get_video_qualities(video_url)

    assert qualities == []

def test_get_video_qualities_avoids_duplicates(mocker):
    """Test that the function correctly avoids adding duplicate qualities."""
    mock_handler_class = mocker.patch('modules.checker.Handler')

    # Simulate the API returning a 720p stream even when 1080p is requested
    def side_effect(quality):
        if quality == '1080p':
            return [{"q": "720p", "size": "50 MB", "dlink": "http://example.com/720p"}]
        if quality == '720p':
            return [{"q": "720p", "size": "50 MB", "dlink": "http://example.com/720p"}]
        return []

    mock_handler_class.return_value.run.side_effect = side_effect

    video_url = "https://www.youtube.com/watch?v=duplicates"
    qualities = get_video_qualities(video_url)

    # The function should only have one entry for 720p
    assert len(qualities) == 1
    assert qualities[0]['q'] == '720p'
    assert [q['q'] for q in qualities] == ['720p']

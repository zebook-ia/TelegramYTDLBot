import os
import pytest
from modules.ytdownloader import download

@pytest.fixture
def mock_bot(mocker):
    """Fixture to create a mock bot object."""
    bot = mocker.MagicMock()
    # When send_message is called, return another mock that has a message_id and chat.id
    bot.send_message.return_value = mocker.MagicMock(message_id=123, chat=mocker.MagicMock(id=456))
    return bot

@pytest.fixture
def mock_message(mocker):
    """Fixture to create a mock message object."""
    message = mocker.MagicMock()
    message.chat.id = 456
    return message

@pytest.fixture
def mock_dependencies(mocker):
    """Fixture to mock all external dependencies of the download function."""
    # Mock y2mate_api Handler and its run method
    mock_handler_instance = mocker.MagicMock()
    # The .run() method returns a list of dictionaries
    mock_handler_instance.run.return_value = [{
        'vid': 'test_vid',
        'q': '720p',
        'ftype': 'mp4'
    }]
    # The save() method also needs to be mocked
    mock_handler_instance.save = mocker.MagicMock()
    mocker.patch('modules.ytdownloader.Handler', return_value=mock_handler_instance)

    # Mock pytube.YouTube
    mock_youtube_instance = mocker.MagicMock()
    mock_youtube_instance.thumbnail_url = "http://example.com/thumb.jpg"
    mock_youtube_instance.title = "Test Video Title"
    mocker.patch('modules.ytdownloader.pytube.YouTube', return_value=mock_youtube_instance)

    # Mock requests.get for fetching thumbnail
    mock_requests_get = mocker.patch('modules.ytdownloader.requests.get')
    mock_requests_get.return_value.content = b'thumbnail_content'

    # Mock os functions
    mocker.patch('modules.ytdownloader.os.path.exists', return_value=True)
    mocker.patch('modules.ytdownloader.os.makedirs')
    mock_os_remove = mocker.patch('modules.ytdownloader.os.remove')
    mock_os_getsize = mocker.patch('modules.ytdownloader.os.path.getsize')

    # Mock subprocess.run for ffmpeg
    mock_subprocess_run = mocker.patch('modules.ytdownloader.subprocess.run')

    # Mock the open built-in for reading the file to send
    mocker.patch('builtins.open', mocker.mock_open(read_data=b"video_data"))

    return {
        "handler_instance": mock_handler_instance,
        "subprocess_run": mock_subprocess_run,
        "os_remove": mock_os_remove,
        "os_getsize": mock_os_getsize,
    }


def test_download_small_video(mock_bot, mock_message, mock_dependencies):
    """Test the download process for a video that does not need compression."""
    # Arrange: Set file size to be small (1 MB)
    mock_dependencies['os_getsize'].return_value = 1 * 1024 * 1024

    # Act
    download(bot=mock_bot, message=mock_message, userInput="720p", videoURL="http://youtube.com/video")

    # Assert
    # Check that download message was sent and then edited to "Uploading"
    mock_bot.send_message.assert_called_once_with(chat_id=mock_message.chat.id, text="<b>Downloading...📥</b>")
    mock_bot.edit_message_text.assert_called_once_with(chat_id=mock_message.chat.id, message_id=123, text="<b>Uploading...📤</b>")

    # Check that compression (subprocess) was NOT called
    mock_dependencies['subprocess_run'].assert_not_called()

    # Check that the video was sent via the bot
    mock_bot.send_video.assert_called_once()

    # Check that the downloaded file was removed
    media_path = f"{os.getcwd()}/vids"
    file_name = "test_vid_720p.mp4"
    expected_path = os.path.join(media_path, file_name)
    mock_dependencies['os_remove'].assert_called_once_with(expected_path)

    # Check that the initial status message was deleted
    mock_bot.delete_message.assert_called_once_with(mock_message.chat.id, 123)


def test_download_large_video_with_compression(mock_bot, mock_message, mock_dependencies):
    """Test the download process for a large video that requires compression."""
    # Arrange: Set file size to be large (3 GB)
    mock_dependencies['os_getsize'].return_value = 3 * 1024 * 1024 * 1024

    # Act
    download(bot=mock_bot, message=mock_message, userInput="720p", videoURL="http://youtube.com/video")

    # Assert
    # Check that the "compressing" message was shown
    mock_bot.edit_message_text.assert_any_call(
        chat_id=mock_message.chat.id,
        message_id=123,
        text="<b>Arquivo grande, comprimindo...</b>",
    )

    # Check that ffmpeg (subprocess) was called for compression
    mock_dependencies['subprocess_run'].assert_called_once()

    # Check that the video was sent
    mock_bot.send_video.assert_called_once()

    # Check that both the original and compressed files were removed
    media_path = f"{os.getcwd()}/vids"
    original_file = os.path.join(media_path, "test_vid_720p.mp4")
    compressed_file = os.path.join(media_path, "compressed_test_vid_720p.mp4")

    mock_dependencies['os_remove'].assert_any_call(original_file)
    mock_dependencies['os_remove'].assert_any_call(compressed_file)
    assert mock_dependencies['os_remove'].call_count == 2

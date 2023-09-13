"""Data used in test_client.py"""
MOCK_CHANNEL_METADATA = {
    "channel_id": "test_channel_id",
    "title": "Test Channel",
    "description": "Test description",
    "channel_title": "Test Channel Title",
    "publish_time": "2023-09-10T00:00:00Z",
    "published_at": "2023-09-10T00:00:00Z",
    "synctimestamp": "2023-09-10T00:00:00Z",
}

CHANNEL_NAME = "Andrew Huberman"
EXPECTED_CHANNEL_ID = "UC2D2CMWXMOVWx7giW1n3LIg"
EXPECTED_CHANNEL_METADATA = {
    'kind': 'youtube#searchResult',
    'etag': '9UNEqum6_YmGcgTOl3TXLuvi1h8',
    'id': {
        'kind': 'youtube#channel', 'channelId': 'UC2D2CMWXMOVWx7giW1n3LIg'
    },
    'snippet': {
        'publishedAt': '2013-04-21T14:41:36Z',
        'channelId': 'UC2D2CMWXMOVWx7giW1n3LIg',
        'title': 'Andrew Huberman',
        'description': (
            'Welcome to the official Huberman Lab YouTube channel. The Huberman Lab podcast is hosted by Dr. Andrew Huberman, ...',
        ),
        'thumbnails': {
            'default': {
                'url': 'https://yt3.ggpht.com/5ONImZvpa9_hYK12Xek2E2JLzRc732DWsZMX2F-AZ1cTutTQLBuAmcEtFwrCgypqJncl5HrV2w=s88-c-k-c0xffffffff-no-rj-mo'
            },
            'medium': {
                'url': 'https://yt3.ggpht.com/5ONImZvpa9_hYK12Xek2E2JLzRc732DWsZMX2F-AZ1cTutTQLBuAmcEtFwrCgypqJncl5HrV2w=s240-c-k-c0xffffffff-no-rj-mo'
            },
            'high': {
                'url': 'https://yt3.ggpht.com/5ONImZvpa9_hYK12Xek2E2JLzRc732DWsZMX2F-AZ1cTutTQLBuAmcEtFwrCgypqJncl5HrV2w=s800-c-k-c0xffffffff-no-rj-mo'
            }
        },
        'channelTitle': 'Andrew Huberman',
        'liveBroadcastContent': 'none',
        'publishTime': '2013-04-21T14:41:36Z'
    }
}

from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from datetime import datetime, timedelta

def get_top_videos(request):
    if request.method == 'POST':
        api_key = 'AIzaSyA-7ranUk4dCfU_n2TLnXsW-6lz1z4K__E'
        youtube = build('youtube', 'v3', developerKey=api_key)

        # ID do canal selecionado no formulário
        channel_id = request.POST.get('channel_id')

        videos = []
        one_week_ago = (datetime.utcnow() - timedelta(days=7)).isoformat("T") + "Z"

        try:
            search_request = youtube.search().list(
                part="snippet",
                channelId=channel_id,
                order="viewCount",
                maxResults=6,
                publishedAfter=one_week_ago
            )
            response = search_request.execute()

            for item in response['items']:
                video = {
                    'title': item['snippet']['title'],
                    'thumbnail': item['snippet']['thumbnails']['high']['url'],
                    'video_id': item['id']['videoId']
                }
                videos.append(video)

        except HttpError as e:
            return JsonResponse({'error': str(e)}, status=500)

        return JsonResponse({'videos': videos})

    # Caso seja uma requisição GET, renderize a página com o template
    return render(request, 'videos.html')

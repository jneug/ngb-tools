from flask import Blueprint, Response, stream_with_context, request, redirect, current_app, g, render_template
from pytube import YouTube
import requests

bp = Blueprint('ytdl.web', __name__, template_folder='templates')

mimetypes = {
    'video/mp4': 'mp4'
}

@bp.route('/')
def start():
    return render_template('ytdl/input.html')

@bp.route('/download', methods=('GET','POST'))
def download():
    vidurl = request.args.get('vidurl', '')

    if len(vidurl):
        yt = YouTube(vidurl)
        stream = yt.streams.filter(file_extension='mp4', resolution='720p').order_by('resolution').desc().first()
        if stream == None:
            stream = yt.streams.filter(file_extension='mp4', resolution='720p').order_by('resolution').desc().first()

        if stream:
            req = requests.get(stream.url, stream=True)

            ext = 'mp4'
            if req.headers['content-type'] in mimetypes:
                ext = mimetypes[req.headers['content-type']]

            headers = {x:y for x,y in req.headers.items()}
            headers['Content-Disposition'] = f'attachment; filename="{yt.title}.{ext}"';
            return Response(
                response=stream_with_context(req.iter_content()),
                status=req.status_code,
                headers=headers,
                content_type=req.headers['content-type'],
                )
    return "Invalid url";

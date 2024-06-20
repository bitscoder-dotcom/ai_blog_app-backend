from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
import os
import openai
import assemblyai as aai
from pytube import YouTube

# Create your views here.
@login_required
def index(request):
    return render(request, 'index.html')

@csrf_exempt
def generate_blog(request):
    if request == 'POST':
        try:
            data = json.loads(request.body)
            yt_link = data['link']
        except(KeyError, json.JSONDecodeError):
            return JsonResponse({'error': 'Invalid data sent'}, status = 400)
        
    # get video title
        title = yt_title(yt_link)

    # get transcript
        transcription = get_transcription(yt_link)
        if not transcription:
            return JsonResponse({'error': 'Failed to get transcript'}, status = 500)

    # use openai to generate blog
        blog_content = generate_blog_from_transcription(transcription)
        if not blog_content:
            return JsonResponse({'error': 'Failed to generate blog article'}, status = 500)

    # save blog article to databse

    # return blog article as a response 

        return JsonResponse({'content': blog_content})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status = 405)


def yt_title(link):
    yt = YouTube(link)
    title = yt.title
    return title

def download_audio(link):
    yt = YouTube(link)
    video = yt.streams.filter(only_audio=True).first()
    out_file = video.download(output_path=settings.MEDIA_ROOT)
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)
    return new_file

def get_transcription(link):
    audio_file = download_audio(link)
    aai.settings.api_key = settings.ASSEMBLYAI_API_KEY

    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_file)

    return transcript.text

def generate_blog_from_transcription(transcript):
    openai.api_key = settings.OPENAI_API_KEY
    prompt = f'''Based on the following transcript from a YouTube video, write a comprehensive blog article, 
                write it based on the transcribe but do not make it look like a youtube video, make it look like
                a proper blog article:\n\n{transcript}\n\nArticle:'''
    response = openai.completions.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=1000
    )
    generated_content = response.choices[0].text.strip

    return generated_content

def user_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirmPassword = request.POST['confirmPassword']

        if password == confirmPassword:
            try:
                user = User.objects.create_user(username, email, password)
                user.save
                login(request, user)
                return redirect('/')
            except IntegrityError:
                error_message = 'Username already exists'
                return render(request, 'signup.html', {'error_message':error_message})
        else:
             error_message = 'Password do not match'
             return render(request, 'signup.html', {'error_message':error_message})
    return render(request, 'signup.html')

def user_login(request):

    if request.method == 'POST':
       username = request.POST['username']
       password = request.POST['password']

       user = authenticate(request, username = username, password=password)
       if user is not None:
           login(request, user)
           return redirect('/')
       else:
           error_message = 'Invalid login details'
           return render(request, 'login.html', {'error_message':error_message})

    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')
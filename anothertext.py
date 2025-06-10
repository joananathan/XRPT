from flask import Flask, render_template, request, redirect, url_for, flash
import subprocess, os, ast
from pytubefix import YouTube
import assemblyai as aai
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from pydub import AudioSegment
from datetime import timedelta
from moviepy import *
from content_aware_crop import load_yolov8_model, process_video, add_audio_to_video

def crop_clips():
    folder = "clips"
    i = 1
    for clip in os.listdir(folder):
        input_video_path = os.path.join(folder, clip)
        print(input_video_path)
        processed_video_path = f"clips\\cropped_no_audio{i}.mp4"
        final_output_path = f"clips\\cropped_final{i}.mp4"
        yolo_model_path = "static\\assets\\yolov8n.pt"
        
        model = load_yolov8_model(yolo_model_path)
        
        process_video(
            input_path=input_video_path,
            output_path=processed_video_path,
            model=model,
            target_aspect_ratio=9/16,
            smoothing_factor=0.95,
            min_confidence=0.6
        )
        
        add_audio_to_video(input_video_path, processed_video_path, final_output_path)
        
        i += 1
        file_path = os.path.join(folder, clip)
        if os.path.isfile(file_path):
            os.remove(file_path)

crop_clips()
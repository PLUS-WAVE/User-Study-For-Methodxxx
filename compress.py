import os
import subprocess

def get_video_resolution(video_path):
    """
    Get the resolution of a video using ffprobe.

    Args:
        video_path (str): Path to the video file.

    Returns:
        tuple: (width, height) of the video.
    """
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
         "stream=width,height", "-of", "csv=p=0", video_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    width, height = map(int, result.stdout.strip().split(','))
    return width, height

def calculate_new_resolution(width, height, scale_factor=0.5):
    """
    Calculate the new resolution by scaling down the original resolution.

    Args:
        width (int): Original width.
        height (int): Original height.
        scale_factor (float): Factor by which to scale down the resolution.

    Returns:
        str: New resolution in the format "width:height".
    """
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)
    return f"{new_width}:{new_height}"

def compress_videos(input_folder, output_folder, crf=28, scale_factor=0.5):
    """
    Compress all videos in the input folder, reduce resolution, and save them to the output folder.

    Args:
        input_folder (str): Path to the folder containing input videos.
        output_folder (str): Path to the folder where compressed videos will be saved.
        crf (int): Constant Rate Factor for compression (lower is better quality, default is 28).
        scale_factor (float): Factor by which to scale down the resolution.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file_name in os.listdir(input_folder):
        input_path = os.path.join(input_folder, file_name)
        if os.path.isfile(input_path) and file_name.lower().endswith(('.mp4', '.mov', '.avi', '.mkv')):
            output_path = os.path.join(output_folder, file_name)
            print(f"Processing: {input_path}")
            
            # Get original resolution
            original_width, original_height = get_video_resolution(input_path)
            # Calculate new resolution
            new_resolution = calculate_new_resolution(original_width, original_height, scale_factor)
            
            print(f"Compressing: {input_path} -> {output_path} with resolution {new_resolution}")
            # Use ffmpeg to compress the video and reduce resolution
            subprocess.run([
                "ffmpeg", "-i", input_path, "-vcodec", "libx264", "-crf", str(crf),
                "-vf", f"scale={new_resolution}", output_path
            ], check=True)
    print("Compression completed.")

if __name__ == "__main__":
    input_folder = "videos/original"  # Replace with your input folder path
    output_folder = "compressed_videos"  # Replace with your output folder path
    compress_videos(input_folder, output_folder, crf=28, scale_factor=0.5)  # Example: scale down by 50%
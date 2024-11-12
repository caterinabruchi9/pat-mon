import os
import cv2

def video_to_segments(input_file, output_frame_rate, output_length_seconds, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Load the video file
    cap = cv2.VideoCapture(input_file)
   
    if not cap.isOpened():
        print("Error: Could not open video file.")
        return

    # Get the input video frame rate, frame count, and frame dimensions
    input_frame_rate = 30
    total_frames = 900
    frame_width = 1920
    frame_height = 1080
    
    # Calculate the total duration of the input video in seconds
    input_duration_seconds = total_frames / input_frame_rate
    
    print(f"Input Video: {input_duration_seconds:.2f}s at {input_frame_rate:.2f} FPS, {frame_width}x{frame_height} resolution.")
    
    # Calculate frame interval and frames per segment for undersampling
    frame_interval = max(1, int(round(input_frame_rate / output_frame_rate)))
    frames_per_segment = int(output_frame_rate * output_length_seconds)
    print(f"Output Video: {output_frame_rate:.2f} FPS, {frames_per_segment} frames per segment.")
    
    segment_index = 0
    frame_count = 0
    segment_frames = 0
    output_video_writer = None

    # Extract the base name of the input file to use in the output file names
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    
    # Loop over frames in the video
    while cap.isOpened():
        ret, frame = cap.read()
        
        # Stop if no more frames are available
        if not ret:
            break
        
        # Only process every nth frame to achieve the desired output frame rate
        if frame_count % frame_interval == 0:
            # Resize the frame to 640x480
            frame_resized = cv2.resize(frame, (640, 480))
            
            # Start a new segment if necessary
            if segment_frames == 0:
                output_path = os.path.join(output_folder, f"{base_name}_segment_{segment_index}.mp4")
                output_video_writer = cv2.VideoWriter(
                    output_path, 
                    cv2.VideoWriter_fourcc(*'mp4v'), 
                    output_frame_rate, 
                    (640, 480)  # Output video resolution
                )
           
            # Write the resized frame to the current segment
            output_video_writer.write(frame_resized)
            segment_frames += 1

            # Check if we've reached the desired length for this segment
            if segment_frames >= frames_per_segment:
                # Close the current segment
                output_video_writer.release()
                segment_index += 1
                segment_frames = 0

        frame_count += 1

    # Release any remaining resources
    cap.release()
    if output_video_writer is not None and segment_frames > 0:
        output_video_writer.release()

    print(f"Video '{input_file}' successfully split into {segment_index} segments.")

def process_all_videos(input_folder, output_frame_rate, output_length_seconds, output_folder):
    # List all video files in the input folder
    for file_name in os.listdir(input_folder):
        if file_name.endswith(('.mp4', '.avi', '.mov', '.mkv')):  # Add any other video formats you want to support
            input_file = os.path.join(input_folder, file_name)
            video_to_segments(input_file, output_frame_rate, output_length_seconds, output_folder)

# Example usage:
input_folder = "original"  # Folder containing input video files
output_frame_rate = 15   # Desired frame rate for the output segments
output_length_seconds = 5 # Length of each output video segment in seconds
output_folder = "cutSHORT"    # Folder to save the output segments

process_all_videos(input_folder, output_frame_rate, output_length_seconds, output_folder)

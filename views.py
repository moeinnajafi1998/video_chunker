from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import cv2,os,tempfile,requests

class VideoToFrames(APIView):
    def post(self, request, *args, **kwargs):
        try:
            video_file = request.FILES['video']
            with tempfile.NamedTemporaryFile(delete=False) as temp_video:
                for chunk in video_file.chunks():
                    temp_video.write(chunk)
            temp_video_path = temp_video.name
            frames_directory = self.process_frames(temp_video_path)
            os.remove(temp_video_path)
            return Response({'frames_directory': frames_directory}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def process_frames(self, video_path):
        video_capture = cv2.VideoCapture(video_path)
        while True:
            ret, frame = video_capture.read()
            if not ret:
                break
            self.identification_request(frame)
        video_capture.release()

    def identification_request(self,frame):
        _, encoded_frame = cv2.imencode('.jpg', frame)
        url = 'http://172.16.18.47:8881/api/MFace/IdentificationWithDetail?username=rohanizade&password=rohani123zade'
        response = requests.post(url, data=encoded_frame.tobytes())
        print(response.text)
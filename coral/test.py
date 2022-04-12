# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A demo to classify Raspberry Pi camera stream."""
import argparse
import collections
from collections import deque
import common
import io
import numpy as np
import operator
import os
import picamera
import tflite_runtime.interpreter as tflite
import time

from PIL import Image
from PIL import ImageDraw
#from pycoral.adapters import common
from pycoral.utils.edgetpu import make_interpreter

_NUM_KEYPOINTS = 17

def get_output(interpreter, top_k, score_threshold):
    pass

def main():
    default_model_dir = './models'
    default_model = 'movenet_single_pose_lightning_ptq_edgetpu.tflite'
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', help='.tflite model path', default=os.path.join(default_model_dir,default_model))

    args = parser.parse_args()

    interpreter = make_interpreter(args.model)
    interpreter.allocate_tensors()

    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        camera.framerate = 30
        camera.annotate_text_size = 20
        width, height, channels = common.input_image_size(interpreter)
        camera.start_preview()
        try:
            stream = io.BytesIO()
            fps = deque(maxlen=20)
            fps.append(time.time())
            for foo in camera.capture_continuous(stream,
                                                 format='rgb',
                                                 use_video_port=True,
                                                 resize=(width, height)):
                stream.truncate()
                stream.seek(0)
                input = np.frombuffer(stream.getvalue(), dtype=np.uint8)
                start_ms = time.time()
                common.input_tensor(interpreter)[:,:] = np.reshape(input, common.input_image_size(interpreter))
                
                interpreter.invoke()

                pose = common.output_tensor(interpreter, 0).copy().reshape(_NUM_KEYPOINTS, 3)
                print(pose)


                '''
                results = get_output(interpreter, top_k=3, score_threshold=0)
                inference_ms = (time.time() - start_ms)*1000.0
                fps.append(time.time())
                fps_ms = len(fps)/(fps[-1] - fps[0])
                camera.annotate_text = 'Inference: {:5.2f}ms FPS: {:3.1f}'.format(inference_ms, fps_ms)
                for result in results:
                   camera.annotate_text += '\n{:.0f}% {}'.format(100*result[1], labels[result[0]])
                print(camera.annotate_text)
                '''
        finally:
            camera.stop_preview()


if __name__ == '__main__':
    main()

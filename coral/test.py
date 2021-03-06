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
doPreview = True
useTpu = True

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--tpu', help='use coral tpu', default=0)
    parser.add_argument('--preview', help='show video preview', default=0)
    args = parser.parse_args()

    useTpu = bool(int(args.tpu))
    doPreview = bool(int(args.preview))

    modelDir = '../models'
    modelFile = 'movenet_single_pose_lightning_ptq_edgetpu.tflite'
    if (useTpu == False):
        modelFile = 'movenet_single_pose_lightning_ptq.tflite'
    modelUrl = os.path.join(modelDir, modelFile)

    interpreter = make_interpreter(modelUrl)
    interpreter.allocate_tensors()

    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        camera.framerate = 30
        camera.annotate_text_size = 20
        width, height, channels = common.input_image_size(interpreter)

        if (doPreview == True):
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

        finally:
            if (doPreview == True):
                camera.stop_preview()


if __name__ == '__main__':
    main()

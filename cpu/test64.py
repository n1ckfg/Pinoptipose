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
from picamera2.picamera2 import *
import tflite_runtime.interpreter as tflite
import time

from PIL import Image
from PIL import ImageDraw
from common import make_interpreter

_NUM_KEYPOINTS = 17
doPreview = True
useTpu = True

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--preview', help='show video preview', default=0)
    args = parser.parse_args()

    doPreview = bool(int(args.preview))

    modelDir = '../models'
    modelFile = 'movenet_single_pose_lightning_ptq.tflite'
    modelUrl = os.path.join(modelDir, modelFile)

    interpreter = make_interpreter(modelUrl)
    interpreter.allocate_tensors()

    with Picamera2() as camera:
        width, height, channels = common.input_image_size(interpreter)
        
        camera.configure(camera.preview_configuration(main={"format": 'RGB888', "size": (640, 480)}))

        if (doPreview == True):
            camera.start_preview()
        
        camera.start()
        
        while True:
            try:
                input = camera.capture_array()

                common.input_tensor(interpreter)[:,:] = np.resize(input, common.input_image_size(interpreter))

                interpreter.invoke()

                pose = common.output_tensor(interpreter, 0).copy().reshape(_NUM_KEYPOINTS, 3)
                print(pose)

            finally:
                pass


if __name__ == '__main__':
    main()

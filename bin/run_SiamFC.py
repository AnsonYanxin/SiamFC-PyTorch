import numpy as np
import time
from siamfc import SiamFCTracker, config
import cv2
import glob
import os
from tqdm import tqdm


def run_SiamFC(seq, rp, saveimage, seq_idx=0):
    x = seq.init_rect[0]
    y = seq.init_rect[1]
    w = seq.init_rect[2]
    h = seq.init_rect[3]

    # frames = [cv2.cvtColor(cv2.imread(filename), cv2.COLOR_BGR2RGB) for filename in seq.s_frames]
    tic = time.clock()
    # starting tracking
    tracker = SiamFCTracker(config.model_path, config.gpu_id, net=config.arch)
    res = []
    for idx, frame in enumerate(tqdm(seq.s_frames, position=seq_idx % 24)):
        frame = cv2.cvtColor(cv2.imread(frame), cv2.COLOR_BGR2RGB)
        if idx == 0:
            bbox = (x, y, w, h)
            tracker.init(frame, bbox)
            bbox = (bbox[0], bbox[1], bbox[0]+bbox[2], bbox[1]+bbox[3]) # 1-idx
        else: # last frame
            bbox = tracker.update(frame)
        res.append((bbox[0], bbox[1], bbox[2]-bbox[0], bbox[3]-bbox[1])) # 1-idx
    duration = time.clock() - tic
    result = {}
    result['res'] = res
    result['type'] = 'rect'
    result['fps'] = round(seq.len / duration, 3)
    return result


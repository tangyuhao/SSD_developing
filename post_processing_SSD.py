from SSD500 import *
from collections import Counter
import operator
# output clip_info structure:
# [   
#     [
#         {
#             "class": int,
#             "score": value from 0 to 1,
#             "box": [ymin, xmin, ymax, xmax]
#         },

#         {
#             "class": int,
#             "score": value from 0 to 1,
#             "box": [ymin, xmin, ymax, xmax]
#         },

#         {
#             "class": int,
#             "score": value from 0 to 1,
#             "box": [ymin, xmin, ymax, xmax]
#         },
#         ...
#     ],
#     [
#         {
#             "class": int,
#             "score": value from 0 to 1,
#             "box": [ymin, xmin, ymax, xmax]
#         },

#         {
#             "class": int,
#             "score": value from 0 to 1,
#             "box": [ymin, xmin, ymax, xmax]
#         },

#         {
#             "class": int,
#             "score": value from 0 to 1,
#             "box": [ymin, xmin, ymax, xmax]
#         },
#         ...
#     ]
# ]
class_dict = {
    12: "dog",
    15: "person",
    19: "train",
    7: "car",
    9: "chair",
    13: "horse",
    16: "plant",
    2: "bicycle",
    10: "cow",
    3: "bird",
    14: "motorbike",
    4: "boat",
    8: "sheep",
    6: "bus"
}
def get_target(clip_path):
    '''
    return find_target, max_class(int), class_count, clip_info
    '''
    clip_info = get_clip_info(clip_path)
    clip_classes = []
    for frame_info in clip_info:
        frame_classes = []
        for box_info in frame_info:
            if box_info["class"] not in frame_classes:
                frame_classes.append(box_info["class"])
        clip_classes = clip_classes + frame_classes
    # now get all clip_classes
    # count the time of appearance in whole clip for each class
    class_count = dict(Counter(clip_classes).items())
    print(class_count)
    if (len(class_count) > 0):
        max_class = max(class_count, key=class_count.get)
        print("most frequent class: %s" %(class_dict[max_class]))
        return True, max_class, class_count, clip_info
    else:
        return False, None, class_count, clip_info

def get_biggest_class_box(frame_info, traget_class):
    target_boxes = [box_info["box"] for box_info in frame_info if box_info["class"] == traget_class]
    if not target_boxes:
        return {"have_box": False, "biggest_box": None}
    else:
        max_box = [0,0,0,0]
        for box in target_boxes:
            if (box[2] - box[0]) * (box[3] - box[1]) > max_box:
                max_box = box
        return {"have_box": True, "biggest_box": max_box}

if __name__ == "__main__":
    test_clips_filename = "./test.txt"
    f = open(test_clips_filename, "r")
    test_clips = f.read().splitlines()
    test_prefix = "../BF_Segmentation/DAVIS/images/"
    test_folders = []
    for clip in test_clips:
        test_folders.append(os.path.join(test_prefix,clip))
    for clip_path in test_folders:
        have_class ,max_class, class_count, clip_info = get_target(clip_path)
        if (have_class):
            if (max_class in class_dict):
                print(clip_path+":",class_dict[max_class])
            else:
                print(clip_path+":",max_class)
        else:
            print(clip_path+":not found classes")














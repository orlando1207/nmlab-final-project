import os
import os.path as osp
import time
import sys
sys.path.append(os.path.abspath('.') + "/demo/libs/")
from track import *
from segment import *
from recognise import *

import json
IDENTITY_MAP_PATH = "./identity_map.json"
def load_identity_map(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        identity_map = json.load(f)
    return identity_map

def main():
    output_dir = "./output/OutputVideos/"
    os.makedirs(output_dir, exist_ok=True)
    current_time = time.localtime()
    timestamp = time.strftime("%Y_%m_%d_%H_%M_%S", current_time)
    video_save_folder = osp.join(output_dir, timestamp)
    
    save_root = './output/'

    # new added 
    IDENTITY_MAP = load_identity_map(IDENTITY_MAP_PATH)

    gallery_folder_path = "./InputVideos/gallery/"
    probe_folder_path   = "./InputVideos/probe/"
    gallery_video = []
    gallery_feats = {}
    # cnostruct features of the gallery
    for filename in os.listdir(gallery_folder_path):
        if filename.endswith('.mp4'):
            video_path = osp.join(gallery_folder_path, filename)
            gallery_video.append(video_path)
            
    cur_id = 0
    for gallery_video_path in gallery_video:
        # tracking 
        gallery_track_result = track(gallery_video_path, video_save_folder)
        print ()
        print ("===============================")
        print (list(gallery_track_result.keys()))
        print ("===============================")
        print ()
        # segmentation
        gallery_video_name = gallery_video_path.split("/")[-1]
        gallery_video_name = save_root+'/GaitSilhouette/'+gallery_video_name.split(".")[0]
        exist = os.path.exists(gallery_video_name)
        if exist:
            gallery_silhouette = getsil(gallery_video_path, save_root+'/GaitSilhouette/')
        else:
            gallery_silhouette = seg(gallery_video_path, gallery_track_result, save_root+'/GaitSilhouette/')
        gallery_feat = extract_sil(gallery_silhouette, save_root+'/GaitFeatures/')
        
        '''gallery_list_new = []
        for gallery_name, gallery_list in gallery_feat.items():
            for gallery_dict in gallery_list:
                gallery_dict_new = {}
                for gallery_index, gallery_detail in gallery_dict.items():
                    cur_id += 1
                    new_key = f"{cur_id:03d}"
                    gallery_dict_new[new_key] = gallery_detail
                gallery_list_new.append(gallery_dict_new)
        gallery_feat = {gallery_name: gallery_list_new}'''

        print ()
        print ("===============================")
        print (gallery_feat)
        print ("===============================")
        print ()

        # recognition
        if gallery_feats == {}:
            gallery_feats = gallery_feat
        else: 
            gallery_feats.update(gallery_feat)

    probe_video_path = probe_folder_path + "probe_1.mp4"
    # tracking
    probe_track_result  = track(probe_video_path, video_save_folder)
    # segmentation
    probe_video_name  = probe_video_path.split("/")[-1]
    probe_video_name  = save_root+'/GaitSilhouette/'+probe_video_name.split(".")[0]
    exist = os.path.exists(probe_video_name)
    if exist:
        probe_silhouette  = getsil(probe_video_path , save_root+'/GaitSilhouette/')
    else:
        probe_silhouette  = seg(probe_video_path , probe_track_result , save_root+'/GaitSilhouette/')
    
    # recognition
    probe_feat  = extract_sil(probe_silhouette , save_root+'/GaitFeatures/')

    # compare
    gallery_probe_result = compare(probe_feat, gallery_feats)

    for probe_id, result in gallery_probe_result.items():
        if result in IDENTITY_MAP:
            identity_info = IDENTITY_MAP[result]
            print ("=================================")
            print(f"Name: {identity_info['name']}")
            print(f"Department: {identity_info['Department']}")
            print(f"Year in school: {identity_info['Year in school']}")
            print(f"Photo URL: {identity_info['photo_url']}")
            print(f"Comparison Result: {result}")
            print ("=================================")
        else:
            print("=================================")
            print(f"Probe ID: {probe_id} not found in identity map.")
            print("=================================")

    writeresult(gallery_probe_result, probe_video_path, video_save_folder, IDENTITY_MAP)
    # new added 

    '''
    gallery_video_path = "./demo/output/InputVideos/gallery.mp4"
    probe1_video_path  = "./demo/output/InputVideos/probe1.mp4"
    probe2_video_path  = "./demo/output/InputVideos/probe2.mp4"
    probe3_video_path  = "./demo/output/InputVideos/probe3.mp4"
    probe4_video_path  = "./demo/output/InputVideos/probe4.mp4"

    # tracking
    gallery_track_result = track(gallery_video_path, video_save_folder)
    probe1_track_result  = track(probe1_video_path, video_save_folder)
    probe2_track_result  = track(probe2_video_path, video_save_folder)
    probe3_track_result  = track(probe3_video_path, video_save_folder)
    probe4_track_result  = track(probe4_video_path, video_save_folder)

    gallery_video_name = gallery_video_path.split("/")[-1]
    gallery_video_name = save_root+'/GaitSilhouette/'+gallery_video_name.split(".")[0]
    probe1_video_name  = probe1_video_path.split("/")[-1]
    probe1_video_name  = save_root+'/GaitSilhouette/'+probe1_video_name.split(".")[0]
    probe2_video_name  = probe2_video_path.split("/")[-1]
    probe2_video_name  = save_root+'/GaitSilhouette/'+probe2_video_name.split(".")[0]
    probe3_video_name  = probe3_video_path.split("/")[-1]
    probe3_video_name  = save_root+'/GaitSilhouette/'+probe3_video_name.split(".")[0]
    probe4_video_name  = probe4_video_path.split("/")[-1]
    probe4_video_name  = save_root+'/GaitSilhouette/'+probe4_video_name.split(".")[0]
    exist = os.path.exists(gallery_video_name) and os.path.exists(probe1_video_name) \
            and os.path.exists(probe2_video_name) and os.path.exists(probe3_video_name) \
            and os.path.exists(probe4_video_name)
    print(exist)
    if exist:
        gallery_silhouette = getsil(gallery_video_path, save_root+'/GaitSilhouette/')
        probe1_silhouette  = getsil(probe1_video_path , save_root+'/GaitSilhouette/')
        probe2_silhouette  = getsil(probe2_video_path , save_root+'/GaitSilhouette/')
        probe3_silhouette  = getsil(probe3_video_path , save_root+'/GaitSilhouette/')
        probe4_silhouette  = getsil(probe4_video_path , save_root+'/GaitSilhouette/')
    else:
        gallery_silhouette = seg(gallery_video_path, gallery_track_result, save_root+'/GaitSilhouette/')
        probe1_silhouette  = seg(probe1_video_path , probe1_track_result , save_root+'/GaitSilhouette/')
        probe2_silhouette  = seg(probe2_video_path , probe2_track_result , save_root+'/GaitSilhouette/')
        probe3_silhouette  = seg(probe3_video_path , probe3_track_result , save_root+'/GaitSilhouette/')
        probe4_silhouette  = seg(probe4_video_path , probe4_track_result , save_root+'/GaitSilhouette/')

    # recognise
    gallery_feat = extract_sil(gallery_silhouette, save_root+'/GaitFeatures/')
    probe1_feat  = extract_sil(probe1_silhouette , save_root+'/GaitFeatures/')
    probe2_feat  = extract_sil(probe2_silhouette , save_root+'/GaitFeatures/')
    probe3_feat  = extract_sil(probe3_silhouette , save_root+'/GaitFeatures/')
    probe4_feat  = extract_sil(probe4_silhouette , save_root+'/GaitFeatures/')

    gallery_probe1_result = compare(probe1_feat, gallery_feat)
    gallery_probe2_result = compare(probe2_feat, gallery_feat)
    gallery_probe3_result = compare(probe3_feat, gallery_feat)
    gallery_probe4_result = compare(probe4_feat, gallery_feat)

    # write the result back to the video
    writeresult(gallery_probe1_result, probe1_video_path, video_save_folder)
    writeresult(gallery_probe2_result, probe2_video_path, video_save_folder)
    writeresult(gallery_probe3_result, probe3_video_path, video_save_folder)
    writeresult(gallery_probe4_result, probe4_video_path, video_save_folder)
    '''

if __name__ == "__main__":
    main()

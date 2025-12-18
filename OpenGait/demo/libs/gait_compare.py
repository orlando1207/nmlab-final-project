import torch
import numpy as np

def getemb(data):
    return data["inference_feat"]

def computedistence(x, y):
    x_flat = x.flatten()
    y_flat = y.flatten()
    
    x_norm = torch.nn.functional.normalize(x_flat, p=2, dim=0)
    y_norm = torch.nn.functional.normalize(y_flat, p=2, dim=0)
    cosine_sim = torch.sum(x_norm * y_norm)
    # distance = 1.0 - cosine_sim

    cosine_distance = 1.0 - cosine_sim
    # sigmoid(k * (x - center)) >[0,1]
    k = 20.0
    center = 0.028
    scaled_distance = torch.sigmoid(k * (cosine_distance - center))
    distance = scaled_distance

    # distance = torch.sqrt(torch.sum(torch.square(x - y))) / torch.sqrt(torch.tensor(x.numel(), dtype=x.dtype))    
    return distance

def compareid(data, dict, pid, threshold_value):
    probe_name = pid.split("-")[0]
    embs = getemb(data)
    min = threshold_value
    id = None
    dic={}
    for key in dict:
        if key == probe_name:
            continue
        for subject in dict[key]:
            for type in subject:
                for view in subject[type]:
                    value = subject[type][view]
                    distance = computedistence(embs["embeddings"],value)
                    gid = key + "-" + str(type)
                    gid_distance = (gid, distance)
                    dic[gid] = distance
                    if distance.float() < min:
                        id = gid
                        min = distance.float()
    dic_sort= sorted(dic.items(), key=lambda d:d[1], reverse = False)
    if id is None:
        print("############## no id #####################")
    return id, dic_sort


def comparefeat(embs, gallery_feat: dict, pid, threshold_value):
    """Compares the distance between features

    Args:
        embs (Tensor): Embeddings of person with pid
        gallery_feat (dict): Dictionary of features from gallery
        pid (str): The id of person in probe
        threshold_value (int): Threshold
    Returns:
        id (str): The id in gallery
        dic_sort (dict): Recognition result sorting dictionary
    """
    probe_name = pid.split("-")[0]
    min = 2
    id = None
    dic={}
    for key in gallery_feat:
        if key == probe_name:
            continue
        for subject in gallery_feat[key]:
            for type in subject:
                for view in subject[type]:
                    value = subject[type][view]
                    distance = computedistence(embs, value)
                    gid = key + "-" + str(type)
                    gid_distance = (gid, distance)
                    dic[gid] = distance
                    if distance.float() < min:
                        id = gid
                        min = distance.float()
    dic_sort= sorted(dic.items(), key=lambda d:d[1], reverse = False)
    
    # 檢查最佳匹配是否超過閾值
    if id is None:
        print("############## no person detected in probe #####################")
        print(f"distance {min:.4f} exceeds the threshold {threshold_value}")
        return "NOT_IN_DATABASE", dic_sort
    elif min >= threshold_value:
        print(f"############## Best match distance {min:.4f} exceeds threshold {threshold_value} #####################")
        print(f"Top 5 matches: {[(gid, f'{dist.item():.6f}') for gid, dist in dic_sort[:5]]}")
        return "NOT_IN_DATABASE", dic_sort
    
    # 顯示詳細的匹配信息用於調試
    print(f"\n✅ Match found: {id}")
    print(f"   Distance: {min:.6f}")
    print(f"   Top 5 candidates:")
    for idx, (gid, dist) in enumerate(dic_sort[:5], 1):
        print(f"      {idx}. {gid}: {dist.item():.6f}")
    
    return id, dic_sort

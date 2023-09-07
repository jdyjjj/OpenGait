import os
import os.path as osp
import numpy as np
import pdb

ORG_KEYPOINTS = {
    'nose'          :0,
    'left_eye'      :1,
    'right_eye'     :2,
    'left_ear'      :3,
    'right_ear'     :4,
    'left_shoulder' :5,
    'right_shoulder':6,
    'left_elbow'    :7,
    'right_elbow'   :8,
    'left_wrist'    :9,
    'right_wrist'   :10,
    'left_hip'      :11,
    'right_hip'     :12,
    'left_knee'     :13,
    'right_knee'    :14,
    'left_ankle'    :15,
    'right_ankle'   :16,
}

NEW_KEYPOINTS = {
    0: 'right_shoulder',
    1: 'right_elbow',
    2: 'right_knee',
    3: 'right_hip',
    4: 'left_elbow',
    5: 'left_knee',
    6: 'left_shoulder',
    7: 'right_wrist',
    8: 'right_ankle',
    9: 'left_hip',
    10: 'left_wrist',
    11: 'left_ankle',
}

def get_index_mapping():
    index_mapping = {}
    for _key in NEW_KEYPOINTS.keys():
        map_index = ORG_KEYPOINTS[NEW_KEYPOINTS[_key]]
        index_mapping[_key] = map_index
    return index_mapping

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='OpenGait dataset pretreatment module.')
    parser.add_argument('-i', '--input_path', default='', type=str, help='Root path of raw dataset.')
    parser.add_argument('-o', '--output_path', default='', type=str, help='Output path of pickled dataset.')
    args = parser.parse_args()

    index_mapping = get_index_mapping()
    data_path = args.input_path
    des_path = args.output_path

    id_list = sorted(os.listdir(data_path))
    for _id in id_list:
        type_list = sorted(os.listdir(osp.join(data_path, _id)))
        for _type in type_list:
            view_list = sorted(os.listdir(osp.join(data_path, _id, _type)))
            for _view in view_list:
                seq_info = [_id, _type, _view]
                seq_dir = osp.join(data_path, *seq_info)
                des_dir = osp.join(des_path, *seq_info)
                if osp.exists(des_dir) is False:
                    os.makedirs(des_dir)

                keypoints_list = os.listdir(seq_dir)
                
                for _keypoints in keypoints_list:
                    keypoints_data = np.load(open(osp.join(seq_dir, _keypoints), 'rb'))
                    mapped_keypoints = np.zeros((12, 3))
                    for i in range(mapped_keypoints.shape[0]):
                        mapped_keypoints[i] = keypoints_data[index_mapping[i]]
                    save_path = osp.join(des_dir, _keypoints)
                    np.save(save_path, mapped_keypoints)
            print("FINISHED: " + "-".join(seq_info))
                

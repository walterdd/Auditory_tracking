import cv2

from .bounding_boxes import BoundingBox


"""
Visualized bounding boxes:
    color: blue / red  (man / woman)
    person id
    predicted age
    border: bold / thin (interested / bored)
"""


def draw_bbox(img, bbox, male_gender, interest):
    color = (255, 0, 0) if male_gender else (0, 0, 255)
    cv2.rectangle(img, (int(bbox.x), int(bbox.y)), (int(bbox.right), int(bbox.bottom)), color, 1 + 2 * interest)
    return img


def put_info(img, bbox, person_id, age):
    string = 'id_%d age=%d' % (person_id, int(age))
    ltopx = int(bbox.x)
    ltopy = int(bbox.y)
    cv2.putText(img, string, (ltopx, ltopy), 1, 1, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(img, string, (ltopx - 1, ltopy - 1), 1, 1, (255, 255, 255), 1, cv2.LINE_AA)
    return img


def draw_bboxes(img, df):
    for person_id in df['person_id'].values:
        bbox = BoundingBox(*df[['x', 'y', 'w', 'h']][df['person_id'] == person_id].values[0])
        male_gender = df['gender'][df['person_id'] == person_id].values[0] == 'Male'
        interest = df['interest'][df['person_id'] == person_id].values[0]
        img = draw_bbox(img, bbox, male_gender, interest)

    for person_id in df['person_id'].values:
        bbox = BoundingBox(*df[['x', 'y', 'w', 'h']][df['person_id'] == person_id].values[0])
        age = df['age'][df['person_id'] == person_id].values[0]
        img = put_info(img, bbox, person_id, age)

    return img


def visualize(people_df, input_videofile, output_videofile, frames_limit, detection_step):
    input_video = cv2.VideoCapture(input_videofile)
    ret, frame = input_video.read()
    cur_frame_num = 0

    height, width = frame.shape[0], frame.shape[1]
    fourcc = cv2.VideoWriter_fourcc(*'XVID')

    output_video = cv2.VideoWriter(output_videofile, fourcc, 25, (width, height))

    while cur_frame_num < frames_limit:
        ret, frame = input_video.read()
        df_slice = people_df[people_df['frame'] == cur_frame_num]
        output_video.write(draw_bboxes(frame, df_slice))
        cur_frame_num += 1

    output_video.release()
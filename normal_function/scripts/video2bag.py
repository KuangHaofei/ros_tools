#!/usr/bin/env python
import rospy
import roslib
import rosbag

roslib.load_manifest('sensor_msgs')
from sensor_msgs.msg import Image

from cv_bridge import CvBridge
import cv2
import tqdm

TOPIC = 'camera/image_raw'


def create_video_bag(video_path, bag_name):
    """Creates a bag file with a video file
    """
    bag = rosbag.Bag(bag_name, 'w')
    cap = cv2.VideoCapture(video_path)
    cb = CvBridge()
    prop_fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if prop_fps != prop_fps or prop_fps <= 1e-2:
        print("Warning: can't get FPS. Assuming 24.")
        prop_fps = 24

    pbar = tqdm.tqdm(total = frame_count)
    i = 1
    ret = True
    while ret:
        pbar.update(i)
        ret, frame = cap.read()
        if not ret:
            break
        stamp = rospy.rostime.Time.now()
        image = cb.cv2_to_imgmsg(frame, encoding='bgr8')
        image.header.stamp = stamp
        image.header.frame_id = "camera"
        bag.write(TOPIC, image, stamp)

    cap.release()
    bag.close()


if __name__ == "__main__":
    rospy.init_node("video2bag", anonymous=True)

    video_path = rospy.get_param("/video2bag/path")
    bag_name = rospy.get_param("/video2bag/bag")

    if video_path and bag_name:
        create_video_bag(video_path, bag_name)
        print("Finished!")
    else:
        print("Usage: roslaunch normal_function video2bag.launch "
              "video_path:={YOUR VIDEO PATH}  bag_name:={YOUR BAG FILE NAME}")
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
from ollama import Client
import time  # Import time to measure response times


def image_callback(msg):
    # transform the image to cv2 format
    bridge = CvBridge()
    cv_image = bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
    
    # image preprocessing
    resized_image = cv2.resize(cv_image, (224, 224))
    
    # send the image to the multimodel
    _, img_encoded = cv2.imencode('.jpg', resized_image)
    img_bytes = img_encoded.tobytes()

    client = Client(host='http://10.64.86.215:3060')

    # Record the timestamp before sending the request
    start_time = time.time()

    response = client.generate(model='llava', prompt=
    'The figure are from gazebo sim env, describe the objeuct in fig in a sentence:', images=[img_bytes], options={'temperature':0,
                                     'num_predict':500,}
)
    
    # Record the timestamp after receiving the response
    end_time = time.time()

    # Calculate the response time in seconds
    response_time = end_time - start_time

    # print(response['response'], end='\n\n', flush=True)
    # print(f"{response['response']}\nResponse Speed is  {(response['eval_count'] / response['eval_duration']) * 10**9} token/sec")
    print(f"Response: {response['response']}")
    print(f"Response Time: {response_time:.3f} seconds")


def main():
    rospy.init_node('llava_node', anonymous=True)
    rospy.Subscriber('/robot2/camera_d435/color/image_raw', Image, image_callback)
    
    # set the rate of the node
    rate = rospy.Rate(0.5) 
    
    while not rospy.is_shutdown():
        rate.sleep()

if __name__ == '__main__':
    main()
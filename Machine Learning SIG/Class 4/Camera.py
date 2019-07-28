import cv2
import os

x1 , x2 = 20, 620
y1 , y2 = 20, 460

def get_cam_image(capture):
    _, image = capture.read()
    return image

def release_cam(capture):
    capture.release()
    cv2.destroyAllWindows()

def display_cam(image):
    cv2.imshow("Capture", image)
    cv2.waitKey(1)

def take_pictures():
    img_counter = 0
    camera = cv2.VideoCapture(0)
    cv2.namedWindow("camera")
    while True:
        _, image = camera.read()
        # To draw a rectangle
        cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0, 0), 2)
        cv2.imshow("camera", image)
        if not _: break
        key = cv2.waitKey(1)
        if key % 256 == 27:
            # ESC pressed - exit
            break
        if key % 256 == 32:
            # SPACE pressed - save the frame
            img_name = "Images/opencv_frame_{}.png".format(img_counter)
            cv2.imwrite(img_name, image)
            print("{} written!".format(img_name))
            img_counter += 1
    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    take_pictures()

import cv2
import time

from reference.get_background import get_background

def detect(source, frame1) :
    camera = source # 기본카메라
    
    cap = cv2.VideoCapture(camera)
    # get the video frame height and width
    frame_width = int(cap.get(3))
    """     frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    save_name = f"outputs"
    # define codec and create VideoWriter object
    out = cv2.VideoWriter(
        save_name,
        cv2.VideoWriter_fourcc(*'mp4v'), 10, 
        (frame_width, frame_height)
    ) """
    
    #start = time.time()

    # get the background model
    background = get_background(camera)
    # convert the background model to grayscale format
    background = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)

    #print(time.time()-start)

    frame_count = 0
    consecutive_frame = frame1

    left = 0
    right = 0
    center = 0

    while (cap.isOpened()):

        ret, frame = cap.read()
        
        if ret == True:
            frame_count += 1
            # print(frame_count)
            orig_frame = frame.copy()
            # IMPORTANT STEP: convert the frame to grayscale first
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if frame_count % consecutive_frame == 0 or frame_count == 1:
                frame_diff_list = []

            # find the difference between current frame and base frame
            frame_diff = cv2.absdiff(gray, background)
            # thresholding to convert the frame to binary
            ret, thres = cv2.threshold(frame_diff, 50, 255, cv2.THRESH_BINARY)
            # dilate the frame a bit to get some more white area...
            # ... makes the detection of contours a bit easier
            dilate_frame = cv2.dilate(thres, None, iterations=2)
            # append the final result into the `frame_diff_list`
            frame_diff_list.append(dilate_frame)
            # if we have reached `consecutive_frame` number of frames
            if len(frame_diff_list) == consecutive_frame:
                # add all the frames in the `frame_diff_list`
                sum_frames = sum(frame_diff_list)
                # find the contours around the white segmented areas
                contours, hierarchy = cv2.findContours(sum_frames, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                # draw the contours, not strictly necessary
                for i, cnt in enumerate(contours):
                    cv2.drawContours(frame, contours, i, (0, 0, 255), 3)
                for contour in contours:
                    # continue through the loop if contour area is less than 500...
                    # ... helps in removing noise detection
                    if cv2.contourArea(contour) < 500:
                        continue
                    # get the xmin, ymin, width, and height coordinates from the contours
                    (x, y, w, h) = cv2.boundingRect(contour)
                    
                    # draw the bounding boxes
                    cv2.rectangle(orig_frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    
                    if frame_width/3 > x+w :
                       
                        left = left + 1
                    elif 2*frame_width/3 > x+w:
                        
                        center = center + 1
                    else :
                        
                        right = right + 1

                if __name__ == "__main__" :
                    cv2.imshow('Detected Objects', orig_frame)
                    # out.write(orig_frame)

                if cv2.waitKey(100) & 0xFF == ord('q'):
                    break

                
        
        else:
            break
    cap.release()
    cv2.destroyAllWindows()


    if max(left,center,right) == left :
        
        print("left") 
        return "left"
        
    elif max(left,center,right) == center :
        
        print("center")
        return "center"
    elif max(left,center,right) == right :
        
        print("right")
        return "right"
    else :
        print("normal")
        return "normal"



if __name__ == "__main__" :
    detect('/Users/jh/Code/Object_detect-OpenCV/sample.mp4',4)

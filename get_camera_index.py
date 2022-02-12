# import the opencv library
import cv2, sys

args = sys.argv
if len(args) <= 1:
    print("Invalid")
    print("please give an index to test (start at 0)")
    exit()

# define a video capture object
vid = cv2.VideoCapture(int(args[1]))

while(True):
    ret, frame = vid.read()
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vid.release()
cv2.destroyAllWindows()
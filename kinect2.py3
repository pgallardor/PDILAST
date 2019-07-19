import cv2
import numpy as np
import math
import random

HEIGHT = 240
WIDTH = 320
FRAME_WINDOW = 20


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
# Create old frame
_, frame = cap.read()
old_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# Lucas kanade params
lk_params = dict(winSize = (20, 20),
                 maxLevel = 5,
                 criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
# Mouse function
def select_point(event, x, y, flags, params):
    global point, point_selected, old_points
    if event == cv2.EVENT_LBUTTONDOWN:
        point = (x, y)
        point_selected = True
        old_points = np.array([[x, y]], dtype=np.float32)

cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame", select_point)
point_selected = False 
point = ()
old_points = np.array([[]])

#Simon behavior
level = 1
seq = [random.randint(0, 3)]
playerSeq = -1
frameCount = [0, 0, 0, 0]
showingLevel = True
roundWon = False
iseq = 0
marking = False

while True:
	_, frame = cap.read()
	#gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray_frame = frame[:,:,0]
	if point_selected is True:
		#cv2.circle(frame, point, 5, (0, 0, 255), 2)
		new_points, status, error = cv2.calcOpticalFlowPyrLK(old_gray, gray_frame, old_points, None, **lk_params)
		old_gray = gray_frame.copy()
		old_points = new_points
		x, y = new_points.ravel()
		cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

		cv2.circle(frame, (160, 60), 20, (0, 0, 255), -1)
		cv2.circle(frame, (160, 180), 20, (0, 255, 0), -1)
		cv2.circle(frame, (80, 120), 20, (255, 0, 0), -1)
		cv2.circle(frame, (240, 120), 20, (0, 255, 255), -1)

		if roundWon:
			roundWon = False
			showingLevel = True
			playerSeq = []
			seq.append(random.randint(0, 3))
			iseq = 0

		if showingLevel:
			print("SHOWING LEVEL")
			if seq[iseq] == 0:
				cv2.circle(frame, (160, 60), 30, (255, 255, 255), 20)
			elif seq[iseq] == 1:
				cv2.circle(frame, (160, 180), 30, (255, 255, 255), 20)
			elif seq[iseq] == 2:
				cv2.circle(frame, (80, 120), 30, (255, 255, 255), 20)
			elif seq[iseq] == 3:
				cv2.circle(frame, (240, 120), 30, (255, 255, 255), 20)

			iseq += 1
			if iseq >= len(seq):
				print("LEVEL SHOWN")
				showingLevel = False
				iseq = 0

		#game logeec
		else:
			print(seq)
			if ((x - 160)**2 + (y - 60)**2 <= 400):
				frameCount[0] += 1
				if (frameCount[0] >= FRAME_WINDOW):
					cv2.circle(frame, (160, 60), 30, (255, 255, 255), 30)
					marking = True
					playerSeq = 0
					frameCount[0] = 0

			else: frameCount[0] = 0


			if ((x - 160)**2 + (y - 180)**2 <= 400):
				frameCount[1] += 1
				if (frameCount[1] >= FRAME_WINDOW):
					cv2.circle(frame, (160, 180), 30, (255, 255, 255), 30)
					marking = True
					playerSeq = 1
					frameCount[1] = 0

			else: frameCount[1] = 0

			if ((x - 80)**2 + (y - 120)**2 <= 400):
				frameCount[2] += 1
				if (frameCount[2] >= FRAME_WINDOW):
					cv2.circle(frame, (80, 120), 30, (255, 255, 255), 30)
					marking = True
					playerSeq = 2
					frameCount[2] = 0

			else: frameCount[2] = 0

			if ((x - 240)**2 + (y - 120)**2 <= 400):
				frameCount[3] += 1
				if (frameCount[3] >= FRAME_WINDOW):
					cv2.circle(frame, (240, 120), 30, (255, 255, 255), 30)
					marking = True
					playerSeq = 3
					frameCount[3] = 0

			else: frameCount[3] = 0

			if (playerSeq != -1):
				if (playerSeq == seq[iseq]):
					iseq += 1
					if (iseq >= len(seq)):
						roundWon = True
						iseq = 0
				else:
					iseq = 0
					showingLevel = True
				playerSeq = -1


	cv2.imshow("Frame", frame)
	if showingLevel is True and point_selected is True:
		cv2.waitKey(500)
	if marking is True:
		cv2.waitKey(300)
		marking = False
	key = cv2.waitKey(16)
	if key == 27:
		break

cap.release()
cv2.destroyAllWindows()
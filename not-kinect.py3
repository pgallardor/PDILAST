import cv2
import numpy as np
import math

HEIGHT = 240
WIDTH = 320
FRAME_WINDOW = 10

#launch logic
x1, y1 = -1,-1
n_frame = 0

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

#Ball behavior
ball_x = int(WIDTH / 2)
ball_y = int(HEIGHT / 2)
ball_radius = 20
ball_speedX = 0
ball_speedY = 0
ball_accelX = 0
MAX_SPEED = 20
isBallOnMovement = False
wasOnPoint = False

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

		if ((x - ball_x)**2 + (y - ball_y)**2 <= ball_radius**2):
			ball_x = x
			ball_y = y
			isBallOnMovement = True
			if wasOnPoint:
				n_frame += 1;
				if n_frame >= FRAME_WINDOW:
					print('start', (x1, y1), ' end', (x, y))
					n_frame = 0
					dist = math.sqrt((x - x1)**2 + (y - y1)**2)
					print(dist)
					if dist >= 40:
						ball_speedX = np.sign(x - x1) * dist / 10
						ball_x += ball_speedX
						ball_y += ball_speedY
						print('speed ', (ball_speedX, ball_speedY))
					x1, y1 = x, y

			else:
				wasOnPoint = True
				x1, y1 = x, y

		else:
			wasOnPoint = False
			n_frame = 0
			x1, y1 = -1, -1
			if isBallOnMovement:
				ball_x += ball_speedX
				ball_y += ball_speedY

	if n_frame >= FRAME_WINDOW:
		n_frame = 0

	ball_speedX *= 0.85
	ball_speedY += 2 #gravity

	if (ball_speedY >= MAX_SPEED):
		ball_speedY = MAX_SPEED

	if (ball_y <= 0):
		ball_y = 0

	if (ball_x <= 0):
		ball_x = 0

	if (ball_y >= HEIGHT - ball_radius):
		ball_y = HEIGHT - ball_radius

	if (ball_x >= WIDTH - ball_radius):
		ball_x = WIDTH - ball_radius

	cv2.circle(frame, (int(ball_x), int(ball_y)), ball_radius, (255,0,0), -1)
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(16)
	if key == 27:
		break

cap.release()
cv2.destroyAllWindows()
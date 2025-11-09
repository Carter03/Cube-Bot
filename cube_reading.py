import numpy as np
import cv2

cam = cv2.VideoCapture(0)
while cv2.waitKey(30) != ord('q'):
    # cv2.imshow('', cam.read()[1])

    # img = cv2.imread('cube.jpg')
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    corners = cv2.goodFeaturesToTrack(
        gray,
        maxCorners=50,
        qualityLevel=0.01,
        minDistance=10,
        blockSize=3,
        useHarrisDetector=True,
        k=0.04
    )

    corners = np.intp(corners)  # Convert to integer coords
    points = []
    for corner in corners:
        x, y = corner.ravel()
        cv2.circle(img, (x, y), radius=3, color=(0, 255, 0), thickness=-1)
        points.append([x, y])
    points = np.array(points)
    cv2.imshow('', img)

# import numpy as np

import numpy as np

def best_outer_square(points, n_iter=500, tol=2.0, size_weight=0.1):
    pts = np.array(points)
    best_square = None
    best_score = -np.inf
    
    for _ in range(n_iter):
        i, j = np.random.choice(len(pts), 2, replace=False)
        p1, p2 = pts[i], pts[j]
        if (min(abs(p1[0] - p2[0]), abs(p1[1] - p2[1])) > 35):
            continue
        side = np.linalg.norm(p2 - p1)
        if side < 5:  # skip tiny squares
            continue

        # direction and perpendicular
        d = (p2 - p1) / side
        perp = np.array([-d[1], d[0]])

        for sgn in [1, -1]:
            p3 = p1 + sgn * perp * side
            p4 = p2 + sgn * perp * side
            square = np.array([p1, p2, p4, p3])

            # distances of all points to nearest edge
            edges = [(square[k], square[(k+1)%4]) for k in range(4)]
            all_dists = []
            for pt in pts:
                dists = []
                for a,b in edges:
                    ap, ab = pt - a, b - a
                    proj = np.clip(np.dot(ap, ab)/np.dot(ab, ab), 0, 1)
                    closest = a + proj*ab
                    dists.append(np.linalg.norm(pt - closest))
                all_dists.append(min(dists))
            all_dists = np.array(all_dists)
            if (all_dists[all_dists<2].sum() < 5):
                continue
            if max(square[i][0] for i in range(4)) > img.shape[0] or max(square[i][1] for i in range(1)) > img.shape[1]:
                continue
            if any(square[i][j] < 0 for i in range(4) for j in range(1)):
                continue
            score = (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 

            if score > best_score:
                best_score = score
                best_square = square
    p1 = best_square[0]
    p2 = best_square[1]
    print(min(p1[0] - p2[0], p1[1] - p2[1]))
    return best_square, best_score



sqr, inliers = best_outer_square(points)
# sqr = [int(i) for i in sqr]

print(sqr)
# cv2.rectangle(img, tuple(int(i) for i in sqr[0]), tuple(int(i) for i in sqr[2]), (255,0,0), 1
for j in range(4):
    cv2.circle(img, tuple(int(i) for i in sqr[j]), 5, (255, 0, 0), 4)

cv2.imshow('test', img)
cv2.waitKey(0)

import cv2
import numpy as np
import pickle

class ImageProcessor:
    def __init__(self):
        self.face_corners = None
        self.color_bounds = {
            'W': [ { 'lower': np.array([0, 0, 200]), 
                    'upper': np.array([179, 50, 255]) } ],

            'Y': [ { 'lower': np.array([20, 100, 100]), 
                    'upper': np.array([40, 255, 255]) } ],

            'G': [ { 'lower': np.array([40, 100, 100]), 
                    'upper': np.array([80, 255, 255]) } ],

            'B': [ { 'lower': np.array([100, 100, 100]), 
                    'upper': np.array([140, 255, 255]) } ],

            'O': [ { 'lower': np.array([5, 100, 100]),
                    'upper': np.array([20, 255, 255]) } ],

            'R': [ { 'lower': np.array([0, 50, 100]), 
                    'upper': np.array([5, 255, 255]) },
                   { 'lower': np.array([145, 50, 100]), 
                    'upper': np.array([179, 255, 255]) } ]
        }
    
    def from_file(self, fp):
        frame = cv2.imread(fp)
        return frame
    
    def export_to(self, fp):
        with open(fp, 'wb') as f:
            pickle.dump(self.face_corners, f)
    
    def import_from(self, fp):
        with open(fp, 'rb') as f:
            self.face_corners = pickle.load(f)
    
    def select_corners(self, img_base):
        annotated_base = img_base.copy()
        corners = []

        def mouse_click(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                corners.append((x,y))
                cv2.circle(annotated_base, (x,y), 5, (0,0,255), 3)
        
        
        order_txts = ('UL', 'UR', 'LR', 'LL')
        for txt_i, txt in enumerate(order_txts):
            img = annotated_base.copy()
            cv2.putText(img, txt, (0,0), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 1)
            while len(corners) != txt_i+1:
                cv2.imshow('CORNER SELECTION', img)
                cv2.setMouseCallback('CORNER SELECTION', mouse_click)
                cv2.waitKey(30)
        self.face_corners = np.float32(corners)

    def color_of(self, hsv):
        for clr, ranges in self.color_bounds.items():
            for range in ranges:
                if all(hsv >= range['lower']) and all(hsv < range['upper']):
                    return clr
        return None

    def calc_colors(self, img_base):
        if self.face_corners is None:
            raise 'Must select_corners before getting colors'
        
        square = np.float32([[0,0],[200,0],[200,200],[0,200]])
        M = cv2.getPerspectiveTransform(self.face_corners, square)
        cube_face = cv2.warpPerspective(img_base, M, (200,200))

        INSET = 10
        BLOCK_SIZE = cube_face.shape[0] // 3  # 200 // 3 = 66

        colors_arr = np.zeros((3, 3, 3), dtype=np.float32)
        cube_face_hsv = cv2.cvtColor(cube_face, cv2.COLOR_BGR2HSV)

        for i in range(3):
            for j in range(3):
                start_x = i * BLOCK_SIZE
                end_x = (i + 1) * BLOCK_SIZE
                start_y = j * BLOCK_SIZE
                end_y = (j + 1) * BLOCK_SIZE

                sample_start_x = start_x + INSET
                sample_end_x = end_x - INSET
                sample_start_y = start_y + INSET
                sample_end_y = end_y - INSET
                
                mean_color = cube_face_hsv[
                    sample_start_x:sample_end_x, 
                    sample_start_y:sample_end_y
                ].mean(axis=(0, 1))

                colors_arr[i, j] = mean_color
        
        clr_names = [[self.color_of(colors_arr[j, i]) for i in range(3)] for j in range(3)]
        return clr_names
    
class StateFinder:
    def __init__(self, encoding_scheme):
        # IMAGE ORDER SETUP
        # 
        # L' R
        # L  R'
        # F  B'
        # F' B
        # F  L' R  F' B
        # B' L  R' F  B'
        # F2 B2
        # L2 R2


        # NORMALIZED FORMAT
        # [8] == [BR, MR, UR, TM, ... (counterclockwise)]
        # [[W 8]  [G 8]  [R 8]  [B 8]  [O 8]  [Y 8]]

        # TRANSLATION SCHEME
        self.scheme = [[[(0, 4), (0, 3), (0, 2)],
                   [(0, 5), (-1, -1), (0, 1)],
                   [(0, 6), (0, 7), (0, 0)]],
                   [[(1, 4), (-1, -1), (1, 2)],
                   [(1, 5), (-1, -1), (1, 1)],
                   [(1, 6), (-1, -1), (1, 0)]],
                   [[(3, 0), (-1, -1), (3, 6)],
                   [(3, 1), (-1, -1), (3, 5)],
                   [(3, 2), (-1, -1), (3, 4)]],
                   [[(4, 6), (4, 5), (4, 4)],
                   [(-1, -1), (-1, -1), (-1, -1)],
                   [(4, 0), (4, 1), (4, 2)]],
                   [[(2, 2), (2, 1), (2, 0)],
                   [(-1, -1), (-1, -1), (-1, -1)],
                   [(2, 4), (2, 5), (2, 6)]],
                   [[(-1, -1), (2, 3), (-1, -1)],
                   [(1, 7), (-1, -1), (1, 3)],
                   [(-1, -1), (2, 7), (-1, -1)]],
                   [[(-1, -1), (4, 7), (-1, -1)],
                   [(3, 7), (-1, -1), (3, 3)],
                   [(-1, -1), (4, 3), (-1, -1)]],
                   [[(5, 0), (5, 7), (5, 6)],
                   [(-1, -1), (-1, -1), (-1, -1)],
                   [(5, 2), (5, 3), (5, 4)]],
                   [[(5, 4), (-1, -1), (5, 2)],
                   [(5, 5), (-1, -1), (5, 1)],
                   [(5, 6), (-1, -1), (5, 0)]],
                   ]

        # self.scheme = encoding_scheme

    def from_colors(self, color_arr):
        # color_arr
        # [[['C', 'C', 'C'], [['C', 'C', 'C'], [['C', 'C', 'C'],
        #   ['C', 'C', 'C'],  ['C', 'C', 'C'],  ['C', 'C', 'C'],
        #   ['C', 'C', 'C']]  ['C', 'C', 'C']]  ['C', 'C', 'C']]   ... ]

        for side in range(6):
            


    
if __name__ == '__main__':
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    frame = cv2.resize(frame, (818, 610))
    ip = ImageProcessor()
    ip.select_corners(frame)
    ip.calc_colors(frame)

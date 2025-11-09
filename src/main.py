import sys
import os.path
from bt import SerialReceiver
from manual_reading import ImageProcessor

IMG_PATH = "imgs"
DAT_PATH = "data"

comms = SerialReceiver("COM7", 115200, IMG_PATH)
processor = ImageProcessor()

def config():
    comms.transmit_config()
    comms.receive_imgs()
    frame = processor.from_file(f"{IMG_PATH}/CFG_0.jpeg")
    processor.select_corners(frame)
    processor.export_to(f"{DAT_PATH}/corners.pkl")

def main():
    if not os.path.isfile(f"{DAT_PATH}/corners.pkl"):
        print("Error: Must config before running.")
        return

    processor.import_from(f"{DAT_PATH}/corners.pkl")
    comms.transmit_start()
    comms.receive_imgs()
    

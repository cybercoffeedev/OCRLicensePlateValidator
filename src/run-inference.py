import cv2 as cv
import easyocr as ocr
import threading

# Global variables
font = cv.FONT_HERSHEY_SIMPLEX
font_size = 1
font_weight = 2

def Display():
    global last_frame
    global put_data
    while True:

    # Capture frame-by-frame
        _, frame = cap.read()
        last_frame = frame.copy()

        # Show detected licence plates
        for idx, (entry, value) in enumerate(put_data):
            # Check for valid entry
            color = (255, 0, 0)
            if value:
                entry = f"Valid licence plate: {entry}"
                color = (0, 255, 0)
            else:
                entry = f"Invalid entry: {entry}"
                color = (0, 0, 255)

            # Print the text
            txt_size = cv.getTextSize(entry, font, font_size, font_weight)[0]
            cv.putText(frame, entry,
                        (frame.shape[1] - txt_size[0],
                        frame.shape[0] - (frame.shape[0] - txt_size[1] * (idx + 1))),
                        font, font_size, color, font_weight)
        cv.imshow('Model inference', frame)

        # Exit the program if user pressed ESC key
        if cv.waitKey(1) == 27:
            cap.release()
            break

def ProcessFrame():
    global last_frame
    global put_data

    # Run the OCR Inference on the last captured frame
    while cap.isOpened():
        if last_frame is not None:
            frame = last_frame
            res = ' '.join(reader.readtext(frame, detail=0)).upper()
            put_data.clear()

            # Validate the processed text
            for entry in whitelist:
                element = entry.split()
                if (element[0] in res) and (element[-1] in res):
                    put_data.append([entry, True])
            if put_data == [] and len(res) > 0:
                put_data.append([res, False])

# Define the global variables to share between threads
global last_frame
global put_data
last_frame = None
put_data = []

# Example valid licence plates
whitelist = [
    "AAA OOAA",
    "FZA 20TH",
    "GO BART",
    "KGW 7JS5",
    "WX 66666",
    "S 29N",
    "UA 03271",
    "ERA 75TM",
    "ERA 81TL"
]

# Begin capturing video from the webcam
cap = cv.VideoCapture(0)
reader = ocr.Reader(['en'])

# Separate display and inference on two threads to avoid low fps
main_thread = threading.Thread(target=Display)
inference_thread = threading.Thread(target=ProcessFrame)

# Start the threads
main_thread.start()
inference_thread.start()

# Exit the program
cv.destroyAllWindows()

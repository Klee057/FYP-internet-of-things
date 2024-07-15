#! /usr/bin/python

# import the necessary packages
from imutils import paths
import numpy as np
import face_recognition
#import argparse
import pickle
import cv2
import os
import firebase_admin
from firebase_admin import credentials, storage

# our images are located in the dataset folder
print("[INFO] start processing faces...")
imagePaths = list(paths.list_images("dataset"))

# initialize the list of known encodings and known names
knownEncodings =  []
knownNames = []

cred = credentials.Certificate('/home/pi/project/facial-recognition2/rpi-key.json')

firebase_admin.initialize_app(cred, {
    'storageBucket': 'rpiapp-17f72.appspot.com'
    })



# def encode_face(image, name):
# 	rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# 	boxes = face_recognition.face_locations(rgb, model = "hog")
# 		# compute the facial embedding for the face
# 	encodings = face_recognition.face_encodings(rgb, boxes)
# 	# loop over the encodings
# 	for encoding in encodings:
# 		# add each encoding + name to our set of known names and
# 		# encodings
# 		knownEncodings.append(encoding)
# 		knownNames.append(name)


def read_all_images_from_folder(folder_path):
	bucket = storage.bucket()
	blobs = bucket.list_blobs(prefix=folder_path)
	for blob in blobs:
		# Get the blob name (remove the folder path)
		blob_name = os.path.basename(blob.name)
		fullName, extension = blob_name.rsplit('.', 1)
		# Download the image
		blob_bytes = blob.download_as_bytes()
		image_array = np.frombuffer(blob_bytes, dtype=np.uint8)
		image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
		# encode_face(image, fullName)
		rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

	# detect the (x, y)-coordinates of the bounding boxes
	# corresponding to each face in the input image
		boxes = face_recognition.face_locations(rgb, model="cnn")
	# compute the facial embedding for the face
		encodings = face_recognition.face_encodings(rgb, boxes)

		# loop over the encodings
		for encoding in encodings:
			# add each encoding + name to our set of known names and
			# encodings
			knownEncodings.append(encoding)
			knownNames.append(fullName)


# loop over the image paths
# for (i, imagePath) in enumerate(imagePaths):
# 	# extract the person name from the image path
# 	print("[INFO] processing image {}/{}".format(i + 1,
# 		len(imagePaths)))
# 	name = imagePath.split(os.path.sep)[-2]

# 	# load the input image and convert it from RGB (OpenCV ordering)
# 	# to dlib ordering (RGB)
# 	image = cv2.imread(imagePath)
# 	rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# 	# detect the (x, y)-coordinates of the bounding boxes
# 	# corresponding to each face in the input image
# 	boxes = face_recognition.face_locations(rgb,
# 		model="hog")

# 	# compute the facial embedding for the face
# 	encodings = face_recognition.face_encodings(rgb, boxes)

# 	# loop over the encodings
# 	for encoding in encodings:
# 		# add each encoding + name to our set of known names and
# 		# encodings
# 		knownEncodings.append(encoding)
# 		knownNames.append(name)

# dump the facial encodings + names to disk
print("[INFO] serializing encodings...")
read_all_images_from_folder("images/")
data = {"encodings": knownEncodings, "names": knownNames}
print("knownnames", knownNames)
f = open("encodings.pickle", "wb")
f.write(pickle.dumps(data))
f.close()

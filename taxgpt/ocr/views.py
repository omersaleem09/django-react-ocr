from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
from .models import ExtractedText, CustomUser
from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist
import tempfile
import pytesseract
from pdf2image import convert_from_path
import cv2
import numpy as np
import re
from collections import namedtuple
import math
from django.contrib.auth import authenticate  # Add this import statement
from pytesseract import Output  # Add this import statement


# Create a named tuple for OCR locations
OCRLocation = namedtuple("OCRLocation", ["id", "x", "y", "w", "h"])

# Define the OCR locations using the named tuple
OCR_LOCATIONS = [
    OCRLocation("ssn", 552, 229, 209, 22),
    OCRLocation("ein", 73, 330, 190, 22),
    OCRLocation("f_name", 84, 452, 115, 21),
    OCRLocation("l_name", 223, 453, 50, 19),
    OCRLocation("emp_name", 84, 866, 76, 22),
    OCRLocation("emp_last_name", 562, 868, 56, 20),
    OCRLocation("wit", 1303, 340, 92, 22),
    OCRLocation("fit", 1808, 340, 73, 22),
    OCRLocation("ssw", 1303, 438, 92, 22),
    OCRLocation("sst", 1810, 438, 130, 22),
    OCRLocation("mwt", 1303, 539, 92, 22),
    OCRLocation("mtw", 1808, 539, 92, 22),
    OCRLocation('address1', 85, 509, 54, 21),
    OCRLocation('address2', 162, 507, 77, 23),
    OCRLocation('address3', 261, 510, 36, 21)
]

@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def user_login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        user = None
        if '@' in username:
            try:
                user = CustomUser.objects.get(email=username)
            except ObjectDoesNotExist:
                pass

        if not user:
            user = authenticate(username=username, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    if request.method == 'POST':
        try:
            # Delete the user's token to logout
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def convert_pdf_to_images(pdf_path):
    images = convert_from_path(pdf_path)
    return images

def preprocess_image(image):
    try:
        # Convert the PIL image to a numpy array
        image_np = np.array(image)

        # Ensure the image is in RGB mode
        if len(image_np.shape) == 2:
            image_np = cv2.cvtColor(image_np, cv2.COLOR_GRAY2RGB)

        # Rotate the image to the correct orientation
        rotated_image = rotate_image(image_np)

        # Convert the rotated image to grayscale
        gray_image = cv2.cvtColor(rotated_image, cv2.COLOR_BGR2GRAY)
        return gray_image
    except Exception as e:
        # Handle any exceptions that may occur during image preprocessing
        print(f"Error during image preprocessing: {str(e)}")
        return None

def rotate_image(image):
    # Step 1: Detect text contours using Canny edge detection
    edges = cv2.Canny(image, 50, 150, apertureSize=3)
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)

    # Step 2: Find the dominant angle of text
    angles = []

    for rho, theta in lines[0]:
        angle = math.degrees(theta)
        angles.append(angle)

    # Most common angle
    dominant_angle = np.median(angles)

    # Step 3: Rotate the image to the dominant angle
    rotated_image = rotate(image, 90 - dominant_angle)

    return rotated_image

def rotate(image, angle):
    # Get the image center
    center = tuple(np.array(image.shape[1::-1]) / 2)

    # Perform the rotation
    rot_mat = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated_image = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)

    return rotated_image

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def file_upload(request):
    if request.method == "POST":
        try:
            # Get the uploaded PDF file from the request
            pdf_file = request.FILES.get('file')

            # Create a temporary file to save the PDF
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_pdf:
                for chunk in pdf_file.chunks():
                    temp_pdf.write(chunk)
                temp_pdf_path = temp_pdf.name

            # Convert PDF to images
            images = convert_pdf_to_images(temp_pdf_path)

            detected_text_boxes = []

            # Create a dictionary to store OCR values
            ocr_values = {}

            for image in images:
                img_orientation = pytesseract.image_to_osd(image, config=' - psm 0')
                angle = int(re.search(r'Orientation in degrees: \d+', img_orientation).group().split(':')[-1].strip())
                confidence = float(re.search(r'Orientation confidence: \d+\.\d+', img_orientation).group().split(':')[-1].strip())
                if angle == 90 and confidence > 2.0:
                    image_np = np.array(image)
                    rotated_image = cv2.rotate(image_np, cv2.ROTATE_90_COUNTERCLOCKWISE)
                elif angle == 180 and confidence > 2.0:
                    image_np = np.array(image)
                    rotated_image = cv2.rotate(image_np, cv2.ROTATE_180)
                elif angle == 270 and confidence > 2.0:
                    image_np = np.array(image)
                    rotated_image = cv2.rotate(image_np, cv2.ROTATE_90_CLOCKWISE)
                else:
                    rotated_image = np.array(image)

                annotated_image = np.array(rotated_image)
                d = pytesseract.image_to_data(annotated_image, output_type=Output.DICT)
                n_boxes = len(d['text'])
                bounding_boxes = []

                for i in range(n_boxes):
                    if int(d['conf'][i]) > 60:
                        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                        cv2.rectangle(annotated_image, (x, y), (x + w, y + h), (0, 255, 0), 2)

                        # Extract the text
                        text = d['text'][i]

                        # Append the bounding box coordinates and text to the list
                        bounding_boxes.append({'x': x, 'y': y, 'w': w, 'h': h, 'text': text})

                for location in OCR_LOCATIONS:
                    for box in bounding_boxes:
                        if (
                            location.x <= box['x'] <= (location.x + location.w) and
                            location.y <= box['y'] <= (location.y + location.h)
                        ):
                            # Store the OCR value in the dictionary
                            ocr_values[location.id] = box['text']

                address_fields = ['address1', 'address2', 'address3']
                ocr_values['address'] = ' '.join(ocr_values[field] for field in address_fields if field in ocr_values)

                ocr_field_mapping = {
                    'ssn': 'ssn',
                    'ein': 'ein',
                    'f_name': 'f_name',
                    'l_name': 'l_name',
                    'emp_name': 'emp_name',
                    'emp_last_name': 'emp_last_name',
                    'wit': 'wtc_val',
                    'fit': 'fit_val',
                    'ssw': 'ssw_val',
                    'sst': 'sst_val',
                    'mwt': 'mwt_val',
                    'mtw': 'mtw_val',
                    'address': 'address'
                }

                # Create an instance of the ExtractedText model and set the fields
                extracted_text = ExtractedText(user=request.user, pdf_file=pdf_file)
                for ocr_key, model_field in ocr_field_mapping.items():
                    if ocr_key in ocr_values:
                        setattr(extracted_text, model_field, ocr_values[ocr_key])

                extracted_text.save()

                return Response({'ocr_values': ocr_values}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'error': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

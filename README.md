# Badge Upload Project

## Overview

This Django project allows users to upload images as badges. Each badge is a circular avatar that adheres to specific criteria: it must be 512x512 pixels, contain only non-transparent pixels within a circular area, and feature colors that convey a "happy" feeling. The project includes functionality to validate and automatically adjust uploaded images to meet these criteria.

## Features

- **Image Upload**: Users can upload images to be used as badges.
- **Automatic Adjustment**: Images are automatically resized to 512x512 pixels and cropped to a circular shape with a transparent background.
- **Color Validation**: The colors of the badge are analyzed to ensure they give off a "happy" feeling. Images are adjusted to meet this criterion if necessary.
- **Admin Interface**: Admins can manage uploaded images through the Django admin interface.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Django 3.2 or higher
- Pillow library for image processing

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/SNAYZZ72/TechAssignement.git
   cd TechAssignmentBadge

2. Install the required packages:
   ```bash
    pip install -r requirements.txt
   
3. Apply migrations:
    ```bash
    python manage.py migrate
   
4. Create a superuser:
    ```bash
    python manage.py createsuperuser

5. Run the server:
    ```bash
    python manage.py runserver
   
6. Open the application in your web browser:
    ```
    http://localhost:8000/
   
7. Access the admin interface:
    ```
    http://localhost:8000/admin/
    ```
    Use the superuser credentials created in step 4 to log in.

## Structure of the Project

The project is structured as follows:



## Project Structure

The project is structured as follows:

- `TechAssignmentBadge/`: Main project directory.
  - `settings.py`: Contains project settings.
  - `urls.py`: Defines project URL configurations.
- `imageUploads/`: Application directory for image uploads.
  - `models.py`: Defines the `Image` model.
  - `views.py`: Handles requests and responses for image uploading.
  - `forms.py`: Contains the form for image upload, including validation and adjustment logic.
  - `admin.py`: Configuration for the Django admin interface.
  - `urls.py`: URL configurations for the `imageUploads` app.
- `templates/`: Directory for HTML templates used by the application.
- `images/`: Directory where uploaded images are stored (configured in `settings.py`).
- `migrations/`: Contains database migrations for the `imageUploads` app.

This structure ensures a clear separation of concerns, with the `imageUploads` app handling all aspects related to image processing and upload functionality.

## Usage

### Image Upload

To upload an image, navigate to the home page and click the "Upload Image" button. Select an image file from your computer and click "Upload" to submit the form. The image will be processed and displayed on the page.

### Admin Interface

The admin interface can be accessed at `http://localhost:8000/admin/`. Log in with the superuser credentials created during installation. From the admin interface, you can view, add, edit, and delete images.


## Acknowledgements

This project was created as part of a technical assignment for a job application. The original requirements and specifications were provided by the employer.

## Contact

For any questions or feedback, feel free to contact me at [said.sabri@etu.estia.fr](mailto:said.sabri@etu.estia.fr).
```
# Path: requirements.txt
asgiref==3.7.2
Django==5.0.2
pillow==10.2.0
sqlparse==0.4.4
tzdata==2024.1
```







   
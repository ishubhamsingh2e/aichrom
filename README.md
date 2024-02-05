# Aichrom Backend Testing Guide

- All the wallpapers are stored in `media/wallpapers`.

## Installation

```shell
pip install virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run

```shell
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```


Certainly! Below is an in-depth documentation and API usage guide for your Django project. This documentation is meant to be added to your README.md file.

# Django Project Documentation

## Table of Contents
- [Models](#models)
  - [IconPack](#iconpack)
  - [IconPackImage](#iconpackimage)
  - [Wallpaper](#wallpaper)
  - [Preference](#preference)
  - [AppUser](#appuser)
- [Views](#views)
  - [WallpaperListView](#wallpaperlistview)
  - [IconPackApiView](#iconpackapiview)
  - [GetPreferenceImage](#getpreferenceimage)
  - [SendOTP](#sendotp)
  - [VerifyOTP](#verifyotp)
- [URLs](#urls)

## Models

### IconPack
Represents an icon pack in the system.

#### Fields:
- `name`: CharField - Maximum length of 100 characters.
- `preview`: ImageField - Uploaded image representing the icon pack preview.
- `icon_pack`: FileField - Uploaded icon pack file (ZIP format) with allowed extensions.
- `created_at`: DateTimeField - Automatically set to the creation date and time.
- `updated_at`: DateTimeField - Automatically updated to the latest modification date and time.

#### Methods:
- `save(self, *args, **kwargs)`: Overrides the save method to sort and move icon pack images to their respective folders.

#### Related Model:
- `IconPackImage`: Represents images associated with an icon pack.

### IconPackImage
Represents images associated with an icon pack.

#### Fields:
- `icon_pack`: ForeignKey - Links to the parent IconPack.
- `image_url`: ImageField - Uploaded image associated with the icon pack.

### Wallpaper
Represents wallpapers in the system.

#### Fields:
- `title`: CharField - Maximum length of 100 characters.
- `image_url`: ImageField - Uploaded image representing the wallpaper.
- `created_at`: DateTimeField - Automatically set to the creation date and time.

### Preference
Represents user preferences for wallpapers.

#### Fields:
- `image`: ImageField - Uploaded image representing the user preference.
- `color`: CharField - Maximum length of 6 characters, representing a color code.
- `male`: BooleanField - Represents the user's gender.
- `style_1_Code`: CharField - Maximum length of 100 characters, representing a style code.
- `style_2_Code`: CharField - Maximum length of 100 characters, representing another style code.

### AppUser
Represents a user in the system.

#### Fields:
- `phone`: CharField - Maximum length of 15 characters, unique.
- `otp`: CharField - Maximum length of 6 characters, storing the one-time password.
- `updated_at`: DateTimeField - Automatically updated to the latest modification date and time.

## Views

### WallpaperListView
Returns a JSON response containing a list of wallpapers based on the requested page and items per page.

#### Endpoint: `/api/wallpapers/`
- **Method**: `GET`
- **Parameters**:
  - `page` (optional): Page number for pagination. Default is 1.
  - `items` (optional): Number of items per page. Default is 20.

#### Response:
```json
{
  "total_pages": 2,
  "current_page": 1,
  "total_images": 25,
  "images": [
    {"id": 1, "title": "Wallpaper 1", "image_url": "/media/wallpapers/.../image.jpg", "created_at": "2022-02-04T12:34:56Z"},
    ...
  ]
}
```

### IconPackApiView
Handles requests related to icon packs.

#### Endpoint: `/api/iconpacks/`
- **Method**: `GET`
- **Parameters**:
  - `page` (optional): Page number for pagination. Default is 1.

#### Endpoint: `/api/iconpacks/`
- **Method**: `POST`
- **Parameters**:
  - `id`: ID of the requested icon pack.
  - `token`: JWT token for authentication.

#### Response:
```json
{
  "total_pages": 2,
  "current_page": 1,
  "total_icon_packs": 10,
  "icon_packs": [
    {"id": 1, "name": "Icon Pack 1", "preview": "/media/icon-packs/.../preview.jpg"},
    ...
  ]
}
```

### GetPreferenceImage
Returns the image URL based on user preferences.

#### Endpoint: `/api/get_preference_image/`
- **Method**: `POST`
- **Parameters**:
  - `color`: User-selected color.
  - `male`: User's gender (boolean).
  - `style_1`: Style code 1.
  - `style_2`: Style code 2.

#### Response:
```json
{
  "success": true,
  "image_url": "/media/preference/.../image.jpg"
}
```

### SendOTP
Sends or updates OTP to the user's phone number.

#### Endpoint: `/api/send_otp/`
- **Method**: `POST`
- **Parameters**:
  - `phone`: User's phone number.

#### Response:
```json
{
  "success": true,
  "message": "OTP sent or updated successfully",
  "otp": 123456
}
```

### VerifyOTP
Verifies the received OTP for the user.

#### Endpoint: `/api/verify_otp/`
- **Method**: `POST`
- **Parameters**:
  - `phone`: User's phone number.
  - `otp`: User-entered OTP.

#### Response:
```json
{
  "success": true,
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwaG9uZSI6IjE2Mzg0OTY5NjEiLCJpYXQiOjE2Mzg0OTY5NjEsImV4cCI6MTYzg0OTczMTYxLCJqdGkiOiJmMGZkMDAwMjM0YjQzYWI2OWFiZjk1YzFkMmRkNjMxNjg4M2ZiNjgyNTFhZDdmN2QzNTA4NGRiN2IyN2RiNTMyMDM1MWMzMTY2NzBkODk5MzQyMDc0OTQzODYyMTIxMTI3MzM3NzIwMTIzNDU2Nzg0MTAxMjM0NTY3ODQxMDEyMzQ1Njc4NDEwMTIzNDU2Nzg0MTAxIiwic2NvcGUiOiJkYXRhYmFzZSB1c2VyIiwiZ3JvdXAiOiJleHRlcm5hbCIsInVzZXJfaWQiOjF9.9BBQTF5GtEoBxE2BbE

3qarWGL8OvY7wVi9Z0JANlycM"
}
```

## URLs

### Wallpaper List
- **Endpoint**: `/wallpapers/`
- **View**: `WallpaperListView`
- **Description**: Retrieves a paginated list of wallpapers.

### Icon Pack API
- **Endpoint**: `/iconpacks/`
- **View**: `IconPackApiView`
- **Description**: Retrieves a paginated list of icon packs and details of a specific icon pack based on ID.

### Send OTP
- **Endpoint**: `/send_otp/`
- **View**: `SendOTP`
- **Description**: Sends or updates OTP to the user's phone number.

### Verify OTP
- **Endpoint**: `/verify_otp/`
- **View**: `VerifyOTP`
- **Description**: Verifies the received OTP for the user.

Feel free to customize this documentation further based on your project's specific needs and functionalities.
